import time
from abc import ABC

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pn_config = PNConfiguration()
pn_config.publish_key = "pub-c-97eb77a6-9354-49f5-a545-803eb1878734"
pn_config.subscribe_key = "sub-c-f87a79a8-a3dd-11ec-81c7-420d26494bdd"
pn_config.uuid = "python-blockchain-uuid"
pubnub = PubNub(config=pn_config)

TEST_CHANNEL = "TEST_CHANNEL"


# ABC superclass was added to satisfy the interpreter
# Not totally sure what it is/does
# https://www.geeksforgeeks.org/abstract-base-class-abc-in-python/
class Listener(SubscribeCallback, ABC):
    """"""

    def message(self, pubnub, message):
        """
        Override of message method for our listener
        :param pubnub:
        :param message: the message that is received
        :return:
        """
        print(f"\n --Channel: {message.channel} | Message: {message.message}")


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between nodes in the blockchain
    """

    def __init__(
        self,
    ):
        """Constructor for PubSub"""
        self.pubnub = PubNub(pn_config)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel: str, message):
        """
        publishes the message object to the specified channel
        :param channel: the channel to be published to
        :param message: the message to be published
        :return:
        """
        self.pubnub.publish().channel(channel=channel).message(message=message).sync()


def main():
    pubsub = PubSub()
    # to ensure that our subscription is setup before we send any messages
    time.sleep(1)
    pubsub.publish(channel=TEST_CHANNEL, message={"foo": "bar"})


if __name__ == "__main__":
    main()
