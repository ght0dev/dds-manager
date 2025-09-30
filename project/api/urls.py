from rest_framework import routers
from django.urls import path, include
from transactions.views import *

router = routers.DefaultRouter()
router.register("types", TypeViewSet)
router.register("statuses", StatusViewSet)
router.register("categories", CategoryViewSet)
router.register("subcategories", SubcategoryViewSet)
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
