import pytest

from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


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
        blockchain.add_block(
            [
                Transaction(
                    sender_wallet=Wallet(), recipient="recipient", amount=i
                ).to_json()
            ]
        )
    return blockchain


def test_is_valid_chain(block_chain_3_blocks: Blockchain):
    """
    Test for when a valid blockchain is passed.
    :return:
    """
    Blockchain.is_valid_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_chain_bad_genesis(block_chain_3_blocks: Blockchain):
    """
    Test for when a chain with a bad genesis block is passed.  Should throw
    an exception
    :return:
    """
    block_chain_3_blocks.chain[0].hash_ = "evil_hash"
    with pytest.raises(
        Exception, match="Chain does not start with the " "genesis block"
    ):
        Blockchain.is_valid_chain(chain=block_chain_3_blocks.chain)


def test_replace_chain(block_chain_3_blocks: Blockchain):
    """
    Making sure a valid blockchain replaces the current one
    :param block_chain_3_blocks: valid blockchain with 3 blocks
    :return:
    """
    blockchain = Blockchain()
    blockchain.replace_chain(chain=block_chain_3_blocks.chain)

    assert blockchain.chain == block_chain_3_blocks.chain


def test_replace_chain_too_short(block_chain_3_blocks: Blockchain):
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
        block_chain_3_blocks.replace_chain(chain=blockchain.chain)


def test_replace_chain_bad_chain(block_chain_3_blocks: Blockchain):
    """
    trying to update chain with a corrupt chain. Should throw exception
    :param block_chain_3_blocks: valid blockchain with 3 blocks
    :return:
    """
    blockchain = Blockchain()
    block_chain_3_blocks.chain[-1].hash_ = "bad_hash"

    with pytest.raises(Exception):
        blockchain.replace_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_transaction_chain_valid_chain(block_chain_3_blocks):
    """
    Testing no exception is raised for valid transaction chain
    :return:
    """
    Blockchain.is_valid_transaction_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_transaction_chain_duplicate_transaction(block_chain_3_blocks):
    """
    Exception should be thrown because a transaction shows up more than once
    in a block
    :return:
    """
    transaction = Transaction(
        sender_wallet=Wallet(), recipient="recipient", amount=12
    ).to_json()
    block_chain_3_blocks.add_block(data=[transaction, transaction])

    with pytest.raises(Exception, match="is not unique"):
        Blockchain.is_valid_transaction_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_transaction_chain_multiple_mining_rewards(block_chain_3_blocks):
    """
    Exception should be thrown if a block has multiple rewards
    :return:
    """
    reward_1 = Transaction.reward_transaction(miner_wallet=Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(miner_wallet=Wallet()).to_json()

    block_chain_3_blocks.add_block(data=[reward_1, reward_2])

    with pytest.raises(
        Exception,
        match="Can only be one mining reward per block.  " "Check block with hash:",
    ):
        Blockchain.is_valid_transaction_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_transaction_chain_bad_transaction(block_chain_3_blocks):
    """
    Exception should be thrown if there is a bad transaction
    :return:
    """
    bad_transaction = Transaction(
        sender_wallet=Wallet(), recipient="recipient", amount=12
    )
    bad_transaction.input["signature"] = Wallet().sign(data=bad_transaction.output)

    block_chain_3_blocks.add_block(data=[bad_transaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(chain=block_chain_3_blocks.chain)


def test_is_valid_transaction_chain_bad_historic_balance(block_chain_3_blocks):
    """
    Exception should be thrown if balance of transaction does not compute
    based on previous blockchain transactions
    :return:
    """
    wallet = Wallet()
    bad_transaction = Transaction(
        sender_wallet=wallet, recipient="recipient", amount=12
    )
    bad_transaction.input[wallet.address] = 9000
    bad_transaction.input["amount"] = 9012
    bad_transaction.output["signature"] = wallet.sign(data=bad_transaction.output)
    block_chain_3_blocks.add_block(data=[bad_transaction.to_json()])

    with pytest.raises(Exception, match="has invalid input amount"):
        Blockchain.is_valid_transaction_chain(chain=block_chain_3_blocks.chain)
