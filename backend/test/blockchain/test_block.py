from backend.blockchain.block import GENESIS_DATA, Block


def test_mine_block():
    """
    testing the creation of a blcok and making sure parameters match inputs
    :return:
    """
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block=last_block, data=data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash_
    assert block.hash_[0 : block.difficulty] == "0" * block.difficulty


def test_genesis():
    """
    makes sure the genesis funcitons creates a block with all of the correct
    values
    :return:
    """

    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value
