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


pubnub.subscribe().channels([TEST_CHANNEL]).execute()
# Have a sleep so that we can ensure that we are subscribed before any messages
time.sleep(1)


# ABC superclass was added to satisfy the interpreter
# Not totally sure what it is/does
class Listener(SubscribeCallback, ABC):
    """ """

    def message(self, pubnub_, message):
        """
        Override of message method for our listener
        :param pubnub_:
        :param message: the message that is received
        :return:
        """
        print(f"\n --Incoming message: {message}")


pubnub.add_listener(Listener())


def main():
    pubnub.publish().channel(TEST_CHANNEL).message({"foo": "bar"}).sync()


if __name__ == "__main__":
    main()
