from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import NumberInput


class AsigEmpClie(models.Model):
    cliente = models.OneToOneField('Clientes', models.DO_NOTHING, primary_key=True)
    empleado = models.ForeignKey('Empleados', on_delete=models.CASCADE, unique=True)

    class Meta:
        managed = False
        db_table = 'asig_emp_clie'
        unique_together = (('cliente', 'empleado'),)


class Clientes(models.Model):
    cliente = models.OneToOneField('Personas', models.DO_NOTHING, primary_key=True)
    tipo_clie = models.ForeignKey('TipoClie', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'clientes'


class Empleados(models.Model):
    empleado = models.OneToOneField('Personas', models.DO_NOTHING, primary_key=True)
    tipo_emp = models.ForeignKey('TipoEmp',  blank=True, null=True, on_delete=models.CASCADE)
    permisos_add = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'


class Personas(models.Model):
    persona_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=25)
    ap_materno = models.CharField(max_length=25)
    telRegex = RegexValidator(regex=r"^\d{10}$")
    telefono = models.CharField(validators = [telRegex], max_length = 10, unique = True)
    dir_num = models.IntegerField(max_length=4)
    calle = models.CharField(max_length=25)
    colonia = models.CharField(max_length=25)
    delegacion = models.CharField(max_length=25)
    cpRegex = RegexValidator(regex=r"^\d{5}$")
    cod_postal = models.CharField(validators = [cpRegex], max_length = 5)
    municipio = models.CharField(max_length=25)
    estado = models.CharField(max_length=25)
    pais = models.CharField(max_length=25)
    correo = models.CharField(max_length=40)
    ESTADO_CIV = [
        ('S', 'SOLTERO(A)'),
        ('C', 'CASADO(A)'),
        ('D', 'DIVORSIADO(A)'),
        ('V', 'VIUDO(A)'),
    ]
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIV, default='S')
    fecha_nac = models.DateField()
    rfc = models.CharField(max_length=13)
    curp = models.CharField(max_length=28)
    fecha_reg = models.DateField()

    class Meta:
        managed = False
        db_table = 'personas'


class Tarea(models.Model):
    tarea_id = models.IntegerField(primary_key=True)
    id_creador = models.ForeignKey(Empleados, db_column='id_creador', blank=True, null=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(AsigEmpClie, blank=True, null=True, on_delete=models.CASCADE, related_name="id_emp_asig")
    id_emp_asig = models.ForeignKey(AsigEmpClie,  db_column='id_emp_asig', to_field='empleado_id', blank=True, null=True, on_delete=models.CASCADE)
    tramite = models.ForeignKey('Tramite', blank=True, null=True, on_delete=models.CASCADE)
    info_add = models.CharField(max_length=50, blank=True, null=True)
    dir_archivo = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)
    costo = models.IntegerField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    fecha_lim = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarea'


class TipoClie(models.Model):
    tipo_clie_id = models.IntegerField(primary_key=True)
    tipo_c = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_clie'


class TipoEmp(models.Model):
    tipo_emp_id = models.IntegerField(primary_key=True)
    tipo_e = models.CharField(max_length=25, blank=True, null=True)
    permisos = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_emp'


class Tramite(models.Model):
    tramite_id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    descrip = models.CharField(max_length=100, blank=True, null=True)
    requisitos = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tramite'