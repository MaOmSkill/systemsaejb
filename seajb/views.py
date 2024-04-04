import io, sweetify, os ,logging, tempfile
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from .models import Brigada, Batallones, Armas, Municiones, Personas, BrigadaDigital, UnidadDigital, Abastecimiento,  Producto,ProductoAbastecimiento, ArmasDePersonas, Cemanblin, Cemantar, Cemansac
from .forms import BrigadaForm, BatallonForm, ArmaForm, MunicionForm, PersonaForm, BrigadaDigitalForm, UnidadDigitalForm, EnviarProductoForm, ProductoForm, AbastecimientoForm, ArmasDePersonasForm, CemanblinForm, CemantarForm, CemansacForm


@login_required
def principal(request):
    return render(request,'servicio/principal.html')

# tabla principal editar , eliminar y crear brigadas
@login_required
def servicio(request):
    servicio = Brigada.objects.all()
    if request.method == 'POST':
       formularios = BrigadaForm(request.POST or None)
       if formularios.is_valid():
           formularios.save()
           messages.success(request, 'El Registro de la Brigada se efectuo con Exito')
           return redirect('servicio')
       else:
           messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formularios = BrigadaForm()
    context = {'servicios':servicio, 'formulario': formularios}
    return render(request, 'servicio/index.html', context)

