from steem import Steem
from steem.transactionbuilder import TransactionBuilder
from steembase import operations

from .actions.heist import Heist
from .datastructures import Transaction


class Heisenberg:
    """
    The core class to interact with the Drugwars game.
    All in-game actions can be created with a Heisenberg instance.

    Example:

        This invests 420 ingame DRUGs to the daily heist.

        ```
        from heisenberg.core import Heisenberg

        h = Heisenberg(
            'username',
            'posting_key'
        )
        h.heist(420)
    """

    def __init__(self, account, private_posting_key):
        self.account = account
        self.private_posting_key = private_posting_key
        self.steem = Steem(
            nodes=["https://api.steemit.com"],
            keys=[private_posting_key])

    def heist(self, amount):
        """Create an "invest to heist" action and broadcast it
        to the STEEM network.

        :param amount (str): The amount of drugs to invest
        :return (Transaction): Transaction data
        """
        heist = Heist(self.account, amount)
        return self.broadcast(heist)

    def broadcast(self, action):
        """ Broadcasts the action to the STEEM network.

        It uses `broadcast_transaction_synchronous` method of steemd which
        actually gives transaction details. (ID, block_num.)

        :param action (Action): Action object
        :return (Transaction): Transaction data
        """
        ops = [
            operations.CustomJson(**action.to_transaction()),
        ]
        tb = TransactionBuilder(steemd_instance=self.steem)
        tb.appendOps(ops)
        tb.appendSigner(self.account, "posting")
        tb.sign()
        response = self.steem.broadcast_transaction_synchronous(tb.json())
        return Transaction(response.get("id"), response.get("block_num"))