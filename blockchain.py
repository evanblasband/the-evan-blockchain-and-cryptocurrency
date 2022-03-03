# when you import something it actually runs everything in that file
from block import Block


class Blockchain:
    """
    Blockchain is a ledger of transactions.
    Implemented by connecting a series of Blocks (data set of transactions) together
    """

    def __init__(self, ):
        """Constructor for Blockchain"""
        self.chain = []

    def add_block(self, data: str) -> None:
        self.chain.append(Block(data))

    def __repr__(self) -> str:
        return f"Blockchain data: {self.chain}"


def main():
    blockchain = Blockchain()
    blockchain.add_block(data="one")
    blockchain.add_block(data="two")

    print(blockchain)
    print(f'blockchain.py __name__ : {__name__}')


if __name__ == '__main__':
    main()
