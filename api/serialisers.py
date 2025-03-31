from rest_framework import serializers
from users.models import User, Profile
from products.models import Category, Product, ProductImage, Cart, CartItem, Order, Payment, OrderItem
from django.shortcuts import get_object_or_404

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "bio", "date_of_birth", "profile_picture", "website"]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', "phone"]
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], 
            password=validated_data['password'],  
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]
        read_only_fields = ("slug",)


# Product
class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'stock']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock']


# Product Image
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', "image", "alt_text"]

class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["product", "image", "alt_text"]

# Cart Items
class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

# Cart 
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'created_at']


# Order
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'items', 'is_paid', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    """Cart dagi barcha mahsulotlarni Order ga o‘tkazish uchun serializer"""
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()

        if not cart_items:
            raise serializers.ValidationError("Cart bo‘sh bo‘lgani uchun buyurtma yaratib bo‘lmaydi!")

        # Buyurtma yaratish
        order = Order.objects.create(
            user=user,
            total_price=sum(item.product.price * item.quantity for item in cart_items)
        )

        # CartItem dan OrderItem yaratish
        order_items = [
            OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Cartni tozalash
        cart.items.all().delete()
        return order


# Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'card', 'status', 'created_at']

class PaymentCreateSerializer(serializers.Serializer):
    card = serializers.CharField(max_length=16)

    def create(self, validated_data):
        user = self.context['request'].user
        order = self.context['order']
        card = validated_data['card']
        payment = Payment.objects.create(user=user, order=order, amount=order.total_price, card=card, status='paid')
        return payment

