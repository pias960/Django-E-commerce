
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('productCrud', views.productApiView, basename="productCrud"),
router.register('categoryCrud', views.categoryApiView, basename="categoryCrud")



urlpatterns = [
    path('', include(router.urls)),
]





