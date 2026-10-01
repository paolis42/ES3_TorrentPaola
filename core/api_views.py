from rest_framework import status, viewsets
from rest_framework.response import Response

from solucion import decidir

from .models import Registro
from .serializers import RegistroSerializer


class RegistroViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSerializer

    def get_queryset(self):
        return Registro.objects.filter(
            eliminado=False
        ).order_by("-fecha")

    def perform_create(self, serializer):
        nivel_interes = serializer.validated_data["nivel_interes"]
        precio = serializer.validated_data["precio"]
        presupuesto = serializer.validated_data["presupuesto"]

        resultado, motivo = decidir(
            nivel_interes,
            precio,
            presupuesto,
        )

        serializer.save(
            resultado=resultado,
            motivo=motivo,
        )

    def perform_update(self, serializer):
        nivel_interes = serializer.validated_data.get(
            "nivel_interes",
            serializer.instance.nivel_interes,
        )

        precio = serializer.validated_data.get(
            "precio",
            serializer.instance.precio,
        )

        presupuesto = serializer.validated_data.get(
            "presupuesto",
            serializer.instance.presupuesto,
        )

        resultado, motivo = decidir(
            nivel_interes,
            precio,
            presupuesto,
        )

        serializer.save(
            resultado=resultado,
            motivo=motivo,
        )

    def destroy(self, request, *args, **kwargs):
        registro = self.get_object()

        registro.soft_delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    