@login_required
def editar(request,brigada_id):
    elemento = Brigada.objects.get(id=brigada_id)
    if request.method == 'POST':
        form = BrigadaForm(request.POST or None , instance=elemento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se edito la Brigada con Exito')
            return redirect('servicio')
        else:
           messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    
    form = BrigadaForm(instance=elemento)
    context = {'formulario': form}
    return render(request, 'servicio/editar.html', context)

@login_required
def eliminar(request, id):
    try:
        registro = Brigada.objects.get(id=id)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
    except Brigada.DoesNotExist:
        messages.error(request, 'Algo Salio Mal', timer=8000)
    return redirect('servicio')
     

# cada brigada tiene unidades que a su vez tienen armamento y municiones pueden ver y editar 
# aqui con este codigo muestra el resumen completo de la brigada y puede crear unidades de esas brigada de acuerdo a su id agregado
@login_required  
def resumen(request, resumen_id):
    try:
        primero = Brigada.objects.get(id=resumen_id)
    except Brigada.DoesNotExist:
        messages.error(request, "La Brigada no existe")
        return redirect('servicio')
    servicio = Batallones.objects.filter(primero=primero)

    if request.method == 'POST':
        formularios = BatallonForm(request.POST)
        if formularios.is_valid():
            nueva_compania = formularios.save()
            messages.success(request, "Se registró la Unidad correctamente")
            return redirect('resumen', resumen_id=nueva_compania.primero.id)
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formularios = BatallonForm()
    context = {'servicios': servicio,'primero': primero,'formulario': formularios,}
    return render(request, 'servicio/resumen.html', context)
@login_required
def batallon_edit(request, unidad_id):
    elemento = Batallones.objects.get(id=unidad_id)
    primero = Brigada.objects.get(id=elemento.primero.id)
    
    if request.method == 'POST':
        formularios = BatallonForm(request.POST, instance=elemento)
        if formularios.is_valid():
            nueva_compania = formularios.save()
            messages.success(request, 'Se edito la Unidad con Exito')
            return redirect('resumen', resumen_id=nueva_compania.primero.id)
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    
    formularios = BatallonForm(instance=elemento)
    context = {'formulario': formularios, 'primero': primero}
    return render(request, 'batallon/batallon_edit.html', context)



# este codigo puede usted ver la informacion completa de las unidades y registrar armas y municiones
# tambien ver la tabla completa de las armas y municiones registradas que dependen de esa unidad que a su vez depende de una brigada
@login_required
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
        formulario_municion = MunicionForm(request.POST)

        if formulario_armas.is_valid():
            nueva_compania = formulario_armas.save()
            messages.success(request, "Se registró el Arma correctamente")
            return redirect('infor', unidad_id=nueva_compania.segundo.id)

        if formulario_municion.is_valid():
            nueva_compania = formulario_municion.save()
            messages.success(request, "Se registró la Munición correctamente")
            return redirect('infor', unidad_id=nueva_compania.tercero.id)

        messages.error(request, 'Faltaron campos por rellenar en los Formularios')

    else:
        formulario_armas = ArmaForm()
        formulario_municion = MunicionForm()

    context = {
        'batallon': batallon,
        'servicio': servicio,
        'municiones': municiones,
        'formulario_armas': formulario_armas,
        'formulario_municion': formulario_municion,
    }
    return render(request, 'batallon/info.html', context)
    
@login_required
def armas_edit(request, arma_id):
    elemento = Armas.objects.get(id=arma_id)
    segundo = Batallones.objects.get(id=elemento.segundo.id)
    
    if request.method == 'POST':
        formulario_armas = ArmaForm(request.POST, instance=elemento)
        if formulario_armas.is_valid():
            nueva_comapania = formulario_armas.save()
            messages.success(request, 'Se edito el Formulario de Armamento con Exito')
            return redirect('infor', unidad_id=nueva_comapania.segundo.id)
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formulario_armas = ArmaForm(instance=elemento)
    context = {'formulario_armas': formulario_armas, 'batallon': segundo}
    return  render(request,'batallon/batallon_armas_edit.html', context)
@login_required
def municion_edit(request,  municion_id):
    elemento = Municiones.objects.get(id=municion_id)
    tercero = Batallones.objects.get(id=elemento.tercero.id)
    
    if request.method == 'POST':
        formulario_municion = MunicionForm(request.POST, instance=elemento)
        if formulario_municion.is_valid():
            nueva_comapania = formulario_municion.save()
            messages.success(request, 'Se edito el  Formulario de Munición con Exito')
            return redirect('infor', unidad_id=nueva_comapania.tercero.id)
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formulario_municion = MunicionForm(instance=elemento)
    context = {'formulario_municion':formulario_municion, 'batallon':tercero}
    return render(request, 'batallon/batallon_municion_edit.html',context)
    
# tabla principal, crear, editar y eliminar personas 
@login_required
def persona_index(request):
    personas = Personas.objects.all()
    if request.method == 'POST':
       formularios = PersonaForm(request.POST or None, request.FILES or None)
       if formularios.is_valid():
           formularios.save()
           if 'img' in request.FILES:
                formularios.instance.img = request.FILES['img']
           messages.success(request, "Se registro la Persona correctamente")
           return redirect('personas')
       else:
           messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formularios = PersonaForm()
    context = {'personas':personas, 'formulario': formularios}
    return render(request, 'personas/persona_index.html', context) 

@login_required
def personas_editar(request,personas_id):
    personas = Personas.objects.get(id=personas_id)
    if request.method == 'POST':
        formularios = PersonaForm(request.POST or None, request.FILES or None, instance=personas)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se editó la Persona correctamente")
            return redirect('personas')
        else:
            messages.error(request, 'Que paso algo esta Mal, revisa')
    else:
        formularios = PersonaForm(instance=personas)
    context = {'formulario':formularios, 'personas':personas}
    return render(request, 'personas/personas_editar.html', context)

@login_required
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
           messages.error(request, 'Revisa el Formulario algo salio mal')
    else:
        formularios = ArmasDePersonasForm() 
    context = {'person': person, 'armas': armas, 'formulario': formularios}
    return render(request, 'personas/persona_informacion.html', context)

# digitalización
@login_required
def digital_index(request):
    digitales = BrigadaDigital.objects.all()
    if request.method == 'POST':
        formularios = BrigadaDigitalForm(request.POST or None)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se Registro Correctamente")
            return redirect('digital')
        else:
            messages.error(request, 'Revisa el Formulario algo salio mal')
    else:
        formularios = BrigadaDigitalForm()
    context = {'digitales': digitales, 'formulario': formularios}
    return render(request, 'digital/digital_index.html', context)

@login_required
def digital_info(request, digital_id):
    digital = BrigadaDigital.objects.get(pk=digital_id)
    digitales = UnidadDigital.objects.filter(digital=digital)
    
    if request.method == 'POST':
        formularios = UnidadDigitalForm(request.POST, request.FILES)
        if formularios.is_valid():
            nuevo = formularios.save()
            id = nuevo.digital.id
            messages.success(request, "Se Registro Correctamente")
            return redirect('infodig', digital_id=id)
        else:
            messages.error(request, 'Revisa el Formulario algo salio mal')
    
    else:
        formularios = UnidadDigitalForm()
    context = {'digital': digital, 'digito': digitales, 'formulario': formularios}
    return render(request, 'digital/digital_info.html', context)

#INVENTARIO
@login_required
def inventario_index(request):
    inventario = Producto.objects.all()
    if request.method == 'POST':
        formularios = ProductoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registro el inventario correctamente")
            return redirect('inventario')
        else:
            messages.error(request, 'Revisa el Formulario algo salio mal')
    else:
        formularios = ProductoForm()
    context = {'inventario':inventario, 'formulario':formularios}
    return render(request, 'inventario/inventario_index.html', context) 


@login_required
def inventario_edit(request, in_id):
    inventario = Producto.objects.get(id=in_id)
    if request.method == 'POST':
        formularios = ProductoForm(request.POST or None , instance=inventario)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, 'Se edito el Inventario con Exito')
            return redirect('inventario')
        else:
           messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
       formularios = ProductoForm(instance=inventario)
    context = {'formulario': formularios}
    return render(request, 'inventario/inventario_edit.html', context)

