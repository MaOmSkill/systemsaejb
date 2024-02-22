import sweetify
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Brigada, Batallones, Armas, Municiones, Personas,Abastecimiento, Producto, Historial
from .forms import BrigadaForm, BatallonForm, ArmaForm, MunicionForm, PersonaForm,AbastecimientoForm, ProductoForm, HistorialForm


# tabla principal editar , eliminar y crear brigadas

def servicio(request):
    servicio = Brigada.objects.all()
    if request.method == 'POST':
       formularios = BrigadaForm(request.POST or None)
       if formularios.is_valid():
           formularios.save()
           messages.success(request, 'El Registro de la Brigada se efectuo con Exito')
           return redirect('servicio')
       else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    else:
        formularios = BrigadaForm() 
    return render(request, 'servicio/index.html', {'servicios':servicio, 'formulario': formularios})

def editar(request,brigada_id):
    elemento = Brigada.objects.get(id=brigada_id)
    if request.method == 'POST':
        form = BrigadaForm(request.POST, instance=elemento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se edito la Brigada con Exito')
            return redirect('servicio')
        else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    
    form = BrigadaForm(instance=elemento)
    context = {'formulario': form}
    return render(request, 'servicio/editar.html', context)


def eliminar(request, id):
    try:
        registro = Brigada.objects.get(id=id)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
    except Brigada.DoesNotExist:
        messages.error(request, "El registro no existe.")
    return redirect('servicio')
     

# cada brigada tiene unidades que a su vez tienen armamento y municiones pueden ver y editar 
# aqui con este codigo muestra el resumen completo de la brigada y puede crear unidades de esas brigada de acuerdo a su id agregado
        
def resumen(request,resumen_id):
    batallon = Brigada.objects.all()
    primero = Brigada.objects.get(id=resumen_id)
    servicio = Batallones.objects.filter(primero = primero)
    datos = Brigada.objects.filter(id=resumen_id)
    if request.method == 'POST':
       formularios = BatallonForm(request.POST or None)
       if formularios.is_valid():
           nueva_compania = formularios.save()
           id = nueva_compania.primero.id
           messages.success(request, "Se registro la Unidad correctamente")
           return redirect('resumen', resumen_id=id)
       else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    else:
        formularios = BatallonForm() 
    return render(request, 'servicio/resumen.html', {'servicios':servicio, 
                                                     'datos':datos , 
                                                     'primero':primero,
                                                     'formulario': formularios, 
                                                     'batallon':batallon})
    


# este codigo puede usted ver la informacion completa de las unidades y registrar armas y municiones
# tambien ver la tabla completa de las armas y municiones registradas que dependen de esa unidad que a su vez depende de una brigada

def info(request, unidad_id):
    entida = Batallones.objects.all()
    segundo = Batallones.objects.get(id=unidad_id)
    tercero= Batallones.objects.get(id=unidad_id)
    servicio = Armas.objects.filter(segundo=segundo)
    ubuntu = Municiones.objects.filter(tercero=tercero)
    datos = Batallones.objects.filter(id = unidad_id)
    
    if request.method == 'POST':
       formularios = ArmaForm(request.POST or None)
       if formularios.is_valid():
           nueva_compania = formularios.save()
           id = nueva_compania.segundo.id
           messages.success(request, "Se registro el Arma correctamente")
           return redirect('infor', unidad_id=id)
    else:
        formularios = ArmaForm()
    
    if request.method == 'POST':
       form = MunicionForm(request.POST or None)
       if form.is_valid():
           nueva_compania = form.save()
           id = nueva_compania.tercero.id
           messages.success(request, "Se registro la Munición correctamente")
           return redirect('infor', unidad_id=id)
       else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    else:
        form = MunicionForm()  
        

    return render(request, 'batallon/info.html', {'segundo':segundo,
                                                  'servicio':servicio, 
                                                  'datos':datos,
                                                  'resumen':ubuntu, 
                                                  'formulario': formularios,
                                                  'form': form,
                                                  'unidad':entida})
    
    
# tabla principal, crear, editar y eliminar personas 
def persona_index(request):
    personas = Personas.objects.all()
    if request.method == 'POST':
       formularios = PersonaForm(request.POST or None)
       if formularios.is_valid():
           formularios.save()
           messages.success(request, "Se registro la Persona correctamente")
           return redirect('personas')
       else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    else:
        formularios = PersonaForm()
    return render(request, 'personas/persona_index.html', {'personas':personas, 'formulario': formularios}) 

def personas_editar(request,personas_id):
    personas = Personas.objects.get(id=personas_id)
    formularios = PersonaForm(request.POST or None, request.FILES or None, instance=personas)
    if formularios.is_valid() and request.method == 'POST':
        formularios.save()
        messages.success(request, "Se editó la Persona correctamente")
        return redirect('personas')
    return render(request, 'personas/personas_editar.html', {'formulario': formularios})

def persona_informacion(request, persona_id):
    registropersona = Personas.objects.filter(id=persona_id)
    return render(request, 'personas/persona_informacion.html', {'registropersona':registropersona})


def pdf(request,pdf_id):
    registros = Personas.objects.get(id=pdf_id)
    response = HttpResponse(content_type='application/pdf')
    
    nombre = registros.cedula
    response['Content-Disposition'] =f'attachment; filename="{nombre}.pdf"'
    
    p = canvas.Canvas(response)
    
    p.setFont("Helvetica", 12)
    p.setFillColorRGB(0.14, 0.59, 0.74)
    p.drawString(100, 100, "aprender esto")
    
    p.showPage()
    p.save()
    return response



#ABASTECIMIENTO VISTAS DE ABASTACIMIENTO CREAR BORRAR, VER, FORMULARIO ENTRE OTROS
def abas_index(request):
    abas = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = AbastecimientoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registro el Abastecimiento correctamente")
            return redirect('abastecimiento')
    else:
        formularios = AbastecimientoForm()
    context = {'abas':abas, 'formulario':formularios}
    return render(request, 'abastecimiento/abas_index.html', context)

def modificar_abas(request, id):
    edicion = Abastecimiento.objects.get(id=id)
    if request.method == 'POST':
        formularios = AbastecimientoForm(request.POST, instance=edicion)
        if formularios.is_valid():
            formularios.save()
            return redirect('abastecimiento')
    else:
        formularios = AbastecimientoForm(instance=edicion)
    return render(request, 'abastecimiento/modificar_abas.html', {'formulario': formularios})

def eliminar_abas(request, id):
    try:
        registro = Abastecimiento.objects.get(id=id)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect('abastecimiento')
    except Brigada.DoesNotExist:
        messages.error(request, "El registro no existe.")
    return redirect('abastecimiento')

def abas_info(request, id):
    abas = Abastecimiento.objects.filter(id=id)
    cuarto = Abastecimiento.objects.get(id=id)
    producto = Producto.objects.filter(cuarto=cuarto)
    
    if request.method == 'POST':
        formularios = ProductoForm(request.POST)
        if formularios.is_valid():
            nuevo_producto = formularios.save()
            id = nuevo_producto.cuarto.id
            return redirect('info', id=id)
    else:
        formularios = ProductoForm()
        
    return render(request, 'abastecimiento/abas_info.html', {'formulario': formularios,'producto': producto, 'abas':abas})

def agregar_historial(request, id):
    producto= Producto.objects.get(id=id)
    if request.method == 'POST':
        formu = HistorialForm(request.POST)
        if formu.is_valid():
            accion = formu.cleaned_data['accion']
            monto = formu.cleaned_data['monto']
            if accion == 'sumar':
                producto.cantidad += monto
            else:
                producto.cantidad -= monto
            producto.save()
            historial = Historial(producto=producto, accion=accion, monto=monto)
            historial.save()
            return redirect(reverse('info', args=[producto.cuarto.id]))
    else:
        formu = HistorialForm()
    return render(request, 'abastecimiento/agregar_historial.html', {'formu': formu, 'producto':producto})

def modificar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        formularios = ProductoForm(request.POST, instance=producto)
        if formularios.is_valid():
            formularios.save()
            return redirect(reverse('info', args=[producto.cuarto.id]))
    else:
        formularios = ProductoForm(instance=producto)
    return render(request, 'abastecimiento/modificar_producto.html', {'formulario': formularios, 'producto':producto})

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('principal')

