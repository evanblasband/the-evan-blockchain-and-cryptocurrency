import flask
from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub()
# for i in range(3):
#     blockchain.add_block(data=i)


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
    Adds a new block to the blockchain with the specified data
    :return: the data of the most recently added block in json format
    """
    transaction_data = "stubbed_transaction_data"
    blockchain.add_block(data=transaction_data)

    return jsonify(blockchain.chain[-1].to_json())


app.run()