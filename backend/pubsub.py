import time
from abc import ABC

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

pn_config = PNConfiguration()
pn_config.publish_key = "pub-c-97eb77a6-9354-49f5-a545-803eb1878734"
pn_config.subscribe_key = "sub-c-f87a79a8-a3dd-11ec-81c7-420d26494bdd"
pn_config.uuid = "python-blockchain-uuid"
pubnub = PubNub(config=pn_config)

CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK", "TRANSACTION": "TRANSACTION"}


# ABC superclass was added to satisfy the interpreter
# Not totally sure what it is/does
# https://www.geeksforgeeks.org/abstract-base-class-abc-in-python/
class Listener(SubscribeCallback, ABC):
    """"""

    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool):
        """

        :param blockchain:
        """
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message) -> None:
        """
        Override of message method for our listener
        :param pubnub:
        :param message: the message that is received
        :return:
        """
        print(f"\n --Channel: {message.channel} | Message: {message.message}")

        if message.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message.message)
            temp_chain = self.blockchain.chain[:]
            temp_chain.append(block)

            try:
                self.blockchain.replace_chain(chain=temp_chain)
                self.transaction_pool.clear_blockchain_transaction(
                    blockchain=self.blockchain
                )
                print("\n -- Chain successfully replaced")
            except Exception as e:
                print(f"\n -- Chain was not replaced: {e}")

        elif message.channel == CHANNELS["TRANSACTION"]:
            transaction = Transaction.from_json(transaction_json=message.message)
            self.transaction_pool.set_transaction(transaction=transaction)
            print("\n -- Set the  new transaction in the transaction pool")


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between nodes in the blockchain
    """

    def __init__(self, blockchain: Blockchain, transaction_pool: TransactionPool):
        """Constructor for PubSub"""
        self.pubnub = PubNub(pn_config)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(
            Listener(blockchain=blockchain, transaction_pool=transaction_pool)
        )

    def publish(self, channel: str, message) -> None:
        """
        publishes the message object to the specified channel
        :param channel: the channel to be published to
        :param message: the message to be published
        :return:
        """
        self.pubnub.publish().channel(channel=channel).message(message=message).sync()

    def broadcast_block(self, block: Block) -> None:
        """
        Broadcast a block to all nodes
        :param block: the block to broadcast
        :return:
        """
        self.publish(channel=CHANNELS["BLOCK"], message=block.to_json())

    def broadcast_transaction(self, transaction: Transaction) -> None:
        """
        Broadcast Transaction to all nodes
        :param transaction: transaction to be broadcast
        :return:
        """
        self.publish(channel=CHANNELS["TRANSACTION"], message=transaction.to_json())


def main():
    pubsub = PubSub()
    # to ensure that our subscription is setup before we send any messages
    time.sleep(1)
    pubsub.publish(channel=CHANNELS["TEST"], message={"foo": "bar"})


if __name__ == "__main__":
    main()
