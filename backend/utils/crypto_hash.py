import hashlib
import json


def crypto_hash(*args) -> hash:
    """
    Creates a hash for the given arguments
    :param args: the data to make a hash of
    :return: a sha-256 hash for the given data
    """
    # converts all args to a string using json dumps and sorts it
    args_as_str = sorted(map(lambda data: json.dumps(data), args))
    joined_data = "".join(args_as_str)

    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()


def main():
    print(
        f"crypto_hash('test1', 'test2', 'test3'): {crypto_hash('test1', 'test2', 'test3')}"
    )


if __name__ == "__main__":
    main()
