from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re
# Tablas de personas
# --------------------------------------------------------------------------
from django.db.models import ForeignKey

def validar_CURP(value):
    patron = r"^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$"

    if not re.match(patron, value):
        raise ValidationError('CURP invalida.')

def validar_RFC(value):
    patron = r"^[A-Za-zñÑ&]{3,4}\d{6}\w{3}$"

    if not re.match(patron, value):
        raise ValidationError('RFC invalido.')

def validar_telefono(value):
    patron = r"^\d{10}$"

    if not re.match(patron, value):
        raise ValidationError('Telefono invalido.')

def validar_CP(value):
    patron = r"^\d{5}$"

    if not re.match(patron, value):
        raise ValidationError('El codigo postal debe tener 5 digitos.')



class Tipo_Archivos(models.Model):
    extension = models.CharField(max_length=5, verbose_name="Extensión")
    # Ejemplo: pdf, doc, jpg, png, xml, xlsx

    class Meta:
        managed = True
        verbose_name = "Tipo de archivo"
        verbose_name_plural = "Tipos de archivos"
        db_table = "tipo_archivos"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tipo_Archivos._meta.fields]

    def nombre_principal(self):
        return self.extension

    def __str__(self):
        return self.extension

class Tipo_Documentos(models.Model):
    nombre = models.CharField(max_length=40, verbose_name="Nombre")
    tamano_MB = models.IntegerField(default=4, verbose_name="Tamaño en MB")
    archivos = models.ManyToManyField(Tipo_Archivos, related_name="archivos", verbose_name="Archivos")
    class Meta:
        managed = True
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"
        db_table = "tipo_documentos"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tipo_Documentos._meta.fields]

    def nombre_principal(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Tipo_Usuarios(models.Model):
    descr = models.CharField(max_length=20, verbose_name="Descripción")

    class Meta:
        managed = True
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuarios"
        db_table = "tipo_usuarios"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tipo_Usuarios._meta.fields]

    def nombre_principal(self):
        return self.descr

    def __str__(self):
        return self.descr
 
class Personas(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    ap_paterno = models.CharField(max_length=30, verbose_name="Apellido paterno")
    ap_materno = models.CharField(max_length=30, verbose_name="Apellido materno")

    ESTADO_CIV = [
        ('S', 'SOLTERO(A)'),
        ('C', 'CASADO(A)'),
        ('D', 'DIVORSIADO(A)'),
        ('U', 'SEPARADO(A)'),
        ('V', 'VIUDO(A)'),
    ]
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIV, default='S', verbose_name="Estado civil")
    correo = models.EmailField(max_length=254, verbose_name="E-mail")
    fecha_nac = models.DateField(verbose_name="Fecha de nacimiento")
    rfc = models.CharField(validators=[validar_RFC], max_length=13, unique=True, verbose_name="RFC")
    curp = models.CharField(validators=[validar_CURP], max_length=28, verbose_name="CURP")
    fecha_reg = models.DateField(verbose_name="Fecha de registro")
    tipo_usuario = models.ForeignKey(Tipo_Usuarios, on_delete=models.CASCADE, verbose_name="Tipo de usuario")
    foto_perfil = models.ImageField(upload_to='fotos_perfil/',null=True,blank=True, verbose_name="Foto de perfil")
    
    class Meta:
        managed = True
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "personas"

    def clean_curp(self):
        validar_CURP(self.curp)
        return self.curp

    def clean_rfc(self):
        validar_RFC(self.rfc)
        return self.rfc

    def get_fields_and_values(self):
        fields = []
        for field in self._meta.fields:
            if isinstance(field, ForeignKey):
                related_obj = getattr(self, field.name)
                if related_obj is not None:
                    fields.append((field.verbose_name, related_obj.nombre_principal()))
            else:
                fields.append((field.verbose_name, getattr(self, field.name)))
        return fields

    def nombre_principal(self):
        return self.nombre + " " + self.ap_paterno + " " + self.ap_materno

    def __str__(self):
        return self.nombre + " " + self.ap_paterno + " " + self.ap_materno

