import pytest

from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    """
    Testing that creating a transaction gives expected output
    :return:
    """
    sender_wallet = Wallet()
    recipient = "recipient"
    amount = 50
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient=recipient, amount=amount
    )

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert "timestamp" in transaction.input
    assert transaction.input["amount"] == sender_wallet.balance
    assert transaction.input["address"] == sender_wallet.address
    assert transaction.input["public_key"] == sender_wallet.public_key

    assert Wallet.verify(
        pub_key=transaction.input["public_key"],
        data=transaction.output,
        signature=transaction.input["signature"],
    )


def test_transaction_amount_exceeds_balance():
    """
    if amount exceeds the wallet balance we should get an exception
    :return:
    """
    with pytest.raises(Exception, match="Amount exceeds senders balance"):
        Transaction(
            sender_wallet=Wallet(), recipient="recipient", amount=STARTING_BALANCE + 1
        )
