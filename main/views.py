from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from main import models, serializers


# Create your views here.
class WalletViewSet(ModelViewSet):
    queryset = models.Wallet.objects.all()
    serializer_class = serializers.WalletSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['balance']
    search_fields = ['label']
    ordering_fields = ['balance']

    @action(methods=['GET'], detail=True)
    def transactions(self, request, pk) -> Response:
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        wallet = models.Wallet.objects.get(id=pk)
        transactions = wallet.transactions.all()

        queryset = self.filter_queryset(transactions)

        page = paginator.paginate_queryset(queryset, request)
        serializer = serializers.TransactionSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class TransactionViewSet(ModelViewSet):
    queryset = models.Transaction.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['wallet__id']
    search_fields = ['wallet__label', 'txid']
    ordering_fields = ['amount']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TransactionDetailSerializer

        return serializers.TransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            trans = serializer.save()

            wallet = trans.wallet
            new_balance = wallet.balance + trans.amount
            wallet.balance = new_balance
            wallet.save()
