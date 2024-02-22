from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #vista principal de las brigadas, eliminar, editar y ver unidades
    path("", views.servicio, name="servicio"),
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
    
    #rutas de abastacimiento nuevo flow
    path('abastecimiento/abas_index', views.abas_index, name='abastecimiento'),
    path('abastecimiento/eliminar_abas/<int:id>', views.eliminar_abas, name='eliminar_abas'),
    path('abastecimiento/abas_info/<int:id>', views.abas_info, name='info'),
    path('abastecimiento/modificar_abas/<int:id>', views.modificar_abas, name='editar_abas'),
    path('abastecimiento/modificar_producto/<int:id>', views.modificar_producto, name='modificar'),
    path('eliminar_producto/<int:id>', views.eliminar_producto, name='eliminar'),
    path('abastecimiento/agregar_historial/<int:id>', views.agregar_historial, name='historial'),
   
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
