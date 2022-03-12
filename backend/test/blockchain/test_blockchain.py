import pytest

from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain


def test_blockchain_first_element():
    """
    making sure the first field of the chain is the genesis block
    :return:
    """

    blockchain = Blockchain()
    assert blockchain.chain[0].hash_ == GENESIS_DATA["hash_"]


def test_add_block():
    """
    testing that a new block gets added to the end of the chain with the
    proper last hash
    :return:
    """
    blockchain = Blockchain()
    test_data = "test_data"
    blockchain.add_block(test_data)

    assert blockchain.chain[-1].data == test_data
    assert blockchain.chain[-1].last_hash == GENESIS_DATA["hash_"]


@pytest.fixture
def block_chain_3_blocks():
    """
    creates a blockchain with 3 blocks in it.
    :return: a blockchain with 3 blocks
    """
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain


def test_is_valid_chain(block_chain_3_blocks):
    """
    Test for when a valid blockchain is passed.
    :return:
    """
    Blockchain.is_valid_chain(blockchain=block_chain_3_blocks)


def test_is_valid_chain_bad_genesis(block_chain_3_blocks):
    """
    Test for when a chain with a bad genesis block is passed.  Should throw
    an exception
    :return:
    """
    block_chain_3_blocks.chain[0].hash_ = "evil_hash"
    with pytest.raises(
        Exception, match="Chain does not start with the " "genesis block"
    ):
        Blockchain.is_valid_chain(blockchain=block_chain_3_blocks)


def test_replace_chain(block_chain_3_blocks):
    """
    Making sure a valid blockchain replaces the current one
    :param block_chain_3_blocks: valid blockchain with 3 blocks
    :return:
    """
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain=block_chain_3_blocks)

    assert blockchain.chain == block_chain_3_blocks.chain


def test_replace_chain_too_short(block_chain_3_blocks):
    """
    trying to update blockchain with a shorter blockchain.  Should throw
    exception.
    :param block_chain_3_blocks: valid blockchain with 3 blocks
    :return:
    """
    blockchain = Blockchain()
    with pytest.raises(
        Exception, match="Can not replace chain. New chain " "is not longer"
    ):
        block_chain_3_blocks.replace_chain(blockchain=blockchain)


def test_replace_chain_bad_chain(block_chain_3_blocks):
    """
    trying to update chain with a corrupt chain. Should throw exception
    :param block_chain_3_blocks: valid blockchain with 3 blocks
    :return:
    """
    blockchain = Blockchain()
    block_chain_3_blocks.chain[-1].hash_ = "bad_hash"

    with pytest.raises(Exception):
        blockchain.replace_chain(block_chain_3_blocks)
