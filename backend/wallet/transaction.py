import time
import uuid

from backend.wallet.wallet import Wallet


class Transaction:
    """
    Document of an exchange in currency from a sender to one or more
    recipients.
    """

    def __init__(self, sender_wallet: Wallet, recipient: str, amount: int):
        """Constructor for Transaction"""
        self.id = str(uuid.uuid4())[0:8]
        self.output = Transaction.create_output(
            sender_wallet=sender_wallet, recipient=recipient, amount=amount
        )
        self.input = Transaction.create_input(
            sender_wallet=sender_wallet, output=self.output
        )

    @staticmethod
    def create_output(sender_wallet: Wallet, recipient: str, amount: int) -> dict:
        """
        Structure output data for the transaction
        :param sender_wallet: the wallet where amount is being sent from
        :param recipient: the recipient address for the amount to fo to
        :param amount: the amount being sent
        :return: dictionary with the structured data for the output
        """
        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds senders balance")

        output = {
            recipient: amount,
            sender_wallet.address: sender_wallet.balance - amount,
        }

        return output

    @staticmethod
    def create_input(sender_wallet: Wallet, output: dict) -> dict:
        """
        Structure input data for the transaction.
        Sign transaction and include senders public key and address.
        :param sender_wallet: the wallet where amount is being sent from
        :param output: The output data for a given transaction
        :param amount: the amount being sent
        :return: dictionary with the structured data for the input
        """
        return {
            "timestamp": time.time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(data=output),
        }


def main():
    transaction = Transaction(sender_wallet=Wallet(), recipient="recipient", amount=10)
    print(f"transaction.__dict__: {transaction.__dict__}")


if __name__ == "__main__":
    main()
