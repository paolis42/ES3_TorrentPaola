from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from solucion import decidir
from .models import Registro


# -------------------------------------------------
# ROLES Y PERMISOS
# -------------------------------------------------

def es_admin(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.groups.filter(name="admin").exists()
    )


def puede_crear(user):
    return user.is_authenticated and (
        es_admin(user)
        or user.groups.filter(name="normal").exists()
    )


# -------------------------------------------------
# VALIDACIÓN COMPARTIDA
# -------------------------------------------------

def leer_datos_formulario(request):
    nombre_lugar = request.POST.get("nombre_lugar", "").strip()

    try:
        nivel_interes = int(
            request.POST.get("nivel_interes", "")
        )
        precio = int(
            request.POST.get("precio", "")
        )
        presupuesto = int(
            request.POST.get("presupuesto", "")
        )

    except ValueError:
        return None, (
            "Interés, precio y presupuesto deben ser números enteros."
        )

    if not nombre_lugar:
        return None, "El nombre del lugar es obligatorio."

    if nivel_interes < 1 or nivel_interes > 5:
        return None, "El nivel de interés debe estar entre 1 y 5."

    if precio < 0:
        return None, "El precio no puede ser negativo."

    if presupuesto < 0:
        return None, "El presupuesto no puede ser negativo."

    datos = {
        "nombre_lugar": nombre_lugar,
        "nivel_interes": nivel_interes,
        "precio": precio,
        "presupuesto": presupuesto,
    }

    return datos, None


# -------------------------------------------------
# READ
# -------------------------------------------------

@login_required(login_url="login")
def lista(request):
    registros = Registro.objects.filter(eliminado=False)

    return render(
        request,
        "lista.html",
        {
            "registros": registros,
            "puede_crear": puede_crear(request.user),
            "es_admin": es_admin(request.user),
        }
    )


# -------------------------------------------------
# CREATE
# -------------------------------------------------

@login_required(login_url="login")
def crear(request):

    if not puede_crear(request.user):
        raise PermissionDenied

    error = None

    if request.method == "POST":

        datos, error = leer_datos_formulario(request)

        if error is None:

            resultado, motivo = decidir(
                datos["nivel_interes"],
                datos["precio"],
                datos["presupuesto"],
            )

            Registro.objects.create(
                nombre_lugar=datos["nombre_lugar"],
                nivel_interes=datos["nivel_interes"],
                precio=datos["precio"],
                presupuesto=datos["presupuesto"],
                resultado=resultado,
                motivo=motivo,
            )

            messages.success(
                request,
                "Lugar creado correctamente."
            )

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Crear",
            "error": error,
        }
    )


# -------------------------------------------------
# UPDATE
# -------------------------------------------------

@login_required(login_url="login")
def editar(request, pk):

    if not es_admin(request.user):
        raise PermissionDenied

    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    error = None

    if request.method == "POST":

        datos, error = leer_datos_formulario(request)

        if error is None:

            resultado, motivo = decidir(
                datos["nivel_interes"],
                datos["precio"],
                datos["presupuesto"],
            )

            registro.nombre_lugar = datos["nombre_lugar"]
            registro.nivel_interes = datos["nivel_interes"]
            registro.precio = datos["precio"]
            registro.presupuesto = datos["presupuesto"]
            registro.resultado = resultado
            registro.motivo = motivo

            registro.save()

            messages.success(
                request,
                "Lugar actualizado correctamente."
            )

            return redirect("lista")

    return render(
        request,
        "form.html",
        {
            "accion": "Editar",
            "registro": registro,
            "error": error,
        }
    )


# -------------------------------------------------
# DELETE LÓGICO
# -------------------------------------------------

@login_required(login_url="login")
def eliminar(request, pk):

    if not es_admin(request.user):
        raise PermissionDenied

    registro = get_object_or_404(
        Registro,
        pk=pk,
        eliminado=False
    )

    if request.method == "POST":
        registro.soft_delete()

        messages.success(
            request,
            "Lugar eliminado correctamente."
        )

        return redirect("lista")

    return render(
        request,
        "confirmar.html",
        {
            "registro": registro
        }
    )


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

def iniciar_sesion(request):
    error = None

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
        or ""
    )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            auth_login(request, usuario)

            if (
                next_url
                and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                )
            ):
                return redirect(next_url)

            return redirect("lista")

        error = "Usuario o contraseña incorrectos."

    return render(
        request,
        "login.html",
        {
            "error": error,
            "next": next_url,
        }
    )


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------

@login_required(login_url="login")
@require_POST
def cerrar_sesion(request):
    auth_logout(request)
    return redirect("login")