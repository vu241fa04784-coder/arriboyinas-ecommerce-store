from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('product/<int:id>/',
         views.product_detail,
         name='product_detail'),

    path('add-to-cart/<int:id>/',
         views.add_to_cart,
         name='add_to_cart'),

    path('cart/',
         views.cart,
         name='cart'),

    path('remove-from-cart/<int:index>/',
         views.remove_from_cart,
         name='remove_from_cart'),

    path('register/',
         views.register,
         name='register'),

    path('login/',
         views.user_login,
         name='login'),

    path('logout/',
         views.user_logout,
         name='logout'),

    path('checkout/',
         views.checkout,
         name='checkout'),
         path('increase/<int:index>/',
     views.increase_quantity,
     name='increase_quantity'),

path('decrease/<int:index>/',
     views.decrease_quantity,
     name='decrease_quantity'),
     path('payment/',
     views.payment,
     name='payment'),
     path('payment/',
     views.payment,
     name='payment'),

path('order-success/',
     views.order_success,
     name='order_success'),
     path('my-orders/',
     views.my_orders,
     name='my_orders'),
     path('buy-now/<int:id>/',
     views.buy_now,
     name='buy_now'),
     path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
]