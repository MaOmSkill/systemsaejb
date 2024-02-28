from django.db import models
from django.utils import timezone
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
    categoria = models.CharField(max_length=100, verbose_name='Categoria')
    tipoA = models.CharField(max_length=100, verbose_name='Tipo')
    modeloA = models.CharField(max_length=100, verbose_name='Modelo')
    calibreA = models.CharField(max_length=100, verbose_name='Calibre')
    serialA = models.CharField(max_length=100, verbose_name='Serial')
    serialAG = models.CharField(max_length=100, verbose_name='Serial del Asignación')
    fechaAG = models.CharField(max_length=100, verbose_name='Fecha de Asignación')
    opAM = models.CharField(max_length=100, verbose_name='Optimo')
    cantidadA = models.CharField(max_length=100, verbose_name='Armas')
    cantidadC = models.CharField(max_length=100, verbose_name='Cargadores')
    armaS  = models.CharField(max_length=100, verbose_name='Arma Segundaria')
    calibreS = models.CharField(max_length=100,   verbose_name='Calibre Segundario',  null=True)
    serialS = models.CharField(max_length=100,    verbose_name='Serial Segundario',   null=True)
    cantidadS = models.CharField(max_length=100,  verbose_name='Cantidad Segundario', null=True)
    fecha = models.DateField(auto_now_add=True)
    segundo = models.ForeignKey(Batallones, on_delete=models.CASCADE, blank=True, default=None)
    
    def __str__(self):
        return (self.categoria,
                self.tipoA,
                self.modeloA,
                self.calibreA,
                self.serialA,
                self.serialAG,
                self.fechaAG,
                self.opAM,
                self.cantidadA,
                self.cantidadC,
                self.segundo,
                self.armaS,
                self.calibreS,
                self.cantidadS,
                self.serialS)
        

class Municiones(models.Model):
    tipoM = models.CharField(max_length=100, verbose_name='Carga Basica')
    serialAG = models.CharField(max_length=100, verbose_name='Serial Asignado')
    fechaAG = models.CharField(max_length=100, verbose_name='Fecha de Asignación')
    cantidadM = models.CharField(max_length=100, verbose_name='Cantidad')
    lote = models.CharField(max_length=100, verbose_name='Lote N°')
    fecha = models.DateField(auto_now_add=True)
    tercero = models.ForeignKey(Batallones, on_delete=models.CASCADE, blank=True, default=None)
    
    def __str__(self):
        return self.tipoM, self.serialAG, self.fechaAG, self.cantidadM, self.lote, self.tercero
    
# aqui va las tablas de Personal con Armamento de las base de datos del saejb   

class Personas(models.Model):
    code = models.CharField(max_length=100, unique=True)
    categoria= models.CharField(max_length=100, verbose_name='Categoria')
    grado = models.CharField(max_length=100, verbose_name='Grado')
    promocion = models.CharField(max_length=100, verbose_name='Promoción')
    ano = models.CharField(max_length=100, verbose_name='Año')
    unidad = models.CharField(max_length=100, verbose_name='Unidad')
    datos = models.CharField(max_length=100, verbose_name='Nombres y Apellidos')
    cedula = models.CharField(max_length=100, verbose_name='Cedula')
    armaA = models.CharField(max_length=100, verbose_name='Arma de Asignada')
    cargadores = models.CharField(max_length=100, verbose_name='Cargadores')
    municiones = models.CharField(max_length=100, verbose_name='Municiones')
    serialA = models.CharField(max_length=100, verbose_name='Serial del Arma')
    serialAG = models.CharField(max_length=100, verbose_name='Serial de Asignacion')
    fechaAG = models.CharField(max_length=100, verbose_name='Fecha de Asignacion')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=100, verbose_name='Telefono')
    correo = models.CharField(max_length=100, verbose_name='Correo Electronico')
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

    def __str__(self):
        return (self.categoria,
                self.grado,
                self.promocion,
                self.ano, 
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
    
    def __str__(self):
        return self.nombre, self.cantidad, self.descripcion, self.serial, self.modelo

class Abastecimiento(models.Model):
    nombre = models.CharField(max_length=255)
    productos = models.ManyToManyField(Producto, through='ProductoAbastecimiento')
    
    def __str__(self):
        return self.nombre

class ProductoAbastecimiento(models.Model):
    movimiento = models.CharField(max_length=200)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    abastecimiento = models.ForeignKey(Abastecimiento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.producto.nombre}'