from django.urls import path
from django.conf.urls import url
from . import views
from .views import OrderSummaryView, navShopView, SellerView, order_list, order_create, order_delete, order_detail, \
    order_edit, add_to_cart, add_to_cart_quick, remove_from_cart, remove_single_produit_from_cart, CheckoutView, \
    AddCouponView

app_name = 'product'

urlpatterns = [

    path('liste', views.product_list, name='indexProduit'),
    path('create/', views.product_create, name='createProduit'),
    path('<int:product_id>/', views.product_detail, name='detailProduit'),
    path('detail/<int:product_id>/', views.view_product, name='viewProduit'),
    #path('edit/<int:product_id>/', views.product_edit, name='editProduit'),
    url(r'(?P<id>\d+)/product_edit/$', views.product_edit, name='editProduit'),
    path('delete/<int:product_id>/', views.product_delete, name='deleteProduit'),

    path('order-summary/', OrderSummaryView, name='order-summary'),
    path('shop/<str:slug>/', navShopView, name='shop'),
    path('seller/', SellerView.as_view(), name='seller'),

    # url Order

    path('order', order_list, name='indexOrder'),
    path('order/create/', order_create, name='createOrder'),
    path('order/<int:order_id>/', order_detail, name='detailOrder'),
    path('order/edit/<int:order_id>/', order_edit, name='editOrder'),
    path('order/delete/<int:order_id>/', order_delete, name='deleteOrder'),

    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-quick/<pk>/', add_to_cart_quick, name='add-to-cart-quick'),

    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('remove-produit-from-cart/<pk>/', remove_single_produit_from_cart,
         name='remove_single_produit_from_cart'),
    path('checkout/', CheckoutView, name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
]
