import binascii

from backend.utils.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100",
    "d": "1101",
    "e": "1110",
    "f": "1111",
}


def hex_to_bin(hex_str: str) -> str:
    """
    Given a hex_str string, this function will go over each character and
    convert it to it's binary representation  using the table above.
    :param hex_str: the hex_str sting of the data we want to add to the chain
    :return: a binary string representation of the hex_str string we want to
    add to the chain
    """
    binary_str = ""
    for char in hex_str:
        binary_str += HEX_TO_BINARY_CONVERSION[char]
    return binary_str


def hex_to_bin2(hex_str: str) -> str:
    """
    NOTE: This fails tests for some reason, using above method
    A simpler more pythonic way to convert hex string to binary string

    :param hex_str: the hex_str sting of the data we want to add to the chain
    :return: a binary string representation of the hex_str string we want to
    add to the chain
    """
    binary = bin(int(hex_str, 16))[2:].zfill(4 * len(hex_str))
    return binary


def main():
    number = 451
    hex_number = hex(number)[2:]
    binary_number = hex_to_bin2(hex_number)
    print(f"binary number: {binary_number}")

    original_number = int(binary_number, 2)
    print(f"Original_number: {original_number}")

    hex_to_bin_crypto_hash = hex_to_bin(crypto_hash("test_data"))
    print(f"hex_to_bin_crypto_hash: {hex_to_bin_crypto_hash}")


if __name__ == "__main__":
    main()
