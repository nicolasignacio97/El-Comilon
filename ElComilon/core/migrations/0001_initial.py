from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('idcargo', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'cargo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('rutcliente', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombreusuario', models.CharField(max_length=15, unique=True)),
                ('nombres', models.CharField(max_length=20)),
                ('apellidos', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=30)),
                ('contrasena', models.CharField(max_length=20)),
                ('telefono', models.IntegerField()),
                ('correo', models.CharField(max_length=30)),
                ('saldocli', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('iddetallepedido', models.IntegerField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('valorunitario', models.IntegerField()),
                ('valortotal', models.IntegerField()),
            ],
            options={
                'db_table': 'detalle_pedido',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmpresaConvenio',
            fields=[
                ('rutempresaconvenio', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('razonsocial', models.CharField(max_length=30)),
                ('fechaconvenio', models.DateField()),
            ],
            options={
                'db_table': 'empresa_convenio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('idestado', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'estado_pedido',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstadoReclamo',
            fields=[
                ('idestreclamo', models.IntegerField(primary_key=True, serialize=False)),
                ('descestreclamo', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'estado_reclamo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('idpedido', models.BigIntegerField(primary_key=True, serialize=False)),
                ('valortotal', models.IntegerField()),
                ('fechapedido', models.DateField()),
                ('direccionpedido', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'pedido',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Platillo',
            fields=[
                ('idplatillo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('ingredientes', models.CharField(max_length=50)),
                ('valorunitario', models.IntegerField()),
                ('foto', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'platillo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('idreclamo', models.BigIntegerField(primary_key=True, serialize=False)),
                ('fechareclamo', models.DateField()),
                ('descreclamo', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'reclamo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Repartidor',
            fields=[
                ('rutrepartidor', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=20)),
                ('apellidos', models.CharField(max_length=20)),
                ('fechacontrato', models.DateField()),
                ('usuario', models.CharField(max_length=15)),
                ('contrasena', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'repartidor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('idregistroventas', models.BigIntegerField(primary_key=True, serialize=False)),
                ('montopromventas', models.BigIntegerField()),
                ('cantidadventas', models.BigIntegerField()),
                ('cantreclamos', models.BigIntegerField()),
                ('cantreclpendiente', models.BigIntegerField()),
                ('cantreclresuelto', models.BigIntegerField()),
                ('calidadreclamo', models.CharField(max_length=30)),
                ('cantpedfin', models.BigIntegerField()),
                ('cantpedcancelado', models.BigIntegerField()),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'reporte',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('rutrepresentante', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=20)),
                ('apellidos', models.CharField(max_length=20)),
                ('telefono', models.IntegerField()),
                ('correo', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'representante',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('rutrestaurante', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombrerestaurante', models.CharField(max_length=20)),
                ('direccionrestaurante', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'restaurante',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipoCliente',
            fields=[
                ('idtipocliente', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tipo_cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipoRestaurante',
            fields=[
                ('idtiporest', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tipo_restaurante',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('idtiposervicio', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tipo_servicio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('idtipovehiculo', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tipo_vehiculo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ruttrabajador', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=20)),
                ('apellidos', models.CharField(max_length=20)),
                ('fechacontrato', models.DateField()),
                ('usuario', models.CharField(max_length=15, unique=True)),
                ('contrasena', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'trabajador',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsuarioGeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.CharField(max_length=50, unique=True, verbose_name='Correo Electronico')),
                ('nombres', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=50, null=True, verbose_name='Apellidos')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'UsuarioGeneral',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('patentevehiculo', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('modelo', models.CharField(max_length=20)),
                ('anio', models.IntegerField()),
                ('color', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'vehiculo',
                'managed': False,
            },
        ),
    ]
