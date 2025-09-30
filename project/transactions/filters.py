import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="date__lte")
    status = django_filters.ModelChoiceFilter(field_name="status", queryset=None)
    type = django_filters.ModelChoiceFilter(field_name="type", queryset=None)
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=None)
    subcategory = django_filters.ModelChoiceFilter(field_name="subcategory", queryset=None)

    class Meta:
        model = Transaction
        fields = ["date_from", "date_to", "status", "type", "category", "subcategory"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # lazy import to avoid circular
        from .models import Status, Type, Category, Subcategory

        self.filters["status"].queryset = Status.objects.all()
        self.filters["type"].queryset = Type.objects.all()
        self.filters["category"].queryset = Category.objects.all()
        self.filters["subcategory"].queryset = Subcategory.objects.all()
