from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from core import views
from core.api_views import RegistroViewSet


router = DefaultRouter()
router.register(
    r"registros",
    RegistroViewSet,
    basename="registro",
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),

    path("registros/", views.lista, name="lista"),
    path("registros/crear/", views.crear, name="crear"),
    path(
        "registros/<int:pk>/editar/",
        views.editar,
        name="editar",
    ),
    path(
        "registros/<int:pk>/eliminar/",
        views.eliminar,
        name="eliminar",
    ),

    path("api/", include(router.urls)),
    path(
        "api/token/",
        obtain_auth_token,
        name="api_token",
    ),
]