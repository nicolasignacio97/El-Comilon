from django.db import models
from django.db.models.fields import related



class Cliente(models.Model):
    rutcliente = models.CharField(primary_key=True, max_length=12)
    nombreusuario = models.CharField(max_length=15)
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    contrasena = models.CharField(max_length=20)
    telefono = models.IntegerField()
    correo = models.CharField(max_length=30)
    saldocli = models.BigIntegerField(blank=True, null=True)
    idtipocliente = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='idtipocliente')
    rutempconv = models.ForeignKey('EmpresaConvenio', models.DO_NOTHING, db_column='rutempconv', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class TipoCliente(models.Model):
    idtipocliente = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'

class EmpresaConvenio(models.Model):
        rutempresaconvenio = models.CharField(primary_key=True, max_length=12)
        nombre = models.CharField(max_length=20)
        razonsocial = models.CharField(max_length=30)
        fechaconvenio = models.DateField()

        class Meta:
            managed = False
            db_table = 'empresa_convenio'