from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):

    search = request.GET.get('search')

    if search:
        products = Product.objects.filter(
            name__icontains=search
        )
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {
        'products': products
    })
def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart = request.session.get(
        'cart',
        []
    )

    cart_count = sum(
        item.get('quantity', 1)
        for item in cart
    )

    cart_message = request.session.pop(
        'cart_message',
        None
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'cart_count': cart_count,
            'cart_message': cart_message
        }
    )


def add_to_cart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart = request.session.get(
        'cart',
        []
    )

    total_items = sum(
        item.get('quantity', 1)
        for item in cart
    )

    if total_items >= 35:

        request.session[
            'cart_message'
        ] = 'Maximum cart limit reached (35)'

        return redirect(
            'product_detail',
            id=id
        )

    found = False

    for item in cart:

        if item['id'] == product.id:

            if 'quantity' not in item:
                item['quantity'] = 1

            item['quantity'] += 1

            found = True
            break

    if not found:

        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image,
            'quantity': 1
        })

    request.session['cart'] = cart

    request.session[
        'cart_message'
    ] = '✅ Product added to cart'

    return redirect(
        'product_detail',
        id=id
    )


def cart(request):

    cart_items = request.session.get('cart', [])

    total = sum(
        item['price'] * item.get('quantity', 1)
        for item in cart_items
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def user_logout(request):

    logout(request)
    return redirect('home')


def checkout(request):

    request.session['cart'] = []

    return render(request, 'checkout.html')


def remove_from_cart(request, index):

    cart = request.session.get('cart', [])

    if index < len(cart):
        cart.pop(index)

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, index):

    cart = request.session.get('cart', [])

    if index < len(cart):

        if 'quantity' not in cart[index]:
            cart[index]['quantity'] = 1

        cart[index]['quantity'] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, index):

    cart = request.session.get('cart', [])

    if index < len(cart):

        if 'quantity' not in cart[index]:
            cart[index]['quantity'] = 1

        if cart[index]['quantity'] > 1:
            cart[index]['quantity'] -= 1

    request.session['cart'] = cart

    return redirect('cart')


def payment(request):

    cart = request.session.get('cart', [])

    if len(cart) == 0:
        return redirect('home')

    return render(request, 'payment.html')
def buy_now(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    request.session['cart'] = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image,
        'quantity': 1
    }]

    return redirect('payment')


def order_success(request):

    cart = request.session.get('cart', [])

    for item in cart:

        Order.objects.create(

            user=request.user
            if request.user.is_authenticated
            else None,

            product_name=item['name'],

            price=item['price'],

            quantity=item.get('quantity', 1)
        )

    request.session['cart'] = []

    return render(request, 'success.html')
def my_orders(request):

    if request.user.is_authenticated:

        orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')

    else:

        orders = Order.objects.all().order_by(
            '-created_at'
        )

    return render(request, 'my_orders.html', {
        'orders': orders
    })
from django.db.models import Sum
from django.contrib.auth.models import User


def admin_dashboard(request):

    total_products = Product.objects.count()

    total_users = User.objects.count()

    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects.aggregate(
            total=Sum('price')
        )['total']
        or 0
    )

    return render(
        request,
        'admin_dashboard.html',
        {
            'total_products': total_products,
            'total_users': total_users,
            'total_orders': total_orders,
            'total_revenue': total_revenue
        }
    )