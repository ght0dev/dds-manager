from rest_framework import serializers
from .models import Type, Status, Category, Subcategory, Transaction


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, data):
        type_obj = data.get("type") or getattr(self.instance, "type", None)
        category = data.get("category") or getattr(self.instance, "category", None)
        subcategory = data.get("subcategory") or getattr(self.instance, "subcategory", None)
        amount = data.get("amount") or getattr(self.instance, "amount", None)

        errors = {}
        if category and type_obj and category.type_id != type_obj.id:
            errors["category"] = "Категория не принадлежит выбранному типу."
        if subcategory and category and subcategory.category_id != category.id:
            errors["subcategory"] = "Подкатегория не принадлежит выбранной категории."
        if amount is not None and amount <= 0:
            errors["amount"] = "Сумма должна быть положительным числом."
        if errors:
            raise serializers.ValidationError(errors)
        return data
