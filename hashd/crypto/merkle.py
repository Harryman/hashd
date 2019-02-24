import hashlib

from .utils import sliceOp


def bCastMerkle(opType, value):
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
    return [hashC, hashD, hashA]


def mRoot(hashA, hashB):
    hsh = hashlib.sha256()
    hsh.update(hashA)
    hsh.update(hashB)
    root = hsh.digest()
    return root


def makeBlock(op, mRoot, prevBlkSig, sk):
    opPad = sliceOp(op)
    sigField = opPad + mRoot + prevBlkSig
    # print(sigField)
    blkSig = sk.sign(sigField)
    return blkSig
