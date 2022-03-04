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
