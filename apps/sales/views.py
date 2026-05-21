# sales/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from .models import Sale, SaleItem
from .serializers import SaleCreateSerializer, SaleOutputSerializer
from apps.inventory.models import Item
from apps.customers.models import Customer  # ← nuevo import


class SaleProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Devuelve productos y bundles activos para agregar a una venta."""
        items = Item.objects.filter(
            is_activate=True,
            type__in=['product', 'bundle'],
        ).select_related('category').order_by('-created_at')  # ← agregar

        data = [
            {
                'id':         item.id,
                'name':       item.name,
                'stock':      int(item.stock),
                'min_stock':  int(item.min_stock),
                'sell_price': float(item.sell_price),
                'type':       item.type,
                'image':      request.build_absolute_uri(item.image.url) if item.image else None,
                'category_name': item.category.name if item.category else None,
            }
            for item in items
        ]

        return Response(data)


class SaleListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sales = (
            Sale.objects
            .select_related('customer')                          # nombre del cliente registrado
            .prefetch_related(
                'items__product__bundle__details__item'          # componentes de bundles
            )
            .order_by('-created_at')
        )
        serializer = SaleOutputSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SaleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            with transaction.atomic():

                # ── Cliente registrado (opcional) ──────────────────────────
                customer = None
                customer_id = data.get('customer_id')
                if customer_id:
                    try:
                        customer = Customer.objects.get(id=customer_id)
                    except Customer.DoesNotExist:
                        return Response(
                            {'detail': 'El cliente seleccionado no existe.'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # ── Crear cabezal de venta ─────────────────────────────────
                sale = Sale.objects.create(
                    # cliente
                    customer       = customer,
                    customer_name  = data.get('customer_name') or '',
                    telephone      = data.get('telephone') or '',
                    nit            = data.get('nit') or '',
                    address        = data.get('address') or '',
                    contact_method = data.get('contact_method') or '',
                    # nuevos campos
                    payment_method = data.get('payment_method', 'efectivo'),
                    notes          = data.get('notes') or '',
                    total          = data['total'],
                )

                # ── Crear líneas de detalle ────────────────────────────────
                for item_data in data['items']:
                    item = Item.objects.select_for_update().get(id=item_data['item_id'])

                    if item.stock < item_data['quantity']:
                        return Response(
                            {'detail': f'Stock insuficiente para "{item.name}". Disponible: {item.stock}'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    item.stock -= item_data['quantity']
                    item.save()

                    SaleItem.objects.create(
                        sale       = sale,
                        product    = item,
                        quantity   = item_data['quantity'],
                        unit_price = item_data['unit_price'],
                        subtotal   = item_data['unit_price'] * item_data['quantity'],
                    )

            return Response(
                SaleOutputSerializer(sale).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print('ERROR EN POST SALE:', str(e))
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )