import io, sweetify, os ,logging
from io import BytesIO
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
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
        sweetify.error(request, 'Algo Salio Mal', timer=8000)
    return redirect('servicio')
     

# cada brigada tiene unidades que a su vez tienen armamento y municiones pueden ver y editar 
# aqui con este codigo muestra el resumen completo de la brigada y puede crear unidades de esas brigada de acuerdo a su id agregado
        
def resumen(request,resumen_id):
    batallon = Brigada.objects.filter(id=resumen_id)
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
    try:
        batallon = Batallones.objects.get(id=unidad_id)
    except ObjectDoesNotExist:
        messages.error(request, "Batallón no encontrado")
        return redirect('servicio')

    servicio = Armas.objects.filter(segundo=batallon)
    municiones = Municiones.objects.filter(tercero=batallon)

    if request.method == 'POST':
        formulario_armas = ArmaForm(request.POST)
        if formulario_armas.is_valid():
            nueva_compania = formulario_armas.save()
            messages.success(request, "Se registró el Arma correctamente")
            return redirect('infor', unidad_id=nueva_compania.segundo.id)
    else:
        formulario_armas = ArmaForm()
    
    if request.method == 'POST':
        formulario_municion = MunicionForm(request.POST)
        if formulario_municion.is_valid():
            nueva_compania = formulario_municion.save()
            messages.success(request, "Se registró la Munición correctamente")
            return redirect('infor', unidad_id=nueva_compania.tercero.id)
        else:
            sweetify.error(request, 'Faltaron campos por rellenar', timer=5000)
    else:
        formulario_municion = MunicionForm()

    context = {
        'batallon': batallon,
        'servicio': servicio,
        'municiones': municiones,
        'formulario_armas': formulario_armas,
        'formulario_municion': formulario_municion,
    }
    return render(request, 'batallon/info.html', context)
    
    
# tabla principal, crear, editar y eliminar personas 
def persona_index(request):
    personas = Personas.objects.all()
    if request.method == 'POST':
       formularios = PersonaForm(request.POST or None, request.FILES or None)
       if formularios.is_valid():
           formularios.save()
           messages.success(request, "Se registro la Persona correctamente")
           return redirect('personas')
       else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=8000)
    else:
        formularios = PersonaForm()
    context = {'personas':personas, 'formulario': formularios}
    return render(request, 'personas/persona_index.html', context) 

def personas_editar(request,personas_id):
    personas = Personas.objects.get(id=personas_id)
    if request.method == 'POST':
        formularios = PersonaForm(request.POST or None, request.FILES or None, instance=personas)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se editó la Persona correctamente")
            return redirect('personas')
        else:
            sweetify.error(request, 'Que paso algo esta Mal, revisa', timer=8000)
    else:
        formularios = PersonaForm(instance=personas)
    context = {'formulario':formularios, 'personas':personas}
    return render(request, 'personas/personas_editar.html', context)

def persona_informacion(request, persona_id):
    person = Personas.objects.get(pk=persona_id)  
    armas = ArmasDePersonas.objects.filter(persona=person)

    if request.method == 'POST':
        formularios = ArmasDePersonasForm(request.POST)  
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registró nuevo armamento asignado correctamente")
            return redirect('informacion', persona_id=person.id)
        else:
           sweetify.error(request, 'Faltaron campos por rellenar', timer=8000)

    else:
        formularios = ArmasDePersonasForm()  # Pre-populate with existing data

    context = {'person': person, 'armas': armas, 'formulario': formularios}
    return render(request, 'personas/persona_informacion.html', context)

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
            serial = formularios.cleaned_data['serial']
            
            if producto.cantidad >= cantidad:
                producto.cantidad -= cantidad
                producto.save()
                ProductoAbastecimiento.objects.create(
                    producto=producto, 
                    abastecimiento=abastecimiento,
                    cantidad=cantidad,
                    serial = serial, 
                    precio= producto.precio,
                    movimiento = producto.nombre)
                sweetify.success(request, 'se envio el paquete correctamente para punto de abastecimiento', timer=7000)
                return redirect('inventario')
            else:
                sweetify.error(request, 'No hay suficientes unidades', timer=8000)
                return redirect('inventario')
            
    else:
        formularios = EnviarProductoForm()
            
    context = {'formulario':formularios, 'producto':producto, 'punto':punto}
    return render(request, 'inventario/inventario_enviar.html', context)

