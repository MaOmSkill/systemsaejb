from django import forms
from django.forms import DateInput
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserChangeForm
from .models import Brigada, Batallones, Armas, Municiones, Personas,BrigadaDigital, UnidadDigital, Abastecimiento , Producto, ProductoAbastecimiento, ArmasDePersonas, Cemanblin, Cemantar, Cemansac


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
    
    calibreS = forms.CharField(required=False)
    cantidadS = forms.IntegerField(required=False)
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
                 'serialS', 
                 'ac']
        
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
    
     fechaAG = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))
     
     class Meta:
        model = Personas
        fields = ['categoria',
                  'grado', 
                  'promocion', 
                  'anio', 
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
                  'correo', 'img']
        
        
        def __init__(self, *args, **kwargs):
            super(PersonaForm, self).__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['fechaAG'].widget.attrs['value'] = self.instance.fechaAG.strftime('%Y-%m-%d')
      
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
        fields = ['producto', 'abastecimiento', 'cantidad', 'serial']
        
class ProductoForm(forms.ModelForm):
    class Meta: 
        model = Producto
        fields = ['nombre', 'cantidad',  'descripcion', 'serial', 'modelo' , 'precio']
        
class AbastecimientoForm(forms.ModelForm):
    class Meta: 
        model = Abastecimiento
        fields = ['nombre']
        
class CemanblinForm(forms.ModelForm):
    class Meta:
        model = Cemanblin
        fields = ['fechaE',
                  'reparado',
                  'seriales',
                  'descripcion',
                  'personauna',
                  'personados',
                  'personatres',
                  'equipo',
                  'unidad']
        
class CemantarForm(forms.ModelForm):
    class Meta:
        model = Cemantar
        fields = ['fechaE',
                  'reparado',
                  'seriales',
                  'descripcion',
                  'personauna',
                  'personados',
                  'personatres',
                  'equipo',
                  'unidad']
class CemansacForm(forms.ModelForm):
    class Meta:
        model = Cemansac
        fields = ['fechaE',
                  'reparado',
                  'seriales',
                  'descripcion',
                  'personauna',
                  'personados',
                  'personatres',
                  'equipo',
                  'unidad']       
        
class EditUserForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser' ,'user_permissions' ]
        exclude = ('user_permissions',)
        
   
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name= forms.CharField(max_length=100,label="Apellido")

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password', 'password1']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas no coinciden")

class CambioForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['password', 'password1']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        
class RegistroForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    is_active = forms.BooleanField(required=False, initial=True)
    is_superuser = forms.BooleanField(required=False, initial=True)
    is_staff = forms.BooleanField(required=False, initial=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','is_active', 'is_staff', 'is_superuser' ,'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
    def clean_checkbox(self):
        is_active = self.cleaned_data.get('checkbox')
        # Convert 'on' to True, and any other value to False
        return is_active == 'on'
 