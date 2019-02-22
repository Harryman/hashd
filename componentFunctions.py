import hashlib
import time
import binascii
from mnemonic import Mnemonic
import pickledb
import socket
from ecdsa import SigningKey, VerifyingKey, SECP256k1
db = pickledb.load('test.db',True)
m = Mnemonic('english')

#HOST = ''
#PORT = 44444
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST,PORT))
#s.listen(1)
#conn, addr = s.accept()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def bCastMerkle(opType,value):
    hsh = hashlib.sha256()
    hsh.update(opType)
    hashC = hsh.digest()
    hsh = hashlib.sha256()
    hsh.update(value)
    hashD = hsh.digest()
    hsh = hashlib.sha256()
    hsh.update(hashC)
    hsh.update(hashD)
    hashA = hsh.digest()
    return [hashC,hashD,hashA]


def mRoot(hashA,hashB):
    hsh = hashlib.sha256()
    hsh.update(hashA)
    hsh.update(hashB)
    root = hsh.digest()
    return root

def sliceOp(op): #slices integer value into a 4byte array to ensure correctness when constructing the block
    opB = bytearray(4)
    for i in range(4):
        opB[i] = (op >> (24 - i * 8) & 255)
    return opB

def makeBlock(op,mRoot,prevBlkSig,sk):
        opPad = sliceOp(op)
        sigField = opPad + mRoot + prevBlkSig
        #print(sigField)
        blkSig = sk.sign(sigField)
        return blkSig

def addWork(blockSig, duration):
    nonce = 0
    low = bytearray(32)
    for i in range(32):
        low[i] = 255
    start = time.time()
    now = start
    while (start + duration) > now: 
        now = time.time()
        h = hashlib.sha256()
        h.update(blockSig)
        h.update(nonce.to_bytes(16,'little',signed=False))
        crnt = h.digest()
        if crnt < low:
            low = crnt
            lowNonce = nonce
        nonce = nonce + 1 
    lowout = binascii.hexlify(low)
    print(lowout)
    print(lowNonce)
    return lowNonce



def init():
    dsk = SigningKey.generate(curve=SECP256k1)
    dvk = dsk.get_verifying_key()
    isk = SigningKey.generate(curve=SECP256k1)
    ivk = isk.get_verifying_key()
    h = hashlib.sha256()
    h.update(ivk.to_string())
    ikHash = h.digest()
    print("Write these words down, this will allow you to recover your identity if this device is hacked or stolen(BIP39):")
    print("================================================")
    print(m.to_mnemonic(isk.to_string())) #replace with mnemonic!!!
    print("================================================")
    bCast = bCastMerkle(b"Key Replacement",dvk.to_string()+ikHash)
    mr = mRoot(bCast[2], bytearray(32))
    blkSig = makeBlock(1,mr,bytearray(64),dsk)
    return blkSig, dsk

    
def say(op,typ, value,prevBlk, dataHash, sk,workDur):
    lhashes = bCastMerkle(typ,value)
    mr = mRoot(lhashes[2],dataHash)
    blkSig = makeBlock(op,mr,prevBlk,sk)
    nonce = addWork(blkSig, workDur)
    return blkSig
    
def tweet(prevBlk, tweet, hashTag, sk, workDur):
    h = hashlib.sha256()
    h.update(tweet.encode('utf-8'))
    dataHash = h.digest()
    tweet.encode('utf-8')
    return say(5,b"Tweet",hashTag.encode('utf-8'),prevBlk,dataHash,sk,workDur)
    


# ## Initialize a New Identity
# 1. Generates two keys
#     - One key is stored on the device(Hot)
#     - Second key is out put as a BIP39 Mnemonic(Cold)
# 2. The hash of the Cold key's public key is included in the first block of this Identity
# 3. The merkleroot and previous block signature(all zeros since this the first block) are signed by the Hot key
     

blkSig0, deviceSK = init()


# ## Broadcast a Well Known name for this idchain
# This example does 10 seconds of proof of work on the second block in our chain to broadcast a name we want to be known as
# - we can add more work to this later 
# - we have the option to have multiple names


blkSig1 = say(2,b"Well Known",b"HashD",blkSig0,bytearray(32),deviceSK,10)


# ## Broadcast a Service Endpoint
# Now that people know our name we want then to be able to connect to us
# 
# Since we have already 10 seconds of PoW we don't need to add much work to broadcast a service endpoint
# 
# Metcalf's Law means adding more peers is a postive sum game, other nodes will value the data that allows them to connect to more peers and information. Self incentivizing them to keep more of this message type for a given amount of PoW


ip = get_ip()

blkSig2 = say(3,b"Service Endpoint",ip.encode('utf-8'),blkSig1,bytearray(32),deviceSK,2)


# ## Broadcast a Tweet 
# Because everyone wants to be heard we have to shout very loudly, or turn up the transmit power of our virtual radio broadcast
# 
# We will do 60 seconds of hash, which on this laptop factoring in depreciation and energy will cost me about $0.0002, which means I could buy 800KB on a modern NVME SSD
# 
# To store the data that would allow people to discover the tweet a node would only need to store 378b verify a few hashes and a signature
# 
# The Nash Equilibrium of cost to broadcast vs cost to network for storage means roughly 2100 nodes could store this broadcast with even cost to publisher and listeners


blkSig3 = tweet(blkSig2,"First","ethDenver",deviceSK,60)

