from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_verify_valid_signature():
    """
    Should pass with a valid signature
    :return:
    """
    data = {"foo": "test-data"}
    wallet = Wallet()
    signature = wallet.sign(data=data)

    assert Wallet.verify(pub_key=wallet.public_key, data=data, signature=signature)


def test_verify_invalid_signature():
    """
    Should return false because of the InvalidSignature exception
    :return:
    """
    data = {"foo": "test-data"}
    wallet = Wallet()
    signature = wallet.sign(data=data)

    assert not Wallet.verify(
        pub_key=Wallet().public_key, data=data, signature=signature
    )


def test_calculate_balance_no_transaction():
    """
    Testing a wallet balance gets calculated properly based on blockchain
    recorded transactions when not transaction has been made
    :return:
    """
    blockchain = Blockchain()
    wallet = Wallet()

    assert (
        Wallet.calculate_balance(blockchain=blockchain, address=wallet.address)
        == STARTING_BALANCE
    )


def test_calculate_balance_send_transaction():
    """
    Testing a wallet balance gets calculated properly based on blockchain
    recorded transactions after making a transaction to send currency
    :return:
    """
    blockchain = Blockchain()
    wallet = Wallet()

    assert (
        Wallet.calculate_balance(blockchain=blockchain, address=wallet.address)
        == STARTING_BALANCE
    )

    amount = 50
    transaction = Transaction(
        sender_wallet=wallet, recipient="recipient", amount=amount
    )
    blockchain.add_block(data=[transaction.to_json()])

    assert (
        Wallet.calculate_balance(blockchain=blockchain, address=wallet.address)
        == STARTING_BALANCE - amount
    )


def test_calculate_balance_receive_transaction():
    """
    Testing a wallet balance gets calculated properly based on blockchain
    recorded transactions after receiving currency
    :return:
    """
    blockchain = Blockchain()
    wallet = Wallet()

    assert (
        Wallet.calculate_balance(blockchain=blockchain, address=wallet.address)
        == STARTING_BALANCE
    )

    amount = 50
    transaction = Transaction(
        sender_wallet=wallet, recipient="recipient", amount=amount
    )
    blockchain.add_block(data=[transaction.to_json()])

    amount_2 = 20
    transaction_2 = Transaction(
        sender_wallet=Wallet(), recipient=wallet.address, amount=amount_2
    )

    amount_3 = 30
    transaction_3 = Transaction(
        sender_wallet=Wallet(), recipient=wallet.address, amount=amount_3
    )

    blockchain.add_block(data=[transaction_2.to_json(), transaction_3.to_json()])

    assert (
        Wallet.calculate_balance(blockchain=blockchain, address=wallet.address)
        == STARTING_BALANCE - amount + amount_2 + amount_3
    )
