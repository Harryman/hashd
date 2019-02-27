import time
import hashlib
import binascii


def add_work(signature, duration):
    nonce = 0
    low = bytearray(32)

    for i in range(32):
        low[i] = 255

    start = time.time()
    now = start

    while (start + float(duration)) > now:
        now = time.time()
        h = hashlib.sha256()
        h.update(signature.encode("utf-8"))
        h.update(nonce.to_bytes(16, "little", signed=False))
        current = h.digest()
        if current < low:
            low = current
        nonce = nonce + 1

    result = binascii.hexlify(low)

    return result, nonce
