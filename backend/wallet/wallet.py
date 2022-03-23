import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
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

    def sign(self, data) -> bytes:
        """
        Generate a signature based on the data and the local private key
        :param data: the data to sign
        :return: returns a signed
        """
        return self.private_key.sign(
            data=json.dumps(data).encode("UTF-8"),
            signature_algorithm=ec.ECDSA(hashes.SHA256()),
        )

    @staticmethod
    def verify(pub_key: ec.EllipticCurvePublicKey, data, signature: bytes) -> bool:
        """
        verify a signature based on the public key and the data.
        :param pub_key: the public key to check signature against
        :param data: the data to verify
        :param signature: the signature to check against
        :return: true if the signature is valid
        """
        try:
            pub_key.verify(
                signature=signature,
                data=json.dumps(data).encode("UTF-8"),
                signature_algorithm=ec.ECDSA(hashes.SHA256()),
            )
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f"wallet.__dict__: {wallet.__dict__}")
    data = "test-data"
    signature = wallet.sign(data)
    print(f"signature: {signature}")
    should_be_valid = Wallet.verify(
        pub_key=wallet.public_key, data=data, signature=signature
    )
    print(f"should_be_valid: {should_be_valid}")

    should_be_invalid = Wallet.verify(
        pub_key=Wallet().public_key, data=data, signature=signature
    )
    print(f"should_be_invalid: {should_be_invalid}")


if __name__ == "__main__":
    main()
