from django.urls import path
from .views import WalletOperationView, WalletBalanceView

urlpatterns = [
    path('<uuid:WALLET_UUID>/operation', WalletOperationView.as_view(), name='wallet_operation'),
    path('<uuid:WALLET_UUID>/', WalletBalanceView.as_view(), name='wallet_balance'),
]
