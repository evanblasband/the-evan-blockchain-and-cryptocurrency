import time

import requests

from backend.wallet.wallet import Wallet

BASE_URL = "http://localhost:5000"


def get_blockchain() -> dict:
    """
    Gets the current blockchain for the local host
    :return: the json representation of the blockchain
    """
    return requests.get(f"{BASE_URL}/blockchain").json()


def get_blockchain_mine() -> dict:
    """
    Calls the route to mine a block
    :return: the json representation of the block that was just mined
    """
    return requests.get(f"{BASE_URL}/blockchain/mine").json()


def post_wallet_transact(recipient: str, amount: int) -> dict:
    """
    Creates post request to make a transaction
    :param recipient: the recipient to transact with
    :param amount: the amount to send
    :return: the json representation of the transaction data
    """
    return requests.post(
        url=f"{BASE_URL}/wallet/transact",
        json={"recipient": recipient, "amount": amount},
    ).json()


def get_wallet_info() -> dict:
    """
    Get the info for the applicaiotn wallet
    :return: a dictionary with the address and balance of the wallet
    """
    return requests.get(f"{BASE_URL}/wallet/info").json()


start_blockchain = get_blockchain()
print(f"start_blockchain: {start_blockchain}")

recipient = Wallet().address

post_wallet_transact_1 = post_wallet_transact(recipient=recipient, amount=12)
print(f"post_wallet_transact_1: {post_wallet_transact_1}")

time.sleep(1)
post_wallet_transact_2 = post_wallet_transact(recipient=recipient, amount=20)
print(f"post_wallet_transact_2: {post_wallet_transact_2}")


time.sleep(1)
mine_block = get_blockchain_mine()
print(f"\n mine_block: {mine_block}")


wallet_info = get_wallet_info()
print(f"\n wallet_info: {wallet_info}")
