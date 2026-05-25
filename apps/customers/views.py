# customers/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Customer
from .serializers import CustomerSerializer


class CustomerListCreateView(APIView):
    """GET  /api/customers/       → lista todos los clientes
       POST /api/customers/       → crea un cliente nuevo"""
    permission_classes = [AllowAny]

    def get(self, request):
        customers = Customer.objects.all()
        return Response(CustomerSerializer(customers, many=True).data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerDetailView(APIView):
    """GET    /api/customers/<id>/  → detalle de un cliente
       PUT    /api/customers/<id>/  → edita un cliente
       DELETE /api/customers/<id>/  → elimina un cliente"""
    permission_classes = [AllowAny]

    def _get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self._get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CustomerSerializer(customer).data)

    def put(self, request, pk):
        customer = self._get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        """Activa o desactiva un cliente según el valor de is_active enviado."""
        customer = self._get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        is_active = request.data.get('is_active')
        if is_active is None:
            return Response({'detail': 'El campo is_active es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        customer.is_active = bool(is_active)
        customer.save(update_fields=['is_active'])
        return Response(CustomerSerializer(customer).data)

    def delete(self, request, pk):
        """Elimina permanentemente. Solo permitido si el cliente ya está inactivo."""
        customer = self._get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if customer.is_active:
            return Response(
                {'detail': 'Debes desactivar el cliente antes de eliminarlo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)