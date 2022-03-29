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
