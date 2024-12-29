from store.models import *
from rest_framework import serializers


class productapi(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class categoryapi(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'