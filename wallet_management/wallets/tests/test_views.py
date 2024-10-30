# test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from uuid import uuid4
from wallets.models import Wallet


class WalletTests(APITestCase):

    def setUp(self):

        self.wallet_uuid = uuid4()
        self.wallet = Wallet.objects.create(uuid=self.wallet_uuid, balance=100)
        self.operation_url = reverse('wallet_operation', kwargs={
                                     'WALLET_UUID': self.wallet_uuid})
        self.balance_url = reverse('wallet_balance', kwargs={
                                   'WALLET_UUID': self.wallet_uuid})

    def test_balance_wallet(self):
        response = self.client.get(self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 100)

    def test_wallet_operation(self):
        operation_data = {
            "amount": 50,
            "operation_type": "credit"
        }
        response = self.client.post(
            self.operation_url, operation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 150)

    def test_invalid_wallet(self):
        invalid_wallet_uuid = uuid4()
        invalid_url = reverse('wallet_balance', kwargs={
                              'WALLET_UUID': invalid_wallet_uuid})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
