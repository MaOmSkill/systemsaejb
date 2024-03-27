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
    path("batallon/batallon_edit/<int:unidad_id>", views.batallon_edit, name="batallon_edit"),
    path("batallon/batallon_armas_edit/<int:arma_id>", views.armas_edit, name="edit_armas"),
    path("batallon/batallon_municion_edit/<int:municion_id>", views.municion_edit, name="edit_municion"),
    
    # aqui son las rutas de las vistas de personas
    path("personas/persona_index", views.persona_index, name="personas"),
    path("personas/persona_informacion/<int:persona_id>", views.persona_informacion, name="informacion"),
    path("persona/personas_editar/<int:personas_id>", views.personas_editar, name="personas_editar"),
    
    
    # todos los documento generados
    path("pdf/pdf_uno", views.pdf_uno, name="pdf_uno"),
    path("pdf/pdf_dos/<int:pdf_id>", views.pdf_dos, name="pdf_dos"),
    path("pdf/pdf_tres/<int:pdf_id>", views.pdf_tres, name="pdf_tres"),
    path("pdf/pdf_cuatro/<int:pdf_id>", views.pdf_cuatro, name="pdf_cuatro"),
    path("pdf/pdf_cinco/<int:pdf_id>", views.pdf_cinco, name="pdf_cinco"),
    path("pdf/pdf_sexto/<int:id>", views.pdf_sexto, name="pdf_sexto"),
    path("pdf/sextimo/<int:id>", views.pdf_sextimo, name="pdf_sextimo"),
    path("pdf/ocho", views.pdf_ocho, name="pdf_ocho"),
    
    #inventario
    path("inventario/inventario_index", views.inventario_index, name="inventario"),
    path("inventario/inventario_enviar", views.inventario_enviar, name="envio"),
    path("inventario/inventario_edit/<int:in_id>", views.inventario_edit, name="edit_in"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("abastecimiento/abas_index", views.abastecimiento, name="abastecimiento"),
    path("abastecimiento/abas_info/<int:punto_id>", views.abas_info, name="info"),
   
    
     # rutas de digitalización
     path('digital/digital_index', views.digital_index, name='digital'),
     path('digital/digital_info/<int:digital_id>', views.digital_info, name='infodig'),
     
     # rutas de los centros
     path('centros/cemantar_index', views.cemantar, name='cemantar'),
     path('centros/cemansac_index', views.cemansac, name='cemansac'),
     path('centros/cemanblin_index', views.cemanblin, name='cemanblin'),
     
     #login
     path('logout/', views.exit, name='exit'),
     
     
     
      
   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
