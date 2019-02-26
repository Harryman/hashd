import time
import hashlib
import binascii


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
        h.update(nonce.to_bytes(16, "little", signed=False))
        crnt = h.digest()
        if crnt < low:
            low = crnt
            lowNonce = nonce
        nonce = nonce + 1

    lowout = binascii.hexlify(low)

    return lowNonce, lowout
