# sales/serializers.py

from rest_framework import serializers
from .models import Sale, SaleItem
from apps.inventory.models import Item


# ── Input ──────────────────────────────────────────────────────────────────────

class SaleItemInputSerializer(serializers.Serializer):
    """Lee los items que vienen del frontend al crear una venta."""
    item_id    = serializers.IntegerField()
    quantity   = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class SaleCreateSerializer(serializers.Serializer):
    """Recibe y valida el payload completo de una nueva venta."""

    # Cliente registrado (opcional — si viene, el view busca el Customer)
    customer_id    = serializers.IntegerField(required=False, allow_null=True)

    # Datos manuales (opcionales si se usa cliente registrado)
    customer_name = serializers.CharField(
    max_length=200,
    required=True,
    allow_blank=False,
    error_messages={
        'required': 'El nombre es obligatorio.',
        'blank': 'El nombre no puede ir vacío.',
    }
)
    telephone = serializers.CharField(
    max_length=20,
    required=True,
    allow_blank=False,
    allow_null=False,
    error_messages={
        'required': 'El teléfono es obligatorio.',
        'blank': 'El teléfono no puede ir vacío.',
        'null': 'El teléfono no puede ser null.',
    }
)
    nit            = serializers.CharField(max_length=20,  required=False, allow_blank=True, allow_null=True)
    address        = serializers.CharField(max_length=300, required=False, allow_blank=True, allow_null=True)
    contact_method = serializers.CharField(max_length=20,  required=False, allow_blank=True, allow_null=True)

    # Nuevos campos del cabezal
    payment_method = serializers.ChoiceField(
    choices=['efectivo', 'transferencia', 'tarjeta'],
    required=True,
    allow_blank=False,
    error_messages={
        'required': 'El método de pago es obligatorio.',
        'blank': 'El método de pago no puede ir vacío.',
        'invalid_choice': 'El método de pago es obligatorio.'
    }
)
    notes          = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    total          = serializers.DecimalField(max_digits=10, decimal_places=2)
    items          = SaleItemInputSerializer(many=True)

    def validate_items(self, items):
        if len(items) == 0:
            raise serializers.ValidationError('La venta debe tener al menos un producto.')
        return items

    def validate(self, data):
        """Si no hay cliente registrado, el nombre es obligatorio."""
        if not data.get('customer_id') and not data.get('customer_name', '').strip():
            raise serializers.ValidationError(
                {'customer_name': 'Ingresa el nombre del cliente o selecciona uno registrado.'}
            )
        return data


# ── Output ─────────────────────────────────────────────────────────────────────



class SaleItemOutputSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    type         = serializers.CharField(source='product.type', read_only=True)

    # Componentes del bundle — lista vacía si es producto simple
    components = serializers.SerializerMethodField()

    class Meta:
        model  = SaleItem
        fields = ['id', 'product', 'product_name', 'type',
                  'quantity', 'unit_price', 'subtotal', 'components']

    def get_components(self, obj):
        if obj.product.type != 'bundle':
            return []
        try:
            return [
                {
                    'name':     detail.item.name,
                    'quantity': detail.quantity,
                }
                for detail in obj.product.bundle.details.select_related('item').all()
            ]
        except Exception:
            return []

class SaleOutputSerializer(serializers.ModelSerializer):
    """Devuelve una venta completa al frontend."""
    items         = SaleItemOutputSerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()  # resuelve nombre registrado o manual

    class Meta:
        model  = Sale
        fields = [
            'id',
            'customer',           # FK id (null si fue manual)
            'customer_name',      # nombre resuelto
            'telephone', 'nit', 'address', 'contact_method',
            'payment_method', 'notes',
            'total', 'items', 'created_at',
        ]

    def get_customer_name(self, obj):
        """Usa el método del modelo para resolver el nombre correcto."""
        return obj.get_customer_name()