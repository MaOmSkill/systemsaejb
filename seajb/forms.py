from django import forms
from .models import Brigada, Batallones, Armas, Municiones, Personas,BrigadaDigital, UnidadDigital, Abastecimiento , Producto, ProductoAbastecimiento, ArmasDePersonas


class BrigadaForm(forms.ModelForm):
    
    nombreB = forms.CharField(min_length=3, max_length=50, required=True)
    
    class Meta:
        model = Brigada
        fields = ['nombreB', 'ubicacionB', 'comandante', 'telefono', 'correo']
        
class BatallonForm(forms.ModelForm):
    nombreB = forms.CharField(min_length=3, max_length=50)
    class Meta:
        model = Batallones
        fields =  ['nombreB',
                   'ubicacionB',
                   'comandante', 
                   'telefono', 
                   'correo',  
                   'primero' ]
         
class ArmaForm(forms.ModelForm):
    
    armaS = forms.CharField(required=False)
    calibreS = forms.CharField(required=False)
    cantidadS = forms.CharField(required=False)
    serialS = forms.CharField(required=False)
    
    class Meta:
        model = Armas
        fields = ['categoria', 
                  'tipoA', 
                  'modeloA', 
                  'calibreA',  
                  'serialA', 
                  'serialAG',
                  'fechaAG',
                  'opAM',
                  'cantidadA',
                  'cantidadC',
                  'segundo',
                  'armaS',
                  'calibreS',
                  'cantidadS',
                  'serialS']
        
class MunicionForm(forms.ModelForm):
    class Meta:
        model = Municiones
        fields = ['tipoM',
                  'serialAG', 
                  'fechaAG',
                  'cantidadM',
                  'lote', 
                  'tercero']
        

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = ['categoria',
                  'grado', 
                  'promocion', 
                  'ano', 
                  'unidad',
                  'datos',
                  'cedula',
                  'armaA',
                  'cargadores',
                  'municiones',
                  'serialA',
                  'serialAG',
                  'fechaAG',
                  'direccion',
                  'telefono', 
                  'correo']
        
class ArmasDePersonasForm(forms.ModelForm):
    class Meta:
        model = ArmasDePersonas
        fields = ['armas' , 'modelo', 'serial', 'serialag', 'fechag', 'cargadores', 'cargadores', 'municiones' , 'persona']
      
class BrigadaDigitalForm(forms.ModelForm):
    class Meta:
        model= BrigadaDigital
        fields = ['nombre']


class UnidadDigitalForm(forms.ModelForm):
    class Meta:
        model= UnidadDigital
        fields =['nombreU','descripcion','img', 'digital']
        
        
        
class EnviarProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoAbastecimiento
        fields = ['producto', 'abastecimiento', 'cantidad']
        
class ProductoForm(forms.ModelForm):
    class Meta: 
        model = Producto
        fields = ['nombre', 'cantidad',  'descripcion', 'serial', 'modelo']
        
class AbastecimientoForm(forms.ModelForm):
    class Meta: 
        model = Abastecimiento
        fields = ['nombre']

    