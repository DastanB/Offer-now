import json

import pytest
from rest_framework.test import APIClient
from decimal import Decimal

client = APIClient()


@pytest.mark.django_db
def test_transaction():
    balance = Decimal('10000')

    # Wallet creation
    wallet_response = client.post(
        '/wallets/',
        data={
            'label': 'TEST',
            'balance': balance
        }
    )
    assert wallet_response.status_code == 201

    wallet_id = wallet_response.data['id']
    transaction_amount = Decimal('-100.000')
    transaction_response = client.post(
        '/transactions/',
        data={
            "txid": "TEST 1",
            "amount": transaction_amount,
            "wallet": wallet_id
        }
    )
    assert transaction_response.status_code == 201

    wallet_detail_response = client.get(f'/wallets/{wallet_id}/')
    wallet_balance = wallet_detail_response.data.get('balance')

    assert Decimal(wallet_balance) == (balance + transaction_amount)
