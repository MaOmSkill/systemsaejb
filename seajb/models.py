from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import random

#  aqui va las tablas de Brigadas, Batallones y Unidades, Armas de las base de datos del saejb

class Brigada(models.Model):
    code = models.CharField(max_length=100, unique=True)
    nombreB = models.CharField(max_length=100, verbose_name='Brigada')
    ubicacionB = models.CharField(max_length=100, verbose_name='Ubicacion')
    comandante = models.CharField(max_length=100, verbose_name='Comandante')
    telefono = models.CharField(max_length=100, verbose_name='Telefono')
    correo = models.CharField(max_length=100, verbose_name='Correo Electronico')
    fecha = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_code():
        prefix = 'SAEJB' 
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return f'{prefix}{suffix}'
    
    def __str__(self):
        fila ="Brigada:" + self.nombreB + "_" + "Ubicación:" + self.ubicacionB + "_" + "Comandante:" + self.comandante + "_" +  "Telefono:" + self.telefono + "_" + "Correo Electronico:" + self.correo
        return fila
    
    
class Batallones(models.Model):
    nombreB = models.CharField(max_length=100, verbose_name='Unidad')
    ubicacionB = models.CharField(max_length=100, verbose_name='Ubicacion')
    comandante = models.CharField(max_length=100, verbose_name='Comandante')
    telefono = models.CharField(max_length=100, verbose_name='Telefono')
    correo = models.CharField(max_length=100, verbose_name='Correo Electronico')
    fecha = models.DateField(auto_now_add=True)
    primero = models.ForeignKey(Brigada, on_delete=models.CASCADE, blank=True, default=None)
    
    def __str__(self):
        return self.nombreB, self.ubicacionB, self.comandante, self.telefono, self.correo, self.primero

class Armas(models.Model):
    categoria = models.CharField(max_length=300, verbose_name='Categoria:')
    tipoA = models.CharField(max_length=300, verbose_name='Tipo de Armas:')
    modeloA = models.CharField(max_length=300, verbose_name='Modelo de la Armas:')
    calibreA = models.CharField(max_length=300, verbose_name='Calibre de la Armas:')
    serialA = models.CharField(max_length=8000, verbose_name='Serial de la Armas:')
    serialAG = models.CharField(max_length=300, verbose_name='Serial del Asignación:')
    fechaAG = models.DateField(verbose_name='Fecha de Asignación:')
    opAM = models.CharField(max_length=300, verbose_name='Condiciones:')
    cantidadA = models.IntegerField(verbose_name='Armas:')
    cantidadC = models.IntegerField(verbose_name='Cargadores:')
    ac = models.TextField(verbose_name="Accesorio:",null=True)
    armaS = models.CharField(max_length=300, verbose_name='Arma Segundaria:')
    calibreS = models.TextField(verbose_name='Tipo,Modelo,Calibre:',  null=True, default=None)
    serialS = models.TextField(verbose_name='Serial Segundario:',   null=True, blank=True, default=None)
    cantidadS = models.IntegerField(verbose_name='Cantidad Segundario:', null=True, blank=True, default=None)
    fecha = models.DateField(auto_now_add=True)
    segundo = models.ForeignKey(Batallones, on_delete=models.CASCADE, blank=True, default=None)
    
    class Meta:
        verbose_name_plural = "Armas"
        ordering = ['categoria']
        
    def __str__(self):
        return f"{self.categoria} - {self.tipoA} - {self.modeloA}  - {self.calibreA}- {self.serialA}  - {self.serialAG}- {self.opAM}  - {self.cantidadA}- {self.cantidadC}  - {self.armaS} - {self.calibreS} - {self.serialS} - {self.cantidadS}- {self.ac}"
        

class Municiones(models.Model):
    tipoM = models.CharField(max_length=100, verbose_name='Carga Basica')
    serialAG = models.CharField(max_length=100, verbose_name='Serial Asignado')
    fechaAG = models.DateField(verbose_name='Fecha de Asignación')
    cantidadM = models.CharField(max_length=100, verbose_name='Cantidad')
    lote = models.CharField(max_length=100, verbose_name='Lote N°')
    fecha = models.DateField(auto_now_add=True)
    tercero = models.ForeignKey(Batallones, on_delete=models.CASCADE, blank=True, default=None)
    
    def __str__(self):
        return self.tipoM, self.serialAG, self.fechaAG, self.cantidadM, self.lote, self.tercero
    
# aqui va las tablas de Personal con Armamento de las base de datos del saejb   
def validate_year(value):
    if value < 1 or value > 9999:
        raise ValidationError("El año debe estar entre 1 y 9999.")
        
