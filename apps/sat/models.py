from django.db import models
from django.core.validators import RegexValidator

# Tablas de personas
# --------------------------------------------------------------------------
class Rol(models.Model):
    Rol = models.CharField(max_length=20, verbose_name="Nombre")

    class Meta:
        managed = True
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "Rol"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Rol._meta.fields]

    def nombre_principal(self):
        return self.Rol

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

class Personas(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    ap_paterno = models.CharField(max_length=30, verbose_name="Apellido paterno")
    ap_materno = models.CharField(max_length=30, verbose_name="Apellido materno")

    ESTADO_CIV = [
        ('S', 'SOLTERO(A)'),
        ('C', 'CASADO(A)'),
        ('D', 'DIVORSIADO(A)'),
        ('V', 'VIUDO(A)'),
    ]
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIV, default='S', verbose_name="Estado civil")

    fecha_nac = models.DateField(verbose_name="Fecha de nacimiento")
    rfc = models.CharField(max_length=13, verbose_name="RFC")
    curp = models.CharField(max_length=28, verbose_name="CURP")
    fecha_reg = models.DateField(verbose_name="Fecha de registro")
    tipo_usuario = models.ForeignKey(Tipo_Usuarios, on_delete=models.CASCADE, verbose_name="Tipo de usuario")

    class Meta:
        managed = True
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "personas"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Personas._meta.fields]

    def nombre_principal(self):
        return self.nombre + " " + self.ap_paterno + " " + self.ap_materno

class Telefonos(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Persona")
    descr = models.CharField(max_length=30, verbose_name="Descripción")
    telRegex = RegexValidator(regex=r"^\d{10}$")
    telefono = models.CharField(validators=[telRegex], max_length=10, unique=True, verbose_name="Telefono")

    class Meta:
        managed = True
        verbose_name = "Telefono"
        verbose_name_plural = "Telefonos"
        db_table = "telefonos"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Telefonos._meta.fields]

    def nombre_principal(self):
        return self.descr

class Direcciones(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Persona")
    num_ext = models.IntegerField(verbose_name="Num. Ext.")
    calle = models.CharField(max_length=40, verbose_name="Calle")
    colonia = models.CharField(max_length=40, verbose_name="Colonia")
    cpRegex = RegexValidator(regex=r"^\d{5}$")
    cod_postal = models.CharField(validators=[cpRegex], max_length=5, verbose_name="Codigo Postal")
    municipio = models.CharField(max_length=25, verbose_name="Municipio")
    estado = models.CharField(max_length=25, verbose_name="Estado")

    class Meta:
        managed = True
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        db_table = "direcciones"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Direcciones._meta.fields]

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

class Estados(models.Model):
    nombre = models.CharField(max_length=10, verbose_name="Nombre")

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

class Comentarios(models.Model):
    descr = models.CharField(max_length=100, verbose_name="Descripción")  # Descripcion

    class Meta:
        managed = True
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        db_table = "comentarios"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Comentarios._meta.fields]

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

class Tipo_Tramites(models.Model):
    nombre = models.CharField(max_length=40, verbose_name="Nombre")
    tiempo_estimado = models.IntegerField(default=5, verbose_name="Días estimados")  # _______________________
    habilitado = models.BooleanField(verbose_name="Habilitado")

    class Meta:
        managed = True
        verbose_name = "Tipo de tramite"
        verbose_name_plural = "Tipos de tramites"
        db_table = "tipo_tramites"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tipo_Tramites._meta.fields]

    def nombre_principal(self):
        return self.nombre

class Tipo_Documentos(models.Model):
    nombre = models.CharField(max_length=40, verbose_name="Nombre")
    tamano_MB = models.IntegerField(default=4, verbose_name="Tamaño en MB")

    class Meta:
        managed = True
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"
        db_table = "tipo_documentos"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tipo_Documentos._meta.fields]

    def nombre_principal(self):
        return self.nombre

class Rel_Tram_Doc(models.Model):  # Relacion tramite-documento
    tramite = models.ForeignKey(Tipo_Tramites, on_delete=models.CASCADE, verbose_name="Tramite")
    documento = models.ForeignKey(Tipo_Documentos, on_delete=models.CASCADE, verbose_name="Documento")

    class Meta:
        managed = True
        db_table = "rel_tram_doc"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Rel_Tram_Doc._meta.fields]

class Rel_Tram_Rol(models.Model):  # Relacion tramite-rol
    tramite = models.ForeignKey(Tipo_Tramites, on_delete=models.CASCADE, verbose_name="Tramite")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="Rol")

    class Meta:
        managed = True
        db_table = "rel_tram_rol"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Rel_Tram_Rol._meta.fields]

class Rel_Empl_Rol(models.Model):  # Relacion empleado-rol
    empleado = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Empleado")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="Rol")

    class Meta:
        managed = True
        db_table = "rel_emp_rol"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Rel_Empl_Rol._meta.fields]

class Rel_Doc_TipoArch(models.Model):  # Relacion Documento-extension
    documento = models.ForeignKey(Tipo_Documentos, on_delete=models.CASCADE, verbose_name="Documento")
    extension = models.ForeignKey(Tipo_Archivos, on_delete=models.CASCADE, verbose_name="Extensión")

    class Meta:
        managed = True
        db_table = "rel_doc_tiparch"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Rel_Doc_TipoArch._meta.fields]

class Entrega_Doc(models.Model):
    cliente = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Cliente")
    tipo_doc = models.ForeignKey(Tipo_Documentos, on_delete=models.CASCADE, verbose_name="Tipo de documento")
    direccion = models.CharField(max_length=100, verbose_name="Dirección del archivo")

    class Meta:
        managed = True
        verbose_name = "Entrega de documento"
        verbose_name_plural = "Entregas de documentos"
        db_table = "entrega_documentos"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Entrega_Doc._meta.fields]

class Observ_Doc(models.Model):
    documento = models.ForeignKey(Entrega_Doc, on_delete=models.CASCADE, verbose_name="Documento")
    supervisor = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Supervisor")
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE, verbose_name="Estado")
    comentario = models.CharField(max_length=100, verbose_name="Comentario")
    fecha = models.DateTimeField(verbose_name="Fecha")

    class Meta:
        managed = True
        verbose_name = "Observación del documento"
        verbose_name_plural = "Observaciones del documento"
        db_table = "observ_doc"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Observ_Doc._meta.fields]

class Tramite(models.Model):
    cliente = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Cliente")
    tramite = models.ForeignKey(Tipo_Tramites, on_delete=models.CASCADE, verbose_name="Tramite")

    class Meta:
        managed = True
        verbose_name = "Tramite"
        verbose_name_plural = "Tramites"
        db_table = "tramites"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Tramite._meta.fields]

class Observ_Tramite(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE, verbose_name="Tramite")
    supervisor = models.ForeignKey(Personas, on_delete=models.CASCADE, verbose_name="Supervisor")
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE, verbose_name="Estado")
    comentario = models.CharField(max_length=100, verbose_name="Comentario")
    fecha = models.DateTimeField(verbose_name="Fecha")

    class Meta:
        managed = True
        verbose_name = "Observación del tramite"
        verbose_name_plural = "Observaciones del tramite"
        db_table = "observ_tramites"

    def get_fields_and_values(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in Observ_Tramite._meta.fields]