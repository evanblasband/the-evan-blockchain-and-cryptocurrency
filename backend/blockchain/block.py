import time

from backend.utils.crypto_hash import crypto_hash

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "hash_": "genesis_hash",
    "data": [],
}


class Block:
    """
    Block: unit of storage that makes up the Blockchain when connected
    together.
    Contains data that consists of transactions
    """

    def __init__(self, data, timestamp: int, last_hash: str, hash_: str):
        """Constructor for Block"""
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash_ = hash_
        self.data = data

    def __repr__(self):
        return (
            f"Block("
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"hash_: {self.hash_}, "
            f"data: {self.data}, "
            f")"
        )

    @staticmethod
    def mine_block(last_block: "Block", data) -> "Block":
        """
        Creates a block given the last block and the given data

        :param last_block: the last Block so that we can get its hash_ value
        :param data: whatever data is to be put in this block
        :return: a new block to be added to the chain
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash_
        hash_ = crypto_hash(timestamp, last_hash, data)

        return Block(timestamp=timestamp, last_hash=last_hash, hash_=hash_, data=data)

    @staticmethod
    def genesis() -> "Block":
        """
        Creates the first block to start the blockchain
        :return: an initial block to start the chain
        """
        # return Block(
        #     timestamp=GENESIS_DATA['timestamp'],
        #     last_hash=GENESIS_DATA['last_hash'],
        #     hash_=GENESIS_DATA['genesis_hash'],
        #     data=GENESIS_DATA['data']
        # )
        # Creates the same as above
        return Block(**GENESIS_DATA)


def main():
    print(f"block.py __name__ : {__name__}")

    genesis_block = Block.genesis()
    block = Block.mine_block(last_block=genesis_block, data="first")
    print(block)


if __name__ == "__main__":
    main()
