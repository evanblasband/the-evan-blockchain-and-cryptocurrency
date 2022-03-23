from backend.wallet.wallet import Wallet


def test_verify_valid_signature():
    """
    Should pass with a valid signature
    :return:
    """
    data = {"foo": "test-data"}
    wallet = Wallet()
    signature = wallet.sign(data=data)

    assert Wallet.verify(pub_key=wallet.public_key, data=data, signature=signature)


def test_verify_invalid_signature():
    """
    Should return false because of the InvalidSignature exception
    :return:
    """
    data = {"foo": "test-data"}
    wallet = Wallet()
    signature = wallet.sign(data=data)

    assert not Wallet.verify(
        pub_key=Wallet().public_key, data=data, signature=signature
    )
