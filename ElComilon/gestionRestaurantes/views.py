from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http.response import Http404
from registroDeUsuarios.forms import FormularioUsuario
from core.models import Restaurante, Representante
from django.contrib import messages
from django.db import connection
from django.contrib.auth.models import Group
import cx_Oracle

data = {}

@permission_required('core')
def listarRestaurantes(request):
    global data
    page = request.GET.get('page',1)
    Lista = listado_restaurantes();
    try:
        paginator = Paginator(Lista, 10)
        Lista = paginator.page(page)
    except :
        raise Http404

    data = {
        'entity': Lista,
        'paginator' : paginator,
    }
    return render(request, 'listarRestau_Repre.html', data)

def modificarRepreResta(request, id,id2):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    representante = get_object_or_404(Representante, rutrepresentante=id2)
    dataMod = {
        'seleccion': restaurante,
        'representante': representante
    }
    if request.method == 'POST':
        rutRest = request.POST.get('rutRestaurante').upper()
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()

        rutRepre = request.POST.get('representante').upper()
        nombres = request.POST.get('nombresRepresentante').upper()
        apellidos = request.POST.get('apellidos').upper()
        telefono = request.POST.get('telefono').upper()
      
        ModificarProveedor(rutRest, nombre, direccion)
        modificarRepre(rutRepre, nombres, apellidos, telefono)

        messages.success(request, nombre + " Modificado correctamente")
        return redirect(to="/administracion/listarProveedores")
    return render(request, 'modificarProveedor.html', dataMod)

@permission_required('core')
def EliminarRepreResta(request, id, id2):
    restaurante = get_object_or_404(Restaurante, rutrestaurante=id)
    representante = get_object_or_404(Representante, rutrepresentante=id2)
    restaurante.delete()
    representante.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="/administracion/listarProveedores")

# Create your views here.
@permission_required('core')
def registroProveedor (request):
    data = {
        'form': FormularioUsuario()
    }
    if request.method == 'POST':
        # REPRESENTANTE
        rutRepre = request.POST.get('rutRepre')
        nombresRepre = request.POST.get('nombresRepresentante').upper()
        apellidosRepre = request.POST.get('apellidos').upper()
        telefono = request.POST.get('telefono')
     
        # RESTAURANTE PROVEEDOR
        rutRest = request.POST.get('rutRetaurante')
        nombre = request.POST.get('nombre').upper()
        direccion = request.POST.get('direccion').upper()
        representante =  request.POST.get('rutRepre')
        tipo = 2    
        forumulario = FormularioUsuario(data=request.POST)
        if Restaurante.objects.filter(rutrestaurante=rutRest).exists():
                mensaje = 'Ya existe un Restaurante con este RUT.'
        if Representante.objects.filter(rutrepresentante=rutRepre).exists():
                mensaje2 = 'Ya existe un Representante con este RUT.'
        else:
            mensaje=''
            mensaje2 ='' 
            if forumulario.is_valid():
                user = forumulario.save()
                group = Group.objects.get(name='Proveedor')
                user.groups.add(group)
                registrarRepre(rutRepre,nombresRepre,apellidosRepre,telefono)
                registrarProve(rutRest,nombre,direccion,representante,tipo)
                messages.success(request, nombre + " Registrado correctamente")
                return render (request,'registro-proveedor.html',data)
        data = {
            'form': forumulario,
            'campos': [rutRest,nombre,direccion,telefono,rutRepre,nombresRepre,apellidosRepre,representante],
            'mensajeRut1':mensaje,
            'mensajeRut2':mensaje2,
        }
   
    return render (request,'registro-proveedor.html',data)
    
# REPRESENTANTE
def registrarRepre(rutRepre,nombresRepre,apellidosRepre,telefono):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaRepre = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_REPRESENTANTE",[rutRepre,nombresRepre,apellidosRepre,telefono, salidaRepre])
    return salidaRepre.getvalue()

# RESTAURANTE PROVEEDOR
def registrarProve(rutRest, nombreRest, direccionRest, rutRepresentante, idTipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("REGISTRAR_PROVEEDOR",[rutRest, nombreRest, direccionRest, rutRepresentante, idTipo, salidaPrve])
    return salidaPrve.getvalue()

def listado_restaurantes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_RESTAURANTE", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listado_representante():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("LISTAR_REPRESENTANTES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def ModificarProveedor(rutRest, nombreRest, direccionRest):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_PROVEEDOR", [rutRest, nombreRest, direccionRest, salidaPrve])
    return salidaPrve.getvalue()

def modificarRepre(rutRepre,nombres,apellidos,telefono):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salidaPrve = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("MODIFICAR_REPRESENTANTE",[rutRepre,nombres,apellidos,telefono,salidaPrve])
    return salidaPrve.getvalue()

@permission_required('core')
def restauranteRut(request):
    global data
    if request.method == 'POST':

        rut = request.POST.get('rutRestaurante')

        data = {
        'entity': listarRestauranteRut(rut)   
        }
    return render(request, 'listarRestau_Repre.html', data)


def listarRestauranteRut(rut):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_RESTAURANTE_RUT", [rut, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

