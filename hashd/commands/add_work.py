from hashd.crypto import work
from argparse import Namespace
from operator import itemgetter


def add_work(args: Namespace):
    signature, duration = itemgetter("signature", "duration")(vars(args))
    (result, nonce) = work.add_work(signature, duration)
    print(
        """
            PoW added to: %(signature)s over %(duration)s seconds.
            Lowest hash: %(result)s - Nonce: %(nonce)s
        """
        % locals()
    )