@login_required
def delete(request, id):
    try:
        registro = Producto.objects.get(id=id)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
    except Producto.DoesNotExist:
        messages.error(request, 'Algo Salio Mal', timer=8000)
    return redirect('inventario')

@login_required
def inventario_enviar(request):
    producto = Producto.objects.all()
    punto = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = EnviarProductoForm(request.POST)
        if formularios.is_valid():
            producto_obj = formularios.cleaned_data['producto']
            abastecimiento = formularios.cleaned_data['abastecimiento']
            cantidad = formularios.cleaned_data['cantidad']
            serial = formularios.cleaned_data['serial']
            
            if producto_obj.cantidad >= cantidad:
                producto_obj.cantidad -= cantidad
                producto_obj.save()
                ProductoAbastecimiento.objects.create(
                    producto=producto_obj, 
                    abastecimiento=abastecimiento,
                    cantidad=cantidad,
                    serial=serial, 
                    precio=producto_obj.precio,
                    movimiento=producto_obj.nombre)
                messages.success(request, 'Se envió el paquete correctamente para el punto de abastecimiento')
                return redirect('inventario')
            else:
                messages.error(request, 'No hay suficientes unidades')
                return redirect('inventario') 
    else:
        formularios = EnviarProductoForm()
            
    context = {'formulario': formularios, 'producto': producto, 'punto': punto}
    return render(request, 'inventario/inventario_enviar.html', context)

@login_required
def abastecimiento(request):
    abasto = Abastecimiento.objects.all()
    if request.method == 'POST':
        formularios = AbastecimientoForm(request.POST)
        if formularios.is_valid():
            formularios.save()
            messages.success(request, "Se registró el abastecimiento correctamente")
            return redirect('abastecimiento')
        else:
            messages.error(request, 'Revisa el Formulario algo salio mal')
    else:
        formularios = AbastecimientoForm()

    context = {'abasto': abasto, 'formulario': formularios}
    return render(request, 'abastecimiento/abas_index.html', context)
@login_required
def abas_info(request, punto_id):
    try:
        abastecimiento = Abastecimiento.objects.get(id=punto_id)
    except Abastecimiento.DoesNotExist:
        return render(request, 'abastecimiento')
    
    producto = ProductoAbastecimiento.objects.filter(abastecimiento=abastecimiento)
    context = {'producto': producto}
    return render(request, 'abastecimiento/abas_info.html', context)


# PDF IMPRIMIR REPORTES TODOS LOS PDf del MODULO DE PERSONAS, Y BRIGADAS,UNIDADES, MUNICIONES Y ARMAS

@login_required
def pdf_uno(request):
    try:
        year = request.GET.get('year', None)
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        prueba = Personas.objects.filter(anio=year)
        template = get_template('pdf/pdf_uno.html')
        context = {
                   'prueba': prueba,
                   'year':year,
                   'fecha':fecha,
                   'img_uno':img_uno,
                   'img_dos':img_dos
                   }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('personas')
        return response
    except:
        return redirect('personas')

@login_required  
def pdf_dos(request, pdf_id):
    try:
        person = Personas.objects.get(pk=pdf_id) 
        armas = ArmasDePersonas.objects.filter(persona=person)
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        template = get_template('pdf/pdf_dos.html')
        context = {'person': person, 
                   'armas': armas, 
                   'fecha':fecha,
                   'img_uno':img_uno,
                   'img_dos':img_dos
                   }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Personas.DoesNotExist:
        messages.error(request, 'Persona no encontrada')
        return redirect('personas')

