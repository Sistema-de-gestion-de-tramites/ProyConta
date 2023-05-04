# Generated by Django 4.1.2 on 2023-05-02 04:49

import apps.sat.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'db_table': 'comentarios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ext', models.IntegerField(verbose_name='Num. Ext.')),
                ('calle', models.CharField(max_length=40, verbose_name='Calle')),
                ('colonia', models.CharField(max_length=40, verbose_name='Colonia')),
                ('cod_postal', models.CharField(max_length=5, validators=[apps.sat.models.validar_CP], verbose_name='Codigo Postal')),
                ('municipio', models.CharField(max_length=25, verbose_name='Municipio')),
                ('estado', models.CharField(max_length=25, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones',
                'db_table': 'direcciones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
                'db_table': 'estados',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Personas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('ap_paterno', models.CharField(max_length=30, verbose_name='Apellido paterno')),
                ('ap_materno', models.CharField(max_length=30, verbose_name='Apellido materno')),
                ('estado_civil', models.CharField(choices=[('S', 'SOLTERO(A)'), ('C', 'CASADO(A)'), ('D', 'DIVORSIADO(A)'), ('U', 'SEPARADO(A)'), ('V', 'VIUDO(A)')], default='S', max_length=1, verbose_name='Estado civil')),
                ('correo', models.EmailField(max_length=254)),
                ('fecha_nac', models.DateField(verbose_name='Fecha de nacimiento')),
                ('rfc', models.CharField(max_length=13, unique=True, validators=[apps.sat.models.validar_RFC], verbose_name='RFC')),
                ('curp', models.CharField(max_length=28, validators=[apps.sat.models.validar_CURP], verbose_name='CURP')),
                ('fecha_reg', models.DateField(verbose_name='Fecha de registro')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'db_table': 'personas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo_Archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension', models.CharField(max_length=5, verbose_name='Extensión')),
            ],
            options={
                'verbose_name': 'Tipo de archivo',
                'verbose_name_plural': 'Tipos de archivos',
                'db_table': 'tipo_archivos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo_Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=20, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de Usuario',
                'verbose_name_plural': 'Tipos de Usuarios',
                'db_table': 'tipo_usuarios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo_Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('tamano_MB', models.IntegerField(default=4, verbose_name='Tamaño en MB')),
                ('archivos', models.ManyToManyField(related_name='archivos', to='sat.tipo_archivos', verbose_name='Archivos')),
            ],
            options={
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documentos',
                'db_table': 'tipo_documentos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Telefonos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=30, verbose_name='Descripción')),
                ('telefono', models.CharField(max_length=10, unique=True, validators=[apps.sat.models.validar_telefono], verbose_name='Telefono')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Persona')),
            ],
            options={
                'verbose_name': 'Telefono',
                'verbose_name_plural': 'Telefonos',
                'db_table': 'telefonos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rol', models.CharField(max_length=20, verbose_name='Nombre')),
                ('documentos', models.ManyToManyField(related_name='documentos', to='sat.tipo_documentos')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'Rol',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='personas',
            name='tipo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_usuarios', verbose_name='Tipo de usuario'),
        ),
        migrations.CreateModel(
            name='Ext_Direcciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_int', models.IntegerField(verbose_name='Num. Int.')),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.direcciones', verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones',
                'db_table': 'ext_direcciones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Entrega_Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=100, verbose_name='Comentario')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('direccion', models.FileField(upload_to='', verbose_name='Documento')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='sat.personas', verbose_name='Cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to='sat.personas', verbose_name='Empleado')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.estados', verbose_name='Estado')),
                ('tipo_doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_documentos', verbose_name='Tipo de documento')),
            ],
            options={
                'verbose_name': 'Entrega de documento',
                'verbose_name_plural': 'Entregas de documentos',
                'db_table': 'entrega_documentos',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='direcciones',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Persona'),
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta', models.CharField(max_length=30, verbose_name='Cuenta')),
                ('contra', models.CharField(max_length=30, verbose_name='Contraseña')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
                'db_table': 'cuentas',
                'managed': True,
            },
        ),
    ]
