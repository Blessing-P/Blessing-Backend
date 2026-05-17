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
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

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

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CustomerSerializer(customer).data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if not customer:
            return Response({'detail': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)