from django.db import models
from django.core.validators import RegexValidator

'''
    DROP DATABASE project_ing;
    CREATE DATABASE project_ing;
'''

class Clientes(models.Model):
    cliente = models.OneToOneField('Personas', models.DO_NOTHING, primary_key=True)
    tipo_clie = models.ForeignKey('TipoClie', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'clientes'


class Empleados(models.Model):
    empleado = models.OneToOneField('Personas', models.DO_NOTHING, primary_key=True)
    tipo_emp = models.ForeignKey('TipoEmp',  blank=True, null=True, on_delete=models.CASCADE)
    clie_s = models.ManyToManyField(Clientes, through="Emp_Clie_Asig")       #genera una nueva tabla
    permisos_add = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'empleados'


class Emp_Clie_Asig(models.Model):
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)


class Personas(models.Model):
    nombre = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=25)
    ap_materno = models.CharField(max_length=25)
    telRegex = RegexValidator(regex=r"^\d{10}$")
    telefono = models.CharField(validators = [telRegex], max_length = 10, unique = True)
    dir_num = models.IntegerField()
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
        managed = True
        db_table = 'personas'

class Tarea(models.Model):
    emp_creador = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    emp_clie = models.ForeignKey(Emp_Clie_Asig, on_delete=models.CASCADE)
    tramite = models.ForeignKey('Tramite', on_delete=models.CASCADE)
    info_add = models.CharField(max_length=50, blank=True, null=True)
    dir_archivo = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=10)
    costo = models.IntegerField(default=0)
    fecha_ini = models.DateTimeField()
    fecha_lim = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        managed = True
        db_table = 'tarea'


class TipoClie(models.Model):
    tipo_c = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_clie'


class TipoEmp(models.Model):
    tipo_e = models.CharField(max_length=25, blank=True, null=True)
    permisos = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_emp'


class Tramite(models.Model):
    tipo = models.CharField(max_length=25, blank=True, null=True)
    descrip = models.CharField(max_length=100, blank=True, null=True)
    requisitos = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tramite'