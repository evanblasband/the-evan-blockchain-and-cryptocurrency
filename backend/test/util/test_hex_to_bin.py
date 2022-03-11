from backend.utils.hex_to_binary import hex_to_bin


def test_hex_to_bin():
    original_num = 789
    hex_num = hex(original_num)[2:]
    bin_num = hex_to_bin(hex_str=hex_num)

    assert int(bin_num, 2) == original_num
