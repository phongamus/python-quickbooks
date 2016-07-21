import os
import unittest
from datetime import datetime

from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account
from quickbooks.objects.transfer import Transfer


class TransferTest(unittest.TestCase):
    def setUp(self):
        self.qb_client = QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Transfer {0}".format(self.account_number)

    def test_create(self):
        accounts = Account.filter(Classification='Asset', max_results=2, qb=self.qb_client)
        from_account = accounts[0]
        to_account = accounts[1]

        transfer = Transfer()
        transfer.Amount = 100
        transfer.FromAccountRef = from_account.to_ref()
        transfer.ToAccountRef = to_account.to_ref()

        transfer.save(qb=self.qb_client)

        query_transfer = Transfer.get(transfer.Id, qb=self.qb_client)

        self.assertEquals(query_transfer.Id, transfer.Id)
        self.assertEquals(query_transfer.Amount, 100)
        self.assertEquals(query_transfer.FromAccountRef.value, from_account.Id)
        self.assertEquals(query_transfer.ToAccountRef.value, to_account.Id)
