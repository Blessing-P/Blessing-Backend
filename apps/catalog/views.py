# apps/catalog/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Category, Unit
from .serializers import CategorySerializer, UnitSerializer


class CategoryListCreateView(APIView):
    """GET  /api/catalog/categories/          → lista por tipo
       POST /api/catalog/categories/          → crea categoría"""
    permission_classes = [AllowAny]

    def get(self, request):
        # Filtra por tipo si viene ?type=product o ?type=supply
        item_type = request.query_params.get('type')
        qs = Category.objects.all()
        if item_type:
            qs = qs.filter(item_type=item_type)
        return Response(CategorySerializer(qs, many=True).data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    """DELETE /api/catalog/categories/<id>/   → elimina categoría"""
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'detail': 'Categoría no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            # PROTECT en Item.category impide borrar si hay items usando esta categoría
            return Response(
                {'detail': 'No se puede eliminar una categoría que está en uso.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UnitListCreateView(APIView):
    """GET  /api/catalog/units/               → lista todas las unidades
       POST /api/catalog/units/               → crea unidad"""
    permission_classes = [AllowAny]

    def get(self, request):
        units = Unit.objects.all()
        return Response(UnitSerializer(units, many=True).data)

    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnitDetailView(APIView):
    """DELETE /api/catalog/units/<id>/        → elimina unidad"""
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            return None

    def delete(self, request, pk):
        unit = self.get_object(pk)
        if not unit:
            return Response({'detail': 'Unidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            unit.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {'detail': 'No se puede eliminar una unidad que está en uso.'},
                status=status.HTTP_400_BAD_REQUEST,
            )