@login_required
def pdf_tres(request, pdf_id):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        brigada = Brigada.objects.get(batallones=pdf_id)
        batallones =Batallones.objects.get(id=pdf_id)
        armas = Armas.objects.filter(segundo=batallones) 
        template = get_template('pdf/pdf_tres.html')
        context = {
                   'brigada':brigada, 
                   'batallones':batallones,
                   'armas':armas, 
                   'fecha':fecha,
                   'img_uno':img_uno,
                   'img_dos':img_dos
                   }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Brigada.DoesNotExist:
        messages.error(request, 'PDF de Brigada no Encontrada')
        return redirect('servicio')
    except Batallones.DoesNotExist:
        messages.error(request, 'PDF de Batallones no Encontrada')
        return redirect('servicio')
    except Armas.DoesNotExist:
        messages.error(request, 'PDF de Armas no Encontrada')
        return redirect('servicio')
  
@login_required
def pdf_cuatro(request, pdf_id):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        brigada = Brigada.objects.get(batallones=pdf_id)
        batallones =Batallones.objects.get(id=pdf_id)
        municion = Municiones.objects.filter(tercero=batallones) 
        template = get_template('pdf/pdf_cuatro.html')
        context = {
                   'brigada':brigada, 
                   'batallones':batallones,
                   'municion':municion, 
                   'fecha':fecha,
                   'img_uno':img_uno,
                   'img_dos':img_dos
                   }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Brigada.DoesNotExist:
        messages.error(request, 'PDF de Brigada no Encontrada')
        return redirect('servicio')
    except Batallones.DoesNotExist:
        messages.error(request, 'PDF de Batallones no Encontrada')
        return redirect('servicio')
    except Municiones.DoesNotExist:
        messages.error(request, 'PDF de Municion no Encontrada')
        return redirect('servicio')
    
@login_required
def pdf_cinco(request, pdf_id):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        armas = Armas.objects.get(pk=pdf_id)
        person = Batallones.objects.filter(armas=armas)
        codigo = Brigada.objects.get(batallones__armas=armas)
        template = get_template('pdf/pdf_cinco.html')
        context = {'armas': armas ,
                   'person':person,
                   'img_uno':img_uno,
                   'img_dos':img_dos,
                   'fecha':fecha,
                   'codigo':codigo
                   
                   }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', extra_tags='alert-danger')
            return redirect('servicio')
        return response
    except Armas.DoesNotExist:
        sweetify.error(request, 'PDF de Armas no Encontrada', timer=8000)
        return redirect('servicio')
    except Brigada.DoesNotExist:
        sweetify.error(request, 'PDF de Brigada no Encontrada', timer=8000)
        return redirect('servicio')
    
@login_required
def pdf_sexto(request, id):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        municiones = Municiones.objects.get(id=id)
        batallones = Batallones.objects.filter(municiones=municiones)
        brigada = Brigada.objects.get(batallones__municiones = municiones)
        template = 'pdf/pdf_sexto.html'
        context = {
                   'batallones':batallones,
                   'municiones':municiones, 
                   'brigada':brigada,
                   'img_uno':img_uno,
                   'img_dos':img_dos,
                   'fecha':fecha,
                   }
        
        template = get_template(template)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF')
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except Municiones.DoesNotExist:
        messages.error(request, 'PDF de Municiones no Encontrada')
        return redirect('servicio')
    except Batallones.DoesNotExist:
        messages.error(request, 'PDF de Batallones no Encontrada')
        return redirect('servicio')
    except Brigada.DoesNotExist:
        messages.error(request, 'PDF de Brigada no Encontrada')
        return redirect('servicio')
    
def pdf_sextimo(request, id):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        producto = Producto.objects.get(id=id)
        template = get_template('pdf/pdf_sextimo.html')
        context ={
                  'producto':producto,
                  'img_uno':img_uno,
                   'img_dos':img_dos,
                   'fecha':fecha,
                  }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment: filename="reporte.pdf'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF')
            return redirect('inventario')
        return response
    except Producto.DoesNotExist:
        messages.error(request, 'PDF del Producto no Encontrado')
        return redirect('inventario')
    
    
def pdf_ocho(request):
    try:
        fecha = datetime.now().date()
        img_uno = settings.STATIC_ROOT + '/imagenes/imagen.png'
        img_dos = settings.STATIC_ROOT + '/imagenes/dos.png'
        producto = Producto.objects.all()
        template = get_template('pdf/pdf_ocho.html')
        context ={
                  'producto':producto,
                  'img_uno':img_uno,
                   'img_dos':img_dos,
                   'fecha':fecha,
                  }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment: filename="reporte.pdf'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            messages.error(request, 'Error al generar el PDF', timer=8000)
            return redirect('inventario')
        return response
    except Producto.DoesNotExist:
        messages.error(request, 'PDF de la Lista de Producto no Encontrado', timer=8000)
        return redirect('inventario')
    
