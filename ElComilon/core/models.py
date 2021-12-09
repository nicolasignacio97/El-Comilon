# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import BaseUserManager 
from django.conf import settings
from  django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin 

class Cargo(models.Model):
    idcargo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cargo'


class Cliente(models.Model):
    rutcliente = models.CharField(primary_key=True, max_length=12)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=30)
    saldocli = models.BigIntegerField(blank=True, null=True)
    idtipocliente = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='idtipocliente')
    rutempconv = models.ForeignKey('EmpresaConvenio', models.DO_NOTHING, db_column='rutempconv', blank=True, null=True)
    idcuenta = models.ForeignKey(User,models.DO_NOTHING , db_column='idcuenta')

    def __str__(self):
        return self.rutcliente;

    class Meta:
        managed = False
        db_table = 'cliente'


class DetallePedido(models.Model):
    iddetallepedido = models.IntegerField(primary_key=True)
    cantidad = models.IntegerField()
    valorunitario = models.IntegerField()
    valortotal = models.IntegerField()
    idpedido = models.ForeignKey('Pedido', models.DO_NOTHING,related_name='re_idpedido',db_column='idpedido')
    idplatillo = models.ForeignKey('Platillo', models.DO_NOTHING,related_name='re_idplatillo', db_column='idplatillo')
    idestadoPlatillo = models.ForeignKey('Pedido', models.DO_NOTHING,related_name='re_idtiposervicio',db_column='idtiposervicio')
    rutcliente = models.ForeignKey('Pedido', models.DO_NOTHING, related_name='re_rutcliente',db_column='rutcliente')
    ID_ESTADO_PLATILLO = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalle_pedido'


class EmpresaConvenio(models.Model):
    rutempresaconvenio = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=20)
    razonsocial = models.CharField(max_length=30)
    fechaconvenio = models.DateField()
    def __str__(self):
        return self.rutempresaconvenio

    class Meta:
        managed = False
        db_table = 'empresa_convenio'


class EstadoPedido(models.Model):
    idestado = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)
    def __str__(self):
        return self.idestado 

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'estado_pedido'


class EstadoReclamo(models.Model):
    idestreclamo = models.IntegerField(primary_key=True)
    descestreclamo = models.CharField(max_length=1000)


    class Meta:
        managed = False
        db_table = 'estado_reclamo'

class MenuSemanal(models.Model):
    idmenu = models.IntegerField(primary_key=True)
    dia = models.CharField(max_length=20)
    idplatillo = models.IntegerField()
    rutcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rutcliente')

    class Meta:
        managed = False
        db_table = 'menu_semanal'

class Pedido(models.Model):
    idpedido = models.BigIntegerField(primary_key=True)
    valortotal = models.IntegerField()
    fechapedido = models.DateField()
    direccionpedido = models.CharField(max_length=30, blank=True, null=True)
    idtiposervicio = models.ForeignKey('TipoServicio', models.DO_NOTHING, db_column='idtiposervicio')
    rutcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rutcliente')
    idestpedido = models.ForeignKey(EstadoPedido, models.DO_NOTHING, db_column='idestpedido')

    def __str__(self):
        return self.rutcliente

    class Meta:
        managed = False
        db_table = 'pedido'
        unique_together = (('idpedido', 'idtiposervicio', 'rutcliente'),)


class Platillo(models.Model):
    idplatillo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    ingredientes = models.CharField(max_length=50)
    disponible = models.BooleanField(blank= True)
    valorunitario = models.IntegerField()
    foto = models.ImageField(blank=True, null=True)
    rutrestaurante = models.ForeignKey('Restaurante', models.DO_NOTHING, db_column='rutrestaurante')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'platillo'


class Reclamo(models.Model):
    idreclamo = models.BigIntegerField(primary_key=True)
    fechareclamo = models.DateField()
    descreclamo = models.CharField(max_length=1000)
    rutcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rutcliente')
    idestreclamo = models.ForeignKey(EstadoReclamo, models.DO_NOTHING, db_column='idestreclamo')

    class Meta:
        managed = False
        db_table = 'reclamo'


class Repartidor(models.Model):
    rutrepartidor = models.CharField(primary_key=True, max_length=12)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    fechacontrato = models.DateField()
    rutrestaurante = models.ForeignKey('Restaurante', models.DO_NOTHING, db_column='rutrestaurante')
    idcuenta = models.ForeignKey(User,models.DO_NOTHING , db_column='idcuenta')
    

    def __str__(self):
        return self.rutrepartidor 

    class Meta:
        managed = False
        db_table = 'repartidor'


class Reporte(models.Model):
    idregistroventas = models.BigIntegerField(primary_key=True)
    montopromventas = models.BigIntegerField()
    cantidadventas = models.BigIntegerField()
    cantreclamos = models.BigIntegerField()
    cantreclpendiente = models.BigIntegerField()
    cantreclresuelto = models.BigIntegerField()
    calidadreclamo = models.CharField(max_length=30)
    cantpedfin = models.BigIntegerField()
    cantpedcancelado = models.BigIntegerField()
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'reporte'


class Representante(models.Model):
    rutrepresentante = models.CharField(primary_key=True, max_length=12)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    telefono = models.IntegerField()
    idcuenta = models.ForeignKey(User,models.DO_NOTHING , db_column='idcuenta')

    class Meta:
        managed = False
        db_table = 'representante'


class Restaurante(models.Model):
    rutrestaurante = models.CharField(primary_key=True, max_length=12)
    nombrerestaurante = models.CharField(max_length=20)
    direccionrestaurante = models.CharField(max_length=30)
    rutrepresentante = models.ForeignKey(Representante, models.DO_NOTHING, db_column='rutrepresentante')
    idtiporest = models.ForeignKey('TipoRestaurante', models.DO_NOTHING, db_column='idtiporest')
    
    def __str__(self):
        return self.rutrestaurante

  
    class Meta:
        managed = False
        db_table = 'restaurante'


class TipoCliente(models.Model):
    idtipocliente = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'


class TipoRestaurante(models.Model):
    idtiporest = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_restaurante'


class TipoServicio(models.Model):
    idtiposervicio = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion


    class Meta:
        managed = False
        db_table = 'tipo_servicio'


class TipoVehiculo(models.Model):
    idtipovehiculo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.idtipovehiculo) 

    class Meta:
        managed = False
        db_table = 'tipo_vehiculo'



class Trabajador(models.Model):
    ruttrabajador = models.CharField(primary_key=True, max_length=12)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    fechacontrato = models.DateField()
    # usuario = models.CharField( unique=True, max_length=15)
    # contrasena = models.CharField(max_length=20)
    rutrestaurante = models.ForeignKey(Restaurante, models.DO_NOTHING, db_column='rutrestaurante')
    idcargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='idcargo')
    idcuenta = models.ForeignKey(User,models.DO_NOTHING , db_column='idcuenta')



    class Meta:
        managed = False
        db_table = 'trabajador'


class Vehiculo(models.Model):
    idvehiculo = models.CharField(primary_key=True, max_length=20)
    patentevehiculo = models.CharField(max_length=6)
    modelo = models.CharField(max_length=20)
    anio = models.IntegerField()
    color = models.CharField(max_length=20)
    rutrepartidor = models.ForeignKey(Repartidor, models.DO_NOTHING, db_column='rutrepartidor')
    idtipovehiculo = models.ForeignKey(TipoVehiculo, models.DO_NOTHING, db_column='idtipovehiculo')

    def __str__(self):
        return self.patentevehiculo 
    
        
    class Meta:
        managed = False
        db_table = 'vehiculo'
