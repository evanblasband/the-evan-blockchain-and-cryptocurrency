# when you import something it actually runs everything in that file
from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


class Blockchain:
    """
    Blockchain is a ledger of transactions.
    Implemented by connecting a series of Blocks (data set of transactions)
    together
    """

    def __init__(
        self,
    ):
        """Constructor for Blockchain"""
        self.chain = [Block.genesis()]

    def __repr__(self) -> str:
        """
        formatting hte chain for printing
        :return:
        """
        return f"Blockchain data: {self.chain}"

    def to_json(self) -> list:
        """
        Serialize the blockchain into a list of serialized blocks
        :return: the chain list of serialized blocks
        """
        return list(map(lambda block_: block_.to_json(), self.chain))

    def add_block(self, data) -> None:
        """
        adding a block to the chain
        :param data: the data to be added (i.e. a list of transactions)
        :return:
        """
        last_block = self.chain[-1]  # the last block in the list
        self.chain.append(Block.mine_block(last_block=last_block, data=data))

    def replace_chain(self, chain: list) -> None:
        """
        Replace local chain with the incoming one if the following rules apply:
            - incoming chain must be longer than the old one
            - Chain must be formatted properly
        :param chain: the incoming chain to replace with
        :return:
        """
        if len(chain) <= len(self.chain):
            raise Exception("Can not replace chain. New chain is not longer")

        try:
            Blockchain.is_valid_chain(chain=chain)
        except Exception as e:
            raise Exception(f"Can not replace chain.  New  Chain is invalid: " f"{e}")
        # New chain was valid so we replace it
        self.chain = chain

    @staticmethod
    def from_json(chain_json: list) -> "Blockchain":
        """
        Deserialize a list of serialized blocks into a blockchain instance
        :param chain_json: the json format of the root node's current
        blockchain
        :return: a chain list of block instances
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json=block_json), chain_json)
        )

        return blockchain

    @staticmethod
    def is_valid_chain(chain: list) -> None:
        """
        Validates the incoming chain.
        Enforces the following rules for the blockchain:
            - Must start with the genesis block
            - blocks must be formatted correctly
        :param chain: the chain to validate
        :return:
        """
        if chain[0] != Block.genesis():
            raise Exception("Chain does not start with the genesis block")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block=last_block, block=block)

        Blockchain.is_valid_transaction_chain(chain=chain)

    @staticmethod
    def is_valid_transaction_chain(chain: list) -> None:
        """
        Enforce the rules of a chain composed of transactions:
            - Each transaction must only appear once in the chain
            - There can only be one mining reward per block
            - Each transaction must be valid
        :param chain: the chain to validate
        :return:
        """
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json=transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f"Transaction: {transaction.id} is not " f"unique")
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            "Can only be one mining reward per "
                            f"block.  Check block with hash: "
                            f"{block.hash_}"
                        )
                    has_mining_reward = True
                else:
                    # Makes sure transactions are valid according to blockchain
                    # history
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        blockchain=historic_blockchain,
                        address=transaction.input["address"],
                    )
                    if historic_balance != transaction.input["amount"]:
                        raise Exception(
                            f"Transaction: {transaction.id} has "
                            f"invalid input amount"
                        )

                Transaction.is_valid_transaction(transaction=transaction)


def main():
    blockchain = Blockchain()
    blockchain.add_block(data="one")
    blockchain.add_block(data="two")

    print(blockchain)
    print(f"blockchain.py __name__ : {__name__}")


if __name__ == "__main__":
    main()
