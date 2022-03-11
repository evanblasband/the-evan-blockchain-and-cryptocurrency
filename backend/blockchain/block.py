import time

from backend.config import MINE_RATE
from backend.utils.crypto_hash import crypto_hash
from backend.utils.hex_to_binary import hex_to_bin

# Default values for the genesis block
# pulled out as global variable for testing purposes
GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "genesis_last_hash",
    "hash_": "genesis_hash",
    "data": [],
    "nonce": 0,
    "difficulty": 3,
}


class Block:
    """
    Block: unit of storage that makes up the Blockchain when connected
    together.
    Contains data that consists of transactions
    """

    def __init__(
        self,
        data,
        timestamp: int,
        last_hash: str,
        hash_: str,
        nonce: int,
        difficulty: int,
    ):
        """Constructor for Block"""
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash_ = hash_
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty

    def __repr__(self):
        return (
            f"Block("
            f"timestamp: {self.timestamp}, "
            f"last_hash: {self.last_hash}, "
            f"hash_: {self.hash_}, "
            f"data: {self.data}, "
            f"nonce: {self.nonce}, "
            f"difficulty: {self.difficulty}, "
            f")"
        )

    @staticmethod
    def mine_block(last_block: "Block", data) -> "Block":
        """
        Creates a block given the last block and the given data until a
        block hash is found that meets the leading zeros proof of work
        requirement

        :param last_block: the last Block so that we can get its hash_ value
        :param data: whatever data is to be put in this block
        :return: a new block to be added to the chain
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash_
        difficulty = Block.adjust_difficulty(
            last_block=last_block, new_timestamp=timestamp
        )
        nonce = 0
        hash_ = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_bin(hash_)[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(
                last_block=last_block, new_timestamp=timestamp
            )
            hash_ = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(
            timestamp=timestamp,
            last_hash=last_hash,
            hash_=hash_,
            data=data,
            difficulty=difficulty,
            nonce=nonce,
        )

    @staticmethod
    def adjust_difficulty(last_block: "Block", new_timestamp: int) -> int:
        """
        Calculate the adjusted difficulty based on the MINE_RATE.
        If blocks are mined too fast we will increase the difficulty,
        and decrease difficulty if mined too slow
        :param last_block: to get the timestamp the last block was mined
        :param new_timestamp: used to reference the time new block was mined
        :return:
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if last_block.difficulty - 1 > 0:
            return last_block.difficulty - 1

        return 1

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
        #     nonce=GENESIS_DATA['nonce']
        #     difficulty=GENESIS_DATA['difficulty']
        # )
        # Creates the same as above
        return Block(**GENESIS_DATA)

    @staticmethod
    def is_valid_block(last_block: "Block", block: "Block"):
        """
        Validate a block based on the following set of rules:
            - must have proper last_hash reference
            - must meet proper proof of work requirement
            - difficulty must only adjust by 1
            - block hash must be valid combination of block fields
        :param last_block: the last block in the chain to reference
        :param block: the current block being validated
        :return: whether or not the block is valid
        """

        if block.last_hash != last_block.hash_:
            raise Exception("the block's last_hash must be correct")
        if hex_to_bin(block.hash_)[0 : block.difficulty] != "0" * block.difficulty:
            raise Exception("Proof of work requirement not met")
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("Difficulty was changed by more than 1")

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce,
        )

        if block.hash_ != reconstructed_hash:
            raise Exception("The hash value does not compute")


def main():
    # print(f"block.py __name__ : {__name__}")
    #
    # genesis_block = Block.genesis()
    # block = Block.mine_block(last_block=genesis_block, data="first")
    # print(block)
    genesis_block = Block.genesis()
    good_block = Block.mine_block(last_block=genesis_block, data="foo")
    bad_block = good_block
    bad_block.last_hash = "evil_hash"
    try:
        Block.is_valid_block(last_block=genesis_block, block=bad_block)
        print("The block is valid")
    except Exception as e:
        print(f"is_valid_block: FALSE - {e}")


if __name__ == "__main__":
    main()
