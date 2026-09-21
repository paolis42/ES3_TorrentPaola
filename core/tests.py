from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from solucion import decidir
from .models import Registro


class GeekMatchTests(TestCase):

    def test_decidir_recomendado(self):
        resultado, motivo = decidir(
            nivel_interes=5,
            precio=100,
            presupuesto=500,
        )

        self.assertEqual(resultado, "Recomendado")


    def test_viewer_no_puede_crear(self):
        grupo_viewer = Group.objects.create(name="viewer")

        usuario = User.objects.create_user(
            username="viewer_test",
            password="clave12345"
        )

        usuario.groups.add(grupo_viewer)

        self.client.login(
            username="viewer_test",
            password="clave12345"
        )

        respuesta = self.client.get(
            reverse("crear")
        )

        self.assertEqual(
            respuesta.status_code,
            403
        )


    def test_soft_delete_no_borra_registro(self):
        registro = Registro.objects.create(
            nombre_lugar="Museo Ghibli",
            nivel_interes=5,
            precio=10000,
            presupuesto=20000,
            resultado="Recomendado",
            motivo="Prueba"
        )

        registro.soft_delete()

        registro.refresh_from_db()

        self.assertTrue(registro.eliminado)
        self.assertIsNotNone(
            registro.fecha_eliminacion
        )

        self.assertTrue(
            Registro.objects.filter(
                pk=registro.pk
            ).exists()
        )