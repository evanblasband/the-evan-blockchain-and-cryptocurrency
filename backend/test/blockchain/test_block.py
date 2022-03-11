import time

import pytest

from backend.blockchain.block import GENESIS_DATA, Block
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_bin


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


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block=last_block, data="test-data")


def test_is_valid_block(last_block, block):
    """
    Test for a valid block. If this fails an exception will be raised
    :return:
    """
    Block.is_valid_block(last_block=last_block, block=block)


def test_is_valid_block_bad_last_hash(last_block, block):
    """
    Test for a bad last_hash. Should raise an exception
    :return:
    """
    block.last_hash = "bad_hash"

    with pytest.raises(Exception, match="the block's last_hash must be " "correct"):
        Block.is_valid_block(last_block=last_block, block=block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    """
    Test for a when proof of work is not correct. Should raise an exception
    :return:
    """
    block.hash_ = "fff"

    with pytest.raises(Exception, match="Proof of work requirement not met"):
        Block.is_valid_block(last_block=last_block, block=block)


def test_is_valid_block_bad_difficulty_jump(last_block, block):
    """
    Test for a when difficulty changes by more than one. Should raise an
    exception
    :return:
    """
    jump_val = 2
    block.difficulty = last_block.difficulty + jump_val
    block.hash_ = f"{'0' * jump_val}111abc"
    with pytest.raises(Exception, match="Difficulty was changed by more than 1"):
        Block.is_valid_block(last_block=last_block, block=block)


def test_is_valid_block_bad_hash(last_block, block):
    """
    Test for a when restructured hash does not compute to the block.hash_.
    Should raise an
    exception
    :return:
    """
    block.hash_ = "00000000000000000111abc"
    with pytest.raises(Exception, match="The hash value does not compute"):
        Block.is_valid_block(last_block=last_block, block=block)
