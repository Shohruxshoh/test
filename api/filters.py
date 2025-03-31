import django_filters
from products.models import Product, ProductImage
class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    class Meta:
        model = Product
        fields = ['category', "price_min", "price_max", 'price']

class ProductImageFilter(django_filters.FilterSet):
    class Meta:
        model = ProductImage
        fields = ['product']