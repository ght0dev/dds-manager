from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="categories")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ("name", "type")

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="subcategories")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ("name", "category")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="transactions")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ["-created_at"]

    def clean(self):
        if self.category and self.type and self.category.type_id != self.type_id:
            raise ValidationError({"category": "Категория не принадлежит выбранному типу."})
        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            raise ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({"amount": "Сумма должна быть положительным числом."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_at.date()} | {self.type} | {self.amount}"

