from store.api.serializer import *
from rest_framework import viewsets
from store.models import *
from rest_framework.authentication import BasicAuthentication
from rest_framework import permissions


class productApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productapi
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

class categoryApiView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categoryapi
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]
    