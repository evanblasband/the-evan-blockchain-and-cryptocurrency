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


def test_transaction_update_amount_exceeds_balance():
    """
    Trying to update transaction when amount exceeds the sender's balance,
    should throw an exception
    :return:
    """
    sender_wallet = Wallet()
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient="recipient", amount=50
    )
    with pytest.raises(Exception, match="Amount exceeds the balance"):
        transaction.update_transaction(
            sender_wallet=sender_wallet,
            recipient="recipient",
            amount=sender_wallet.balance + 1000,
        )


def test_transaction_update_existing_recipient():
    """
    Updating the transaction amount for an already existing recipient
    :return:
    """
    amount_1 = 50
    amount_2 = 75
    assert amount_1 + amount_2 < STARTING_BALANCE
    recipient = "recipient"
    sender_wallet = Wallet()
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient=recipient, amount=amount_1
    )

    transaction.update_transaction(
        sender_wallet=sender_wallet, recipient=recipient, amount=amount_2
    )

    assert (
        transaction.output[sender_wallet.address]
        == STARTING_BALANCE - amount_1 - amount_2
    )
    assert transaction.output[recipient] == amount_1 + amount_2
    assert Wallet.verify(
        pub_key=transaction.input["public_key"],
        data=transaction.output,
        signature=transaction.input["signature"],
    )


def test_transaction_update_new_recipient():
    """
    adding a new recipient to the transaction
    :return:
    """
    amount_1 = 50
    amount_2 = 75
    assert amount_1 + amount_2 < STARTING_BALANCE
    recipient_1 = "recipient1"
    recipient_2 = "recipient2"
    sender_wallet = Wallet()
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient=recipient_1, amount=amount_1
    )

    transaction.update_transaction(
        sender_wallet=sender_wallet, recipient=recipient_2, amount=amount_2
    )

    assert (
        transaction.output[sender_wallet.address]
        == STARTING_BALANCE - amount_1 - amount_2
    )
    assert transaction.output[recipient_1] == amount_1
    assert transaction.output[recipient_2] == amount_2
    assert Wallet.verify(
        pub_key=transaction.input["public_key"],
        data=transaction.output,
        signature=transaction.input["signature"],
    )


def test_valid_transaction():
    """
    Test a valid transaction throws no exceptions
    :return:
    """
    sender_wallet = Wallet()
    recipient = "recipient"
    Transaction.is_valid_transaction(
        Transaction(sender_wallet=sender_wallet, recipient=recipient, amount=50)
    )


def test_valid_transaction_invalid_outputs():
    """
    Test a transaction where the outputs do not add up
    :return:
    """
    sender_wallet = Wallet()
    recipient = "recipient"
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient=recipient, amount=50
    )
    transaction.output[recipient] = 12
    with pytest.raises(Exception, match="Invalid output transaction total"):
        Transaction.is_valid_transaction(transaction=transaction)


def test_valid_transaction_invalid_signature():
    """
    Test a transaction where the signature is not valid
    :return:
    """
    sender_wallet = Wallet()
    recipient = "recipient"
    transaction = Transaction(
        sender_wallet=sender_wallet, recipient=recipient, amount=50
    )
    transaction.input["signature"] = Wallet().sign(data=transaction.output)
    with pytest.raises(Exception, match="Invalid signature"):
        Transaction.is_valid_transaction(transaction=transaction)