class Personas(models.Model):
    code = models.CharField(max_length=300, unique=True)
    categoria= models.CharField(max_length=300, verbose_name='Categoria:')
    grado = models.CharField(max_length=100, verbose_name='Grado:')
    promocion = models.TextField(null=True, verbose_name='Promoción:')
    anio = models.IntegerField(validators=[validate_year], verbose_name="Año:")
    unidad = models.TextField(null=True, verbose_name='Unidad:')
    datos = models.CharField(max_length=300, verbose_name='Nombres y Apellidos:')
    cedula = models.CharField(max_length=100, verbose_name='Cedula')
    armaA = models.TextField(null=True, verbose_name='Arma de Asignada:')
    cargadores = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Cargadores:")
    municiones = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Carga Basica:")
    serialA = models.CharField(max_length=100, verbose_name='Serial del Arma')
    serialAG = models.CharField(max_length=100, verbose_name='Serial de Asignacion')
    fechaAG = models.DateField(null=True, verbose_name='Fecha de Asignacion')
    direccion = models.TextField(null=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Telefono')
    correo = models.CharField(max_length=100, verbose_name='Correo Electronico')
    img = models.ImageField(upload_to='imagenes/',verbose_name="Imagen", null=True, blank=True, default='imagenes/default.jpg')
    fecha = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generar_unico_codigo()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generar_unico_codigo():
        prefix = 'SAPRS' 
        suffix = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return f'{prefix}{suffix}'
    
    def delete(self, using=None, keep_parents=False):
        self.img.storage.delete(self.img.name)
        super().delete()
    
    def __str__(self):
        return (self.categoria,
                self.grado,
                self.promocion,
                self.anio, 
                self.unidad, 
                self.datos, 
                self.cedula, 
                self.armaA,
                self.cargadores,
                self.municiones,
                self.serialA,
                self.serialAG,
                self.fechaAG,
                self.direccion,
                self.telefono,
                self.correo)

class ArmasDePersonas(models.Model):
    armas = models.CharField(max_length=200, verbose_name="Armas Nuevas")
    modelo = models.CharField(max_length=200, verbose_name="Modelo")
    serial = models.CharField(max_length=200, verbose_name="Serial")
    serialag = models.CharField(max_length=200, verbose_name="Serial de Asignación")
    fechag =  models.CharField(max_length=200, verbose_name="Fecha")
    cargadores =  models.CharField(max_length=200, verbose_name="Cargadores")
    municiones =  models.CharField(max_length=200, verbose_name="Munciones")
    persona = models.ForeignKey(Personas,  on_delete=models.CASCADE, blank=True, default=None)
    def __str__(self):
        return self.armas, self.modelo,self.serial,self.serialag,self.fechag,self.cargadores,self.municiones
    
# aqui digitalizacion de documentos antiguos saejb
class BrigadaDigital(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    fecha_entrada = models.DateField(auto_now_add=True) 
    
    def __str__(self):
        return self.nombre
    
class UnidadDigital(models.Model):
    nombreU = models.CharField(max_length=100 , verbose_name="Unidad")
    descripcion = models.TextField(verbose_name="Descripcion",null=True)
    img = models.ImageField(upload_to='imagenes/',verbose_name="Imagen", null=True)
    fecha_entrada = models.DateField(auto_now_add=True) 
    digital = models.ForeignKey(BrigadaDigital, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombreU, self.descripcion
    
    def delete(self, using=None, keep_parents=False):
        self.img.storage.delete(self.img.name)
        super().delete()
        
#  INVENTARIO saejb

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    serial = models.CharField(max_length=100, verbose_name='Serial')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    descripcion = models.TextField(verbose_name="Descripción", null=True)
    fecha_entrada = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.nombre, self.cantidad, self.descripcion, self.serial, self.modelo
    
    def total(self):
        return self.cantidad * self.precio

class Abastecimiento(models.Model):
    nombre = models.CharField(max_length=255)
    productos = models.ManyToManyField(Producto, through='ProductoAbastecimiento')
    
    def __str__(self):
        return self.nombre

class ProductoAbastecimiento(models.Model):
    movimiento = models.CharField(max_length=200)
    serial = models.TextField(verbose_name="serial", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    abastecimiento = models.ForeignKey(Abastecimiento, on_delete=models.CASCADE)
    fecha_salida = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f'{self.producto.nombre} - {self.producto.precio} - {self.producto.serial}'
    def total(self):
        return self.cantidad * self.precio
    
class Cemanblin(models.Model):
    code = models.CharField(max_length=200, unique=True)
    unidad = models.CharField(max_length=300, verbose_name='Nombre de la Unidad')
    equipo = models.TextField(verbose_name='Equipo', null=True)
    fechaR = models.DateField(auto_now_add=True)
    fechaE = models.DateField(verbose_name='Fecha de Entrega')
    reparado = models.BooleanField(default=False)
    seriales = models.TextField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    personauna = models.CharField(max_length=300, verbose_name='Personas a Firmar')
    personados = models.CharField(max_length=300)
    personatres = models.CharField(max_length=300)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_code():
        prefix = 'CBLIN'
        while True:
            suffix = ''.join(str(random.randint(0, 9)) for _ in range(6))
            code = f'{prefix}{suffix}'
            if not Cemanblin.objects.filter(code=code).exists():
                return code
            
    def __str__(self):
        return f"{self.unidad}, {self.fechaE}, {self.reparado}, {self.seriales}, {self.descripcion}, {self.personauna}, {self.personados}, {self.personatres}, {self.equipo}"
    

    