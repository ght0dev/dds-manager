from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Type, Status, Category, Subcategory, Transaction
from .serializers import *
from .filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("type").all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        type_id = self.request.GET.get("type")
        if type_id:
            qs = qs.filter(type_id=type_id)
        return qs


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.select_related("category").all()
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("status", "type", "category", "subcategory").all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["comment"]
    ordering_fields = ["created_at", "amount"]

    @action(detail=False, methods=["get"])
    def totals(self, request):
        qs = self.filter_queryset(self.get_queryset())
        total = qs.aggregate(total_amount=models.Sum("amount"))["total_amount"] or 0
        return Response({"total": total})


def index(request):
    return render(request, "transactions/list.html")


def transaction_create(request):
    return render(request, "transactions/form.html")


def transaction_edit(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    return render(request, "transactions/form.html", {"transaction": t})