def abastecimiento(request):
    abasto = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = AbastecimientoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registro el abastecimiento correctamente")
            return redirect('abastecimiento')
    else:
        formularios = AbastecimientoForm()
    context = {'abasto':abasto,  'formulario':formularios}
    return render(request, 'abastecimiento/abas_index.html', context)

def abas_info(request, punto_id):
    abastecimiento = Abastecimiento.objects.get(id=punto_id)
    producto = ProductoAbastecimiento.objects.filter(abastecimiento=abastecimiento)
    context = {'producto':producto}
    return render(request, 'abastecimiento/abas_info.html', context)



# PDF IMPRIMIR REPORTES TODOS LOS PDf del MODULO DE PERSONAS, Y BRIGADAS,UNIDADES, MUNICIONES Y ARMAS

def link_callback(uri, rel):
    
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL         
                    mRoot = settings.MEDIA_ROOT       

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

def pdf_uno(request):
    try:
        year = request.GET.get('year', None)
        prueba = Personas.objects.filter(anio=year)
        template = get_template('pdf/pdf_uno.html')
        context = {'prueba': prueba, 'year':year}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except:
        return redirect('personas')
    
def pdf_dos(request, pdf_id):
    try:
        person = Personas.objects.get(pk=pdf_id) 
        armas = ArmasDePersonas.objects.filter(persona=person)
        template = get_template('pdf/pdf_dos.html')
        context = {'person': person, 'armas': armas}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Personas.DoesNotExist:
        messages.error(request, 'Persona no encontrada')
        return redirect('personas')


def pdf_tres(request, pdf_id):
    try:
        person = Batallones.objects.get(pk=pdf_id) 
        armas = Armas.objects.filter(segundo=person)
        template = get_template('pdf/pdf_tres.html')
        context = {'person': person, 'armas': armas}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Batallones.DoesNotExist:
        messages.error(request, 'Armas no encontrada')
        return redirect('Servicio')
    
def pdf_cuatro(request, pdf_id):
    try:
        person = Batallones.objects.get(pk=pdf_id) 
        armas = Municiones.objects.filter(tercero=person)
        template = get_template('pdf/pdf_cuatro.html')
        context = {'person': person, 'armas': armas}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Batallones.DoesNotExist:
        messages.error(request, 'Municiones no encontrada')
        return redirect('Servicio')
    
def pdf_cinco(request, pdf_id):
    try:

        armas = Armas.objects.get(pk=pdf_id)
        person = Batallones.objects.filter(armas=armas)
        template = get_template('pdf/pdf_cinco.html')
        context = {'armas': armas ,
                   'person':person,
                   'icon':'{}{}'.format(settings.STATIC_URL, 'imagenes/imagen1.png')
                   
                   }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Armas.DoesNotExist:
        sweetify.error(request, 'PDF de Armas no Encontrada', timer=8000)
        return redirect('servicio')
    
def pdf_sexto(request, id):
    try:
        municiones = Municiones.objects.get(id=id)
        unidad = Batallones.objects.filter(municiones=municiones)
        template = get_template('pdf/pdf_sexto.html')
        context = {'unidad':unidad, 'municiones':municiones}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

        if pisa_status.err:
            sweetify.error(request, 'Error al generar el PDF', timer=8000)
            return redirect('servicio')
        return response
    
    except Municiones.DoesNotExist:
        sweetify.error(request, 'PDF de Municiones no Encontrada', timer=8000)
        return redirect('servicio')
def pdf_sextimo(request, id):
    try:
        producto = Producto.objects.get(id=id)
        template = get_template('pdf/pdf_sextimo.html')
        context ={'producto':producto}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment: filename="reporte.pdf'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisa_status.err:
            sweetify.error(request, 'Error al generar el PDF', timer=8000)
            return redirect('servicio')
        return response
    except Producto.DoesNotExist:
        sweetify.error(request, 'PDF del Producto no Encontrado', timer=8000)
        return redirect('inventario')
   