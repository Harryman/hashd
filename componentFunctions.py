import hashlib
import time
import binascii
import mnemonic
import pickledb
from ecdsa import SigningKey, VerifyingKey, SECP256k1
db = pickledb.load('test.db',True)


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
        op = sliceOp(op)
        sigField = op + mRoot + prevBlkSig
        print(sigField)
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
        h.update(nonce.to_bytes(16,'big',signed=False))
        crnt = h.digest()
        if crnt < low:
            low = crnt
            lownonce = nonce
        nonce = nonce + 1 
    lowout = binascii.hexlify(low)
    print(lowout)
    return lownonce
        
def hashBench():
    nonce = 0
    preimage = bytearray(64)
    for i in range(64):
        preimage[i] = 255
    low = preimage
    now = time.time()
    last = now
    for i in range(3):
        start = time.time()
        dur = (10**i)
        print(dur)
        while (start + dur) > now: 
            now = time.time()
            h = hashlib.sha256()
            h.update(preimage)
            h.update(nonce.to_bytes(16,'little',signed=False))
            crnt = h.digest()
            if crnt < low:
                low = crnt
                print(now-start)
                print(nonce)
            nonce = nonce + 1 
        lowout = binascii.hexlify(low)
        print(lowout)
        #f'{dur} of hashing = {lowout}'
    print(nonce)
            



# #D init
# Keygen takes roughly 0.1s per key
dsk = SigningKey.generate(curve=SECP256k1)
dvk = dsk.get_verifying_key()
isk = SigningKey.generate(curve=SECP256k1)
ivk = isk.get_verifying_key()
h = hashlib.sha256()
h.update(ivk.to_string())
ikHash = h.digest()
print("Recovery Key. This supercedes your active key, keep it safe an online, you need this to rotate keys:")
print(binascii.hexlify(isk.to_string())) #replace with mnemonic!!!
print("================================================")
bCast = bCastMerkle(b"Key Replacement",dvk.to_string()+ikHash)
mr = mRoot(bCast[2], bytearray(32))
blkSig = makeBlock(1,mr,bytearray(64),dsk)
print("PoW Hash")
nonce = addWork(blkSig,1)
db.set(blkSig,)
print("PubKey")
print(dvk.to_string())
print(len(dvk.to_string()))
print("blkSig")
print(blkSig)
print(len(blkSig))


#verify block
prevBlk = bytearray(64)
def verifySig(blkSig, pubKey):
    vk = VerifyingKey.from_string(pubKey, curve=SECP256k1)
    print(vk.to_string())
    try:
        vk.verify(blkSig,(op+mr+prevBlk))
        print("Valid block Signature")
        return True
    except invalidSigError:
        print("Bad block Signature")
        return False
    
verifySig(blkSig,dvk.to_string())   
        


def workToStorageCalc(computeCost,computeDepriciationMonths,computeWattage,energyCostUSDkwh,storageSizeTB,storageCost, computeTimeSec, messageSizeBytes, hostSubjectiveAverageValueCents):
    dep = computeDepriciationMonths * 2629744 #convert To Seconds
    compDepCentSec = (computeCost*100)/dep #convert to cents of depreciation per second
    compEnrgCentSec = computeWattage * ((energyCostUSDkwh/1000)/(60*60)) #convert to energy cost cents per second
    hashCost = (compDepCentSec+compEnrgCentSec) * computeTimeSec #cost of hash in cents
    kbCost = (storageSizeTB *1000000000)/(storageCost*100) #kb per cent
    networkStorageUsage = hashCost*kbCost
    print("Cost Equivalent Storage(kb)")
    print(networkStorageUsage)
    print("Number of Replications for message size and work, with no subjective value")
    print((networkStorageUsage*1024)/messageSizeBytes)
    print("Number of Replicas with subjective vaue")
    print((((hostSubjectiveAverageValueCents+hashCost)*kbCost)*1024)/messageSizeBytes)

workToStorageCalc(1000,36,1400,.15,1,250,10,400,.01)

