# customers/serializers.py

from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Sirve tanto para input como para output — el modelo es simple."""

    class Meta:
        model  = Customer
        fields = ['id', 'name', 'telephone', 'nit', 'email', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()