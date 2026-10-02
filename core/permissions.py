from rest_framework import permissions


class PermisosRegistro(permissions.BasePermission):
    """
    Permisos de la API de GeekMatch Trips:

    viewer:
        puede visualizar.

    normal:
        puede visualizar y crear.

    admin:
        puede visualizar, crear, editar y eliminar.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # GET, HEAD y OPTIONS:
        # cualquier usuario autenticado puede consultar.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superusuario:
        # puede realizar cualquier operación.
        if user.is_superuser:
            return True

        es_admin = user.groups.filter(
            name="admin"
        ).exists()

        es_normal = user.groups.filter(
            name="normal"
        ).exists()

        # POST:
        # admin y normal pueden crear.
        if request.method == "POST":
            return es_admin or es_normal

        # PUT, PATCH y DELETE:
        # solo admin.
        if request.method in (
            "PUT",
            "PATCH",
            "DELETE",
        ):
            return es_admin

        return False