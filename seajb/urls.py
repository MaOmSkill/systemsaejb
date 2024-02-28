from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #vista principal de las brigadas, eliminar, editar y ver unidades
    path("", views.principal, name="principal"),
    path("servicio/index", views.servicio, name="servicio"),
    path("servicio/editar/<int:brigada_id>", views.editar, name="editar"),
    path("eliminar/<int:id>", views.eliminar, name="eliminar"),
    path("servicio/resumen/<int:resumen_id>", views.resumen, name="resumen"),
    
    #aqui la ruta de los batallones o unidades que tienen armas y municiones
    path("batallon/info/<int:unidad_id>", views.info, name="infor"),
    
    # aqui son las rutas de las vistas de personas
    path("personas/persona_index", views.persona_index, name="personas"),
    path("personas/persona_informacion/<int:persona_id>", views.persona_informacion, name="informacion"),
    path("persona/personas_editar/<int:personas_id>", views.personas_editar, name="personas_editar"),
    
    # todos los documento generados
    path("personas/pdf/<int:pdf_id>", views.pdf, name="pdf"),
    
    #inventario
    path("inventario/inventario_index", views.inventario_index, name="inventario"),
    path("inventario/inventario_enviar", views.inventario_enviar, name="envio"),
    path("abastecimiento/abas_index", views.abastecimiento, name="abastecimiento"),
    path("abastecimiento/abas_info/<int:punto_id>", views.abas_info, name="info"),
    
     # rutas de digitalización
     path('digital/digital_index', views.digital_index, name='digital'),
     path('digital/digital_info/<int:digital_id>', views.digital_info, name='infodig'),
     
      
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
