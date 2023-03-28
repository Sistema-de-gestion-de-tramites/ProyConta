# Generated by Django 4.1.7 on 2023-03-22 02:17

import django.core.validators
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
                ('cod_postal', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(regex='^\\d{5}$')], verbose_name='Codigo Postal')),
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
            name='Entrega_Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección del archivo')),
            ],
            options={
                'verbose_name': 'Entrega de documento',
                'verbose_name_plural': 'Entregas de documentos',
                'db_table': 'entrega_documentos',
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
                ('estado_civil', models.CharField(choices=[('S', 'SOLTERO(A)'), ('C', 'CASADO(A)'), ('D', 'DIVORSIADO(A)'), ('V', 'VIUDO(A)')], default='S', max_length=1, verbose_name='Estado civil')),
                ('fecha_nac', models.DateField(verbose_name='Fecha de nacimiento')),
                ('rfc', models.CharField(max_length=13, verbose_name='RFC')),
                ('curp', models.CharField(max_length=28, verbose_name='CURP')),
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
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rol', models.CharField(max_length=20, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'Rol',
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
            name='Tipo_Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('tamano_MB', models.IntegerField(default=4, verbose_name='Tamaño en MB')),
            ],
            options={
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documentos',
                'db_table': 'tipo_documentos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo_Tramites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('tiempo_estimado', models.IntegerField(default=5, verbose_name='Días estimados')),
                ('habilitado', models.BooleanField(verbose_name='Habilitado')),
            ],
            options={
                'verbose_name': 'Tipo de tramite',
                'verbose_name_plural': 'Tipos de tramites',
                'db_table': 'tipo_tramites',
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
            name='Tramite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Cliente')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_tramites', verbose_name='Tramite')),
            ],
            options={
                'verbose_name': 'Tramite',
                'verbose_name_plural': 'Tramites',
                'db_table': 'tramites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Telefonos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descr', models.CharField(max_length=30, verbose_name='Descripción')),
                ('telefono', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{10}$')], verbose_name='Telefono')),
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
            name='Rel_Tram_Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.rol', verbose_name='Rol')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_tramites', verbose_name='Tramite')),
            ],
            options={
                'db_table': 'rel_tram_rol',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rel_Tram_Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_documentos', verbose_name='Documento')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_tramites', verbose_name='Tramite')),
            ],
            options={
                'db_table': 'rel_tram_doc',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rel_Empl_Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Empleado')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.rol', verbose_name='Rol')),
            ],
            options={
                'db_table': 'rel_emp_rol',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rel_Doc_TipoArch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_documentos', verbose_name='Documento')),
                ('extension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_archivos', verbose_name='Extensión')),
            ],
            options={
                'db_table': 'rel_doc_tiparch',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='personas',
            name='tipo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_usuarios', verbose_name='Tipo de usuario'),
        ),
        migrations.CreateModel(
            name='Observ_Tramite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=100, verbose_name='Comentario')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.estados', verbose_name='Estado')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Supervisor')),
                ('tramite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tramite', verbose_name='Tramite')),
            ],
            options={
                'verbose_name': 'Observación del tramite',
                'verbose_name_plural': 'Observaciones del tramite',
                'db_table': 'observ_tramites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Observ_Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=100, verbose_name='Comentario')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.entrega_doc', verbose_name='Documento')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.estados', verbose_name='Estado')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Supervisor')),
            ],
            options={
                'verbose_name': 'Observación del documento',
                'verbose_name_plural': 'Observaciones del documento',
                'db_table': 'observ_doc',
                'managed': True,
            },
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
        migrations.AddField(
            model_name='entrega_doc',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='entrega_doc',
            name='tipo_doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.tipo_documentos', verbose_name='Tipo de documento'),
        ),
        migrations.AddField(
            model_name='direcciones',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sat.personas', verbose_name='Persona'),
        ),
    ]
