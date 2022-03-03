import time


class Block:
    """
    Block: unit of storage that makes up the Blockchain when connected together.
    Contains data that consists of transactions
    """

    def __init__(self, data, timestamp: int, last_hash: str, hash_: str):
        """Constructor for Block"""
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash_
        self.data = data

    def __repr__(self):
        return (f'Block('
                f'timestamp: {self.timestamp}, '
                f'last_hash: {self.last_hash}, '
                f'hash: {self.hash}, '
                f'data: {self.data}, '
                f')'
                )


def mine_block(last_block: Block, data) -> Block:
    """
    Creates a block given the last block and the given data

    :param last_block: the last Block so that we can get its hash value
    :param data: whatever data is to be put in this block
    :return: a new block to be added to the chain
    """
    timestamp = time.time_ns()
    last_hash = last_block.hash
    hash_ = f'{timestamp}-{last_hash}'

    return Block(timestamp=timestamp, last_hash=last_hash, hash_=hash_, data=data)


def genesis():
    """
    Creates the first block to start the blockchain
    :return: an initial block to start the chain
    """
    return Block(timestamp=1, last_hash='genesis_last_hash', hash_='genesis_hash', data=[])


def main():
    print(f'block.py __name__ : {__name__}')

    genesis_block = genesis()
    block = mine_block(genesis_block, 'first')
    print(block)


if __name__ == '__main__':
    main()
