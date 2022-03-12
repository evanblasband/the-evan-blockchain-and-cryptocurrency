from flask import Flask

app = Flask(__name__)


@app.route("/")
def default():
    return "Welcome to the EBBlockchain"


# @app.route("/blockchain")
# def get_blockchain():
#
#
# @app.route("/mine_block")
# def add_block():


app.run()