# AQUI ESTAN LOS CENTROS DE REPARACIONES
@login_required
def cemantar(request):
    cemantar = Cemantar.objects.all()
    if request.method == 'POST':
        formulario_cemantar = CemantarForm(request.POST)
        if formulario_cemantar.is_valid():
            formulario_cemantar.save()
            messages.success(request, 'El Registro del Equipo Cemantar se efectuó con Éxito')
            return redirect('cemantar')
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formulario_cemantar = CemantarForm()
    context = {'cemantar': cemantar, 'formulario_cemantar': formulario_cemantar}
    return render(request, 'centros/cemantar_index.html', context)

@login_required
def cemansac(request):
    cemansac = Cemansac.objects.all()
    if request.method == 'POST':
        formulario_cemansac = CemansacForm(request.POST)
        if formulario_cemansac.is_valid():
            formulario_cemansac.save()
            messages.success(request, 'El Registro del Equipo Cemansac se efectuó con Éxito')
            return redirect('cemansac')
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formulario_cemansac = CemansacForm()
    context = {'cemansac': cemansac, 'formulario_cemansac': formulario_cemansac}
    return render(request, 'centros/cemansac_index.html', context)

@login_required
def cemanblin(request):
    cemanblin = Cemanblin.objects.all()
    if request.method == 'POST':
        formulario_cemanblin = CemanblinForm(request.POST)
        if formulario_cemanblin.is_valid():
            formulario_cemanblin.save()
            messages.success(request, 'El Registro del Equipo Cemanblin se efectuó con Éxito')
            return redirect('cemanblin')
        else:
            messages.error(request, 'Faltaron campos por rellenar en el Formulario')
    else:
        formulario_cemanblin = CemanblinForm()
    context = {'cemanblin': cemanblin, 'formulario_cemanblin': formulario_cemanblin}
    return render(request, 'centros/cemanblin_index.html', context)


# USUARIOS Y RESGISTROS Y PERMISOS
from django.contrib.auth.models import User, Permission
from .forms import EditUserForm, RegisterForm, CambioPasswordForm

def usuarios(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # No guarda el usuario todavía
            user.set_password(form.cleaned_data['password']) # Aplica el hash a la contraseña
            user.save() # Ahora guarda el usuario con la contraseña hasheada
            messages.success(request, 'Se Registro Usuario con Éxito')
            return redirect('usuarios')
        else:
            messages.error(request, 'Faltan Campos por Rellenar o la Contraseña no Coinciden')
    else:
        form = RegisterForm()
    context = {'usuarios': usuarios , 'form' : form }
    return render(request, 'usuarios/tabla_user.html', context)


def info_user(request, user_id):
    info_user = get_object_or_404(User, id=user_id)
    permissions = Permission.objects.all() 
    assigned_permissions_ids = info_user.user_permissions.values_list('id', flat=True)
    

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=info_user)
        if form.is_valid():
            form.save()
            selected_permissions_ids = request.POST.getlist('user_permissions')
            selected_permissions = Permission.objects.filter(id__in=selected_permissions_ids)
            info_user.user_permissions.set(selected_permissions)
            messages.success(request, 'Se Actualizo con Éxito')
            return redirect('usuarios')
        else:
            messages.error(request, 'Faltaron campos 2 por rellenar en el Formulario')
    else:
        form = EditUserForm(instance=info_user)
    context = {'info_user': info_user, 'permissions': permissions, 'assigned_permissions_ids': assigned_permissions_ids, 'form': form}
    return render(request, 'usuarios/info_user.html', context)

def cambio_password(request, id):
    cambio = User.objects.get(pk=id)
    if request.method == 'POST':
        formulario = CambioPasswordForm(request.POST)
        if  formulario.is_valid():
            user = formulario.save(commit=False) 
            user.set_password(formulario.cleaned_data['password']) 
            user.save() 
            messages.success(request, 'Se Cambio la Contraseña con Éxito')
            return redirect('usuarios')
        else:
            messages.error(request, 'Faltan Campos 1 por Rellenar o la Contraseña no Coinciden')
    else:
        formulario = CambioPasswordForm()
    context = {'formulario' : formulario, 'cambio':cambio }
    return render(request, 'usuarios/cambio_password.html', context)


def exit(request):
    logout(request)
    return redirect('principal')