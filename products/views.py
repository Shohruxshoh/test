from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Payment
from django.core.paginator import Paginator
from .forms import PaymentForm
# Create your views here.


# Kategoriyalar ro'yxati
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

# Kategoriya detallari
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

# Mahsulotlar ro'yxati
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 15)  # Har sahifada 15 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/product_list.html', {'products': page_obj})

# Mahsulot detallari
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()
    return render(request, 'products/product_detail.html', {'product': product, 'images': images})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Get the quantity from the request
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is provided
    
    # Create or get the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock < quantity:
        messages.error(request, f"Bizda faqat {product.stock}ta mahsulot qolgan. Iltimoz kamroq buyurtma bering!!!")
        return redirect('product_detail', product.slug)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Update the quantity
    cart_item.quantity += quantity
    cart_item.save()
    messages.success(request, "Mahsulot savatga qo'shildi!")
    return redirect('cart_detail')

# Savat detallari
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart_detail.html', {'cart': cart})


# Savatdagi mahsulotni olib tashlash
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Mahsulot savatdan olib tashlandi!")
    return redirect('cart_detail')


# Buyurtma yaratish
@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, "Savat bo'sh, buyurtma berish uchun mahsulot qo'shing.")
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price * item.quantity
        )
        total_price += item.product.price * item.quantity
        product = get_object_or_404(Product, slug=item.product.slug)
        product.stock = product.stock - item.quantity
        product.save()
    order.total_price = total_price
    order.save()

    # Savatni tozalash
    cart.items.all().delete()
    messages.success(request, "Buyurtmangiz muvaffaqiyatli qabul qilindi!")
    return redirect('payment', order_id=order.id)

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = PaymentForm(data=request.POST)
        if form.is_valid():
            card = form.cleaned_data.get('card')
            payment = Payment.objects.create(user=request.user, order=order, amount=order.total_price, card=card, status='paid')
            order.is_paid = True
            order.save()
            messages.success(request, "To'lov muvaffaqiyatli amalga oshirildi!")
            return redirect('order_detail', order_id=order.id)
    else:
        form = PaymentForm()
    return render(request, 'products/payment.html', {'order':order, "form":form})



# Buyurtma detallari
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_detail.html', {'order': order})

# Foydalanuvchi buyurtmalari ro'yxati
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'products/order_list.html', {'orders': orders})