class Telefonos(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Persona")
    descr = models.CharField(max_length=30, verbose_name="Descripción")
    telefono = models.CharField(validators=[validar_telefono], max_length=10, unique=True, verbose_name="Telefono")

    class Meta:
        managed = True
        verbose_name = "Telefono"
        verbose_name_plural = "Telefonos"
        db_table = "telefonos"

    def clean_telefono(self):
        validar_telefono(self.telefono)
        return self.telefono

    def get_fields_and_values(self):
        fields = []
        for field in self._meta.fields:
            if isinstance(field, ForeignKey):
                related_obj = getattr(self, field.name)
                if related_obj is not None:
                    related_fields = [('Nombre', related_obj.nombre_principal())]
                    fields.extend(related_fields)
            else:
                fields.append((field.verbose_name, getattr(self, field.name)))
        return fields


        #return [(field.verbose_name, field.value_to_string(self)) for field in Telefonos._meta.fields]
    def __str__(self):
        return self.descr + ': ' + self.telefono

    def nombre_principal(self):
        return self.descr

class Direcciones(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Persona")
    num_ext = models.IntegerField(verbose_name="Num. Ext.")
    calle = models.CharField(max_length=40, verbose_name="Calle")
    colonia = models.CharField(max_length=40, verbose_name="Colonia")
    cod_postal = models.CharField(validators=[validar_CP], max_length=5, verbose_name="Codigo Postal")
    municipio = models.CharField(max_length=25, verbose_name="Municipio")
    estado = models.CharField(max_length=25, verbose_name="Estado")

    class Meta:
        managed = True
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        db_table = "direcciones"

    def clean_cod_postal(self):
        validar_CP(self.cod_postal)
        return self.cod_postal

    def get_fields_and_values(self):
        fields = []
        for field in self._meta.fields:
            if isinstance(field, ForeignKey):
                related_obj = getattr(self, field.name)
                if related_obj is not None:
                    related_fields = [('Nombre', related_obj.nombre_principal())]
                    fields.extend(related_fields)
            else:
                fields.append((field.verbose_name, getattr(self, field.name)))
        return fields

    def __str__(self):
        return 'Calle ' + self.calle + ' #' + str(self.num_ext) + ', Col. ' + self.colonia + ', ' + self.municipio + ', ' + self.estado

class Ext_Direcciones(models.Model):
    direccion = models.ForeignKey(Direcciones, on_delete=models.CASCADE, verbose_name="Dirección")
    num_int = models.IntegerField(verbose_name="Num. Int.")

    class Meta:
        managed = True
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        db_table = "ext_direcciones"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Ext_Direcciones._meta.fields]

class Cuentas(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Cliente")
    cuenta = models.CharField(max_length=30, verbose_name="Cuenta")
    contra = models.CharField(max_length=1000, verbose_name="Contraseña")

    class Meta:
        managed = True
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        db_table = "cuentas"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Cuentas._meta.fields]

    def __str__(self):
        return self.cuenta

class Estados(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    # ENTREGADO, CANCELADO, ATRASADO, INICIADO, PENDIENTE,

    class Meta:
        managed = True
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        db_table = "estados"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Estados._meta.fields]

    def nombre_principal(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Comentarios(models.Model):
    descr = models.CharField(max_length=100, verbose_name="Descripción", )  # Descripcion

    class Meta:
        managed = True
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        db_table = "comentarios"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Comentarios._meta.fields]

    def __str__(self):
        return self.descr

class Entrega_Doc(models.Model):
    cliente = models.ForeignKey(Personas, on_delete=models.CASCADE, related_name="cliente", verbose_name="Cliente")
    empleado = models.ForeignKey(Personas, on_delete=models.CASCADE, related_name="empleado", verbose_name="Empleado")
    tipo_doc = models.ForeignKey(Tipo_Documentos, on_delete=models.CASCADE, verbose_name="Tipo de documento")
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE, verbose_name="Estado")
    comentario = models.CharField(max_length=100, verbose_name="Comentario")
    fecha = models.DateTimeField(verbose_name="Fecha")
    direccion = models.FileField(verbose_name="Documento")

    class Meta:
        managed = True
        verbose_name = "Entrega de documento"
        verbose_name_plural = "Entregas de documentos"
        db_table = "entrega_documentos"

    def get_fields_and_values(self):
        fields = []
        for field in self._meta.fields:
            if isinstance(field, ForeignKey):
                related_obj = getattr(self, field.name)
                if related_obj is not None:
                    fields.append((field.verbose_name,related_obj.nombre_principal()))
            else:
                fields.append((field.verbose_name, getattr(self, field.name)))
        return fields

    def __str__(self):
        return self.cliente.__str__() + ': ' + self.tipo_doc.__str__()

class Usuario_empleado(models.Model):
    empleado = models.ForeignKey(Personas, on_delete=models.CASCADE, related_name="empleado_id", verbose_name="Empleado")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_id", verbose_name="Usuario")

    class Meta:
        managed = True
        verbose_name = "usuario empleado"
        verbose_name_plural = "usuarios empleados"
        db_table = "usuario_empleado"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Usuario_empleado._meta.fields]