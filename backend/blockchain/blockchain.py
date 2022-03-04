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

    def add_block(self, data: str) -> None:
        last_block = self.chain[-1]  # the last block in the list
        self.chain.append(Block.mine_block(last_block=last_block, data=data))

    def __repr__(self) -> str:
        return f"Blockchain data: {self.chain}"


def main():
    blockchain = Blockchain()
    blockchain.add_block(data="one")
    blockchain.add_block(data="two")

    print(blockchain)
    print(f"blockchain.py __name__ : {__name__}")


if __name__ == "__main__":
    main()
