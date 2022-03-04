from backend.utils.crypto_hash import crypto_hash


def test_input_types_and_order():
    """
    Should create the same hash_ for any input types in any order
    :return:
    """
    assert crypto_hash(1, [2], "three") == crypto_hash([2], "three", 1)


def test_congruency():
    """
    testing to make sure the same value is always computed
    :return:
    """
    assert (
        crypto_hash("test")
        == "4d967a30111bf29f0eba01c448b375c1629b2fed01cdfcc3aed91f1b57d5dd5e"
    )
