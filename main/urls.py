from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('wallets', views.WalletViewSet, basename='wallets')
router.register('transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = router.urls
