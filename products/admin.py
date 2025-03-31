from django.contrib import admin
from .models import Category, Cart, CartItem, Order, OrderItem, Product, ProductImage, Payment

# Category modeli uchun
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')  # Ko'rinadigan ustunlar
    search_fields = ('name', 'description')  # Qidiruv oynasi
    list_filter = ('created_at', 'updated_at')  # Filtr bo'yicha qidirish


# Product modeli uchun
class ProductImageInline(admin.TabularInline):  # Rasmni mahsulot sahifasida ko'rsatish
    model = ProductImage
    extra = 3  # Bitta bo'sh rasm maydoni qo'shiladi


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at', 'updated_at')
    inlines = [ProductImageInline]  # Rasm qo'shish uchun ichki forma


# Cart modeli uchun
class CartItemInline(admin.TabularInline):  # CartItem-larni Cart ichida ko'rsatish
    model = CartItem
    extra = 2


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]


# Order modeli uchun
class OrderItemInline(admin.TabularInline):  # OrderItem-larni Order ichida ko'rsatish
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]


# Oddiy OrderItem modeli uchun
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name', 'order__id')


# CartItem modeli uchun
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__user__username')


# ProductImage modeli uchun
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('product__name', 'alt_text')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status')
    search_fields = ('user__username', 'status', 'card')