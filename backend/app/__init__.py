import os
import random

import flask
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet

app = Flask(__name__)
CORS(app=app, resources={r"/*": {"origins": "http://localhost:3000"}})
blockchain = Blockchain()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain=blockchain, transaction_pool=transaction_pool)
wallet = Wallet(blockchain=blockchain)


@app.route("/")
def route_default() -> str:
    """
    the homepage for the blockchain
    :return:
    """
    return "Welcome to the EBBlockchain"


@app.route("/blockchain")
def route_get_blockchain() -> flask.Response:
    """
    route for getting the blockchain data
    :return: returns the blockchain list as json
    """
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine() -> flask.Response:
    """
    Adds a new block to the blockchain with the specified data then removes
    it from the transaction pool
    :return: the data of the most recently added block in json format
    """
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(
        Transaction.reward_transaction(miner_wallet=wallet).to_json()
    )
    blockchain.add_block(data=transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block=block)
    transaction_pool.clear_blockchain_transaction(blockchain=blockchain)

    return jsonify(block.to_json())


@app.route("/wallet/transact", methods=["POST"])
def route_wallet_transact():
    """
    Route for creating a new transaction, caller will post json data
    containing the recipient and the amount
    :return:
    """
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    if transaction:  # If transaction already exists just update it
        transaction.update_transaction(
            sender_wallet=wallet,
            recipient=transaction_data["recipient"],
            amount=transaction_data["amount"],
        )
    else:  # If a transaction from this address doesn't exist
        transaction = Transaction(
            sender_wallet=wallet,
            recipient=transaction_data["recipient"],
            amount=transaction_data["amount"],
        )

    pubsub.broadcast_transaction(transaction=transaction)

    print(f"transaction.to_json: {transaction.to_json()}")
    return jsonify(transaction.to_json())


@app.route("/wallet/info")
def route_wallet_info():
    """
    Access the wallet info associated with this application
    :return: a json string with the wallet address and the balance
    """
    return jsonify({"address": wallet.address, "balance": wallet.balance})


@app.route("/blockchain/range")
def route_blockchain_range():
    """
    Route for only querying part of the blockchain
    :return: will return a json list in reverse order from [start] block to
    [end] block
    """
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))

    # [::-1] reverses a list, we do this to see the most recent blocks
    # instead of the oldest blocks
    return jsonify(blockchain.to_json()[::-1][start:end])


@app.route("/blockchain/length")
def route_blockchain_length():
    """
    Gets the length of the blockchain.
    :return: int of length of blockchain
    """
    return jsonify(len(blockchain.chain))


# Need to enable other nodes to run on different ports
ROOT_PORT = 5000
PORT = ROOT_PORT
# check for environment variable
if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)
    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(chain=result_blockchain.chain)
        print("\n -- Successfully synchronized local chain")
    except Exception as e:
        print(f"\n -- Error synchronizing chain: {e}")

if os.environ.get("SEED_DATA"):
    for i in range(10):
        blockchain.add_block(
            data=[
                Transaction(
                    sender_wallet=Wallet(),
                    recipient=Wallet().address,
                    amount=random.randint(2, 50),
                ).to_json(),
                Transaction(
                    sender_wallet=Wallet(),
                    recipient=Wallet().address,
                    amount=random.randint(2, 50),
                ).to_json(),
            ]
        )


app.run(port=PORT)
