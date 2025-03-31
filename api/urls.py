from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (RegisterView, ProfileDetailView, CategoryListApiView, CategoryDetailApiView, CategoryCreateApiView,
                    ProductCreateApiView, ProductDetailApiView, ProductListApiView, ProductImageCreateView, ProductImagesListView,
                    CartView, CartItemsView, CartItemDeleteView, OrderListAPIView, OrderDetailAPIView, CreateOrderView,
                    PaymentCreateAPIView, PaymentListAPIView
                    )

urlpatterns = [
    # login and register
    path('register/', RegisterView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    
    # Profile
    path('profile/', ProfileDetailView.as_view(), name="profile"),

    # Category
    path('categories/', CategoryListApiView.as_view(), name="categories"),
    path('categories/create/', CategoryCreateApiView.as_view(), name="categories-create"),
    path('categories/<int:pk>', CategoryDetailApiView.as_view(), name="categories-detail"),

    # Product
    path('products/', ProductListApiView.as_view(), name='products'),
    path('products/create/', ProductCreateApiView.as_view(), name='products-create'),
    path('products/<int:pk>', ProductDetailApiView.as_view(), name='products-detail'),

    # Product Image
    path('products-images/', ProductImagesListView.as_view(), name='products'),
    path('products-image/create/', ProductImageCreateView.as_view(), name='products-create'),

    # Cart
    path('cart/', CartView.as_view(), name='cart'),

    # Cart Items
    path('cart-items/create/', CartItemsView.as_view(), name='cart-items-create'),
    path('cart-items/delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-items-delete'),

    # Order
    path('orders/', OrderListAPIView.as_view(), name='orders'),
    path('orders-create/', CreateOrderView.as_view(), name='orders-create'),
    path('orders/<int:pk>', OrderDetailAPIView.as_view(), name='order-detail'),

    # Payment
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('payment-create/<int:order_id>/', PaymentCreateAPIView.as_view(), name='payments-create'),
    
]
