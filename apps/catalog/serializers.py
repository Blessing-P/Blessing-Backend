# apps/catalog/serializers.py

from rest_framework import serializers
from .models import Category, Unit


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'item_type']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Unit
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()