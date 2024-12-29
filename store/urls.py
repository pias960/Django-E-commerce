from django.contrib import admin
from django.urls import path
from . import views
from .views import *



urlpatterns = [
   path('', views.UserHome, name='Uhome'),
   path('about/', views.about, name='about'),
   path('add-to-cart/', views.AddCart, name='addtocart'),
   path('update_quantity/', views.update_quantity, name='update_quantity'),
   path('showcart/', views.showcart, name='showcart'),
   path('cart/', views.cart, name='cart'),
   path('removecart/', views.removecart),
   path('checkout/', views.checkout, name='checkout'),
   path('category/', views.category, name='category'),
   path('categorydet/<int:category_id>/', views.products_by_category, name='products_by_category'),


   path('orders/', views.orders, name='orders'),

   path('product/<slug>/', views.Product_detail_view.as_view(), name='product_details'),
   path('contact/', views.contact, name='contact'),
   path("quantity/", views.update_cart_product_quantity, name="quantity"),



]
