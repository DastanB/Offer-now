from rest_framework import serializers
from django.db import transaction

from main.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'
