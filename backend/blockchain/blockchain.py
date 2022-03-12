# when you import something it actually runs everything in that file
from backend.blockchain.block import Block


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

    def replace_chain(self, blockchain: "Blockchain") -> None:
        """
        Replace local chain with the incoming one if the following rules apply:
            - incoming chain must be longer than the old one
            - Chain must be formatted properly
        :param blockchain: the incoming chain to replace with
        :return:
        """
        if len(blockchain.chain) <= len(self.chain):
            raise Exception("Can not replace chain. New chain is not longer")

        try:
            Blockchain.is_valid_chain(blockchain=blockchain)
        except Exception as e:
            raise Exception(f"Can not replace chain.  New  Chain is invalid: " f"{e}")
        # New chain was valid so we replace it
        self.chain = blockchain.chain

    @staticmethod
    def is_valid_chain(blockchain: "Blockchain") -> None:
        """
        Validates the incoming chain.
        Enforces the following rules for the blockchain:
            - Must start with the genesis block
            - blocks must be formatted correctly
        :param blockchain: the chain to validate
        :return:
        """
        chain = blockchain.chain
        if chain[0] != Block.genesis():
            raise Exception("Chain does not start with the genesis block")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block=last_block, block=block)


def main():
    blockchain = Blockchain()
    blockchain.add_block(data="one")
    blockchain.add_block(data="two")

    print(blockchain)
    print(f"blockchain.py __name__ : {__name__}")


if __name__ == "__main__":
    main()
