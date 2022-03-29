from backend.wallet.transaction import Transaction


class TransactionPool:
    """
    Class for getting all transactions together in order to be included in
    the blockchain
    """

    def __init__(
        self,
    ):
        """Constructor for TransactionPool"""
        self.transaction_map = {}

    def set_transaction(self, transaction: Transaction) -> None:
        """
        Adding a transaction to the transaction pool
        :param transaction: the transaction to be set
        :return:
        """
        self.transaction_map[transaction.id] = transaction
