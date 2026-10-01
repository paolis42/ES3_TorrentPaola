from rest_framework import serializers

from .models import Registro


class RegistroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registro

        fields = [
            "id",
            "nombre_lugar",
            "nivel_interes",
            "precio",
            "presupuesto",
            "resultado",
            "motivo",
            "fecha",
            "eliminado",
            "fecha_eliminacion",
        ]

        read_only_fields = [
            "resultado",
            "motivo",
            "fecha",
            "eliminado",
            "fecha_eliminacion",
        ]

    def validate_nombre_lugar(self, valor):
        if not valor.strip():
            raise serializers.ValidationError(
                "El nombre del lugar es obligatorio."
            )

        return valor.strip()

    def validate_nivel_interes(self, valor):
        if valor < 1 or valor > 5:
            raise serializers.ValidationError(
                "El nivel de interés debe estar entre 1 y 5."
            )

        return valor

    def validate_precio(self, valor):
        if valor < 0:
            raise serializers.ValidationError(
                "El precio no puede ser negativo."
            )

        return valor

    def validate_presupuesto(self, valor):
        if valor < 0:
            raise serializers.ValidationError(
                "El presupuesto no puede ser negativo."
            )

        return valor
    