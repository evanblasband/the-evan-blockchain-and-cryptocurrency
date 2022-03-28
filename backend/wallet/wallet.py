import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

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
        self.public_key = (
            self.private_key.public_key()
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode("utf-8")
        )
        self.balance = STARTING_BALANCE
        # self.serialize_public_key()

    def sign(self, data) -> tuple[int, int]:
        """
        Generate a signature based on the data and the local private key
        :param data: the data to sign
        :return: a tuple containing the r and s coordinate values for the
        signature, to be used to encode later
        """
        return decode_dss_signature(
            self.private_key.sign(
                data=json.dumps(data).encode("UTF-8"),
                signature_algorithm=ec.ECDSA(hashes.SHA256()),
            )
        )

    # def serialize_public_key(self) -> None:
    #     """
    #     Serialize public key to a string, used inline definition keeping
    #     here for reference
    #     :return:
    #     """
    #     self.public_key = self.public_key.public_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PublicFormat.SubjectPublicKeyInfo,
    #     ).decode("utf-8")

    @staticmethod
    def verify(pub_key: str, data, signature: tuple[int, int]) -> bool:
        """
        verify a signature based on the public key and the data.
        :param pub_key: the public key to check signature against
        :param data: the data to verify
        :param signature: the tuple of r and s values corresponding to
        coordinates on elliptic curve
        :return: true if the signature is valid
        """
        deserialized_pub_key = serialization.load_pem_public_key(
            data=pub_key.encode("utf-8"), backend=default_backend()
        )

        (r, s) = signature

        try:
            deserialized_pub_key.verify(
                signature=encode_dss_signature(r=r, s=s),
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
