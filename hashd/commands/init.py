from mnemonic import Mnemonic
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib

from hashd.crypto import merkle

m = Mnemonic("english")


def init(args):
    dsk = SigningKey.generate(curve=SECP256k1)
    dvk = dsk.get_verifying_key()
    isk = SigningKey.generate(curve=SECP256k1)
    ivk = isk.get_verifying_key()
    h = hashlib.sha256()
    h.update(ivk.to_string())
    ikHash = h.digest()
    bCast = merkle.bCastMerkle(b"Key Replacement", dvk.to_string() + ikHash)
    mr = merkle.mRoot(bCast[2], bytearray(32))
    blkSig = merkle.makeBlock(1, mr, bytearray(64), dsk)

    mstr = m.to_mnemonic(isk.to_string())

    print(
        "Write these words down, this will allow you to recover your identity if this device is hacked or stolen(BIP39):"
    )
    print("================================================")
    print(mstr)
    print("================================================")

    return blkSig, dsk
