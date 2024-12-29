from django.contrib.auth.models import User
from rest_framework import serializers
from .models import BloodDonor
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=BloodDonor.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
        