import time

from backend.blockchain.block import GENESIS_DATA, Block
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_bin, hex_to_bin2


def test_mine_block():
    """
    testing the creation of a block and making sure parameters match inputs
    :return:
    """
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block=last_block, data=data)

    print(block)
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash_
    assert hex_to_bin(block.hash_)[0 : block.difficulty] == "0" * block.difficulty


def test_genesis():
    """
    makes sure the genesis functions creates a block with all of the correct
    values
    :return:
    """

    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_adjust_difficulty_quickly_mined():
    """
    tests the adjust_difficulty function when a block is mined too fast.
    should increase the difficulty by 1
    :return:
    """
    last_block = Block.mine_block(last_block=Block.genesis(), data="test")
    mined_block = Block.mine_block(last_block=last_block, data="test2")

    assert mined_block.difficulty == last_block.difficulty + 1


def test_adjust_difficulty_slowly_mined():
    """
    tests the adjust_difficulty function when a block is mined too slow.
    should decrease the difficulty by 1
    :return:
    """
    last_block = Block.mine_block(last_block=Block.genesis(), data="test")
    time.sleep(MINE_RATE / SECONDS)  # MINE_RATE is 4B ns so we need to
    # divide be seconds
    mined_block = Block.mine_block(last_block=last_block, data="test2")

    assert mined_block.difficulty == last_block.difficulty - 1


def test_adjust_difficulty_default():
    """
    making sure the adjust block function can never set a negative difficulty
    :return:
    """
    last_block = Block(
        timestamp=time.time_ns(),
        last_hash="test_last_hash",
        data="test_data",
        hash_="test_hash",
        difficulty=1,
        nonce=0,
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block=last_block, data="test2")

    assert mined_block.difficulty == 1
