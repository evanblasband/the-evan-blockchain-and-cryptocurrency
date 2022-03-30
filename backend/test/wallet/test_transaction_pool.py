from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction_pool import Transaction, TransactionPool
from backend.wallet.wallet import Wallet


def test_set_transaction():
    """
    Testing that setting a transaction properly works
    :return:
    """
    transaction_pool = TransactionPool()
    transaction = Transaction(sender_wallet=Wallet(), recipient="recipient", amount=10)
    transaction_pool.set_transaction(transaction=transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_blockchain_transactions():
    """
    Make sure that blockchain recorded transactions are removed from the
    transaction pool
    :return:
    """
    transaction_pool = TransactionPool()
    blockchain = Blockchain()
    transaction_1 = Transaction(
        sender_wallet=Wallet(), recipient="recipient", amount=10
    )
    transaction_2 = Transaction(
        sender_wallet=Wallet(), recipient="recipient", amount=20
    )

    transaction_pool.set_transaction(transaction=transaction_1)
    transaction_pool.set_transaction(transaction=transaction_2)

    blockchain.add_block(data=[transaction_1.to_json(), transaction_2.to_json()])

    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transaction(blockchain=blockchain)

    assert transaction_1.id not in transaction_pool.transaction_map
    assert transaction_2.id not in transaction_pool.transaction_map
