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

    def update_transaction(
        self, sender_wallet: Wallet, recipient: str, amount: int
    ) -> None:
        """
        Update a transaction that is already in a block i.e. add
        recipients or update amount to existing recipient.
        :param sender_wallet: the wallet that is sending the amount
        :param recipient: the recipient to add or change amount of
        :param amount: amount to add or change
        :return: dictionary with the updated recipients and their
        corresponding amounts
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception("Amount exceeds the balance")

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet=sender_wallet, output=self.output)

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
        :return: dictionary with the structured data for the input
        """
        return {
            "timestamp": time.time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(data=output),
        }

    @staticmethod
    def is_valid_transaction(transaction: "Transaction"):
        """
        Validates the format of a transaction.  Raises Exception for invalid
        transactions.
        :param transaction: the transaction to validate
        :return:
        """
        output_total = sum(transaction.output.values())
        if transaction.input["amount"] != output_total:
            raise Exception("Invalid output transaction total")

        if not Wallet.verify(
            pub_key=transaction.input["public_key"],
            data=transaction.output,
            signature=transaction.input["signature"],
        ):
            raise Exception("Invalid signature")


def main():
    transaction = Transaction(sender_wallet=Wallet(), recipient="recipient", amount=10)
    print(f"transaction.__dict__: {transaction.__dict__}")


if __name__ == "__main__":
    main()
