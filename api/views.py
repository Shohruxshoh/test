from django.shortcuts import render, get_object_or_404
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, 
                                     ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView,
                                     RetrieveAPIView
                                     )
from users.models import User, Profile
from products.models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem, Payment
from .serialisers import (UserRegisterSerializer, ProfileDetailSerializer, CategorySerializer, 
                          ProductListSerializer, ProductDetailSerializer, ProductImageCreateSerializer, ProductImageSerializer,
                          CartSerializer, CartItemsSerializer, OrderItemSerializer, OrderSerializer, CreateOrderSerializer, 
                          PaymentCreateSerializer, PaymentSerializer
                          )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter, ProductImageFilter
from .paginations import ProductPagination
from drf_spectacular.utils import extend_schema, extend_schema_view
# Create your views here.


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).last()

# Category
class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryCreateApiView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


# Product
class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', "category__name"]
    pagination_class = ProductPagination

class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminUser]

class ProductDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminUser]

# Product Image
class ProductImagesListView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductImageFilter
    pagination_class = ProductPagination

class ProductImageCreateView(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdminUser]

# Cart
class CartView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.filter(user=self.request.user).last()


# Cart Items
class CartItemsView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).last()
        serializer.save(cart=cart)

class CartItemDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemsSerializer
    http_method_names = ["delete"]

# Order
class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    post=extend_schema(
        responses={201: OrderSerializer
        },
        description="Order data",
    ),
)
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data={}, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data)
    
# payment
class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

@extend_schema_view(
    post=extend_schema(
        request=PaymentCreateSerializer,
        responses={201: PaymentSerializer
        },
        description="Order data",
    ),
)
class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, pk=order_id)
        serializer = PaymentCreateSerializer(data=request.data, context={"request": request, "order":order})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data)    
