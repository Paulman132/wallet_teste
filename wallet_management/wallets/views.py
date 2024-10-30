from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import OperationSerializer
from django.db import transaction

class WalletOperationView(APIView):

    def post(self, request, WALLET_UUID):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation_type = serializer.validated_data['operationType']
            amount = serializer.validated_data['amount']

            try:
                with transaction.atomic():
                    wallet = Wallet.objects.get(uuid=WALLET_UUID)
                    if operation_type == 'DEPOSIT':
                        wallet.balance += amount
                    elif operation_type == 'WITHDRAW':
                        if wallet.balance >= amount:
                            wallet.balance -= amount
                        else:
                            return Response({'error': 'Недостаточно средств'}, status=status.HTTP_400_BAD_REQUEST)
                    wallet.save()
                    return Response({'balance': wallet.balance}, status=status.HTTP_200_OK)
            except Wallet.DoesNotExist:
                return Response({'error': 'Кошелек не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletBalanceView(APIView):

    def get(self, request, WALLET_UUID):
        try:
            wallet = Wallet.objects.get(uuid=WALLET_UUID)
            return Response({'balance': wallet.balance}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'error': 'Кошелек не существует'}, status=status.HTTP_404_NOT_FOUND)

