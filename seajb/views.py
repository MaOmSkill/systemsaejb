import sweetify
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Brigada, Batallones, Armas, Municiones, Personas, BrigadaDigital, UnidadDigital, Abastecimiento,  Producto,ProductoAbastecimiento, ArmasDePersonas
from .forms import BrigadaForm, BatallonForm, ArmaForm, MunicionForm, PersonaForm, BrigadaDigitalForm, UnidadDigitalForm, EnviarProductoForm, ProductoForm, AbastecimientoForm, ArmasDePersonasForm



def principal(request):
    return render(request,'servicio/principal.html')

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
    context = {'servicios':servicio, 'formulario': formularios}
    return render(request, 'servicio/index.html', context)

def editar(request,brigada_id):
    elemento = Brigada.objects.get(id=brigada_id)
    if request.method == 'POST':
        form = BrigadaForm(request.POST or None , instance=elemento)
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
           sweetify.error(request, 'Faltaron campos por rellenar', timer=8000)
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
    
    person = Personas.objects.get(id=persona_id)
    humano = Personas.objects.filter(id=persona_id)
    persona = ArmasDePersonas.objects.filter(persona = person)
    
    if request.method =='POST':
        formularios = ArmasDePersonasForm(request.POST or None)
        if formularios.is_valid():
            persona = formularios.save()
            id = persona.persona.id
            messages.success(request, "Se Registro Nuevo Armamento Asignado correctamente")
            return redirect('informacion', persona_id=id)
        else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=8000)
    else:
        formularios = ArmasDePersonasForm()
    context = {'person':humano, 'formulario':formularios, 'persona':persona}
    return render(request, 'personas/persona_informacion.html', context)



# imprimir reportes de personas 
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

# digitalización

def digital_index(request):
    dital = BrigadaDigital.objects.all()
    if request.method == 'POST':
        formularios = BrigadaDigitalForm(request.POST or None)
        if formularios.is_valid():
            formularios.save()
            return redirect('digital')
    else:
        formularios = BrigadaDigitalForm()
    context = {'digitales': dital, 'formulario': formularios}
    return render(request, 'digital/digital_index.html', context)


    
def digital_info(request,digital_id):
    digital = BrigadaDigital.objects.get(pk=digital_id)
    digitos = UnidadDigital.objects.filter(digital=digital)
    if request.method == 'POST':
        formularios = UnidadDigitalForm(request.POST or None, request.FILES or None)
        if formularios.is_valid():
            nuevo = formularios.save()
            id = nuevo.digital.id
            return redirect('infodig', digital_id=id)
    else:
        formularios = UnidadDigitalForm()
    context = {'digital':digital, 'digito':digitos , 'formulario': formularios}
    return render(request, 'digital/digital_info.html', context)

#INVENTARIO
def inventario_index(request):
    inventario = Producto.objects.all()
    if request.method == 'POST':
        formularios = ProductoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registro el inventario correctamente")
            return redirect('inventario')
    else:
        formularios = ProductoForm()
    context = {'inventario':inventario, 'formulario':formularios}
    return render(request, 'inventario/inventario_index.html', context)    

def inventario_enviar(request):
    producto = Producto.objects.all()
    punto = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = EnviarProductoForm(request.POST)
        if formularios.is_valid():
            producto = formularios.cleaned_data['producto']
            abastecimiento = formularios.cleaned_data['abastecimiento']
            cantidad = formularios.cleaned_data['cantidad']
            
            if producto.cantidad >= cantidad:
                producto.cantidad -= cantidad
                producto.save()
                ProductoAbastecimiento.objects.create(
                    producto=producto, 
                    abastecimiento=abastecimiento,
                    cantidad=cantidad, 
                    movimiento = producto.nombre)
                sweetify.success(request, 'se envio el paquete correctamente para punto de abastecimiento', timer=7000)
                return redirect('inventario')
            else:
                sweetify.error(request, 'No hay suficientes unidades', timer=8000)
                return redirect('principal')
            
    else:
        formularios = EnviarProductoForm()
            
    context = {'formulario':formularios, 'producto':producto, 'punto':punto}
    return render(request, 'inventario/inventario_enviar.html', context)

def abastecimiento(request):
    seña = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = AbastecimientoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registro el abastecimiento correctamente")
            return redirect('abastecimiento')
    else:
        formularios = AbastecimientoForm()
    context = {'seña':seña,  'formulario':formularios}
    return render(request, 'abastecimiento/abas_index.html', context)

def abas_info(request, punto_id):
    abastecimiento = Abastecimiento.objects.get(id=punto_id)
    producto = ProductoAbastecimiento.objects.filter(abastecimiento=abastecimiento)
    context = {'producto':producto}
    return render(request, 'abastecimiento/abas_info.html', context)