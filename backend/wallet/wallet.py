import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

from backend.config import STARTING_BALANCE


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of a miner's balance.
    Allows a miner to authorize transactions.
    """

    def __init__(
        self,
    ):
        """Constructor for Wallet"""
        self.address = str(uuid.uuid4())[0:8]  # shorter uuid for now for
        # debugging
        self.private_key = ec.generate_private_key(
            curve=ec.SECP256K1(), backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.balance = STARTING_BALANCE


def main():
    wallet = Wallet()
    print(f"wallet.__dict__: {wallet.__dict__}")


if __name__ == "__main__":
    main()
