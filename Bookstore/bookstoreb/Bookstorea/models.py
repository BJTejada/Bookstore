from django.db import models
from datetime import date


class CATEGORIAS(models.Model):
    id_categ=models.IntegerField(primary_key=True, default=0)
    nombre_categ=models.CharField(max_length=40)
    def __str__(self):
        return f"ID: {self.id_categ} - {self.nombre_categ}"
    
class PROVEEDORES(models.Model):
    id_prov=models.IntegerField(primary_key=True)
    nombre_prov=models.CharField(max_length=200)
    telefono_prov=models.CharField(max_length=50)
    direccion_prov=models.CharField(max_length=200)
    correo_prov=models.CharField(max_length=80)
    def __str__(self):
        return f"ID: {self.id_prov} - {self.nombre_prov}"
    
class PRODUCTO(models.Model):
    id_prod=models.IntegerField(primary_key=True)
    nombre_prod=models.CharField(max_length=200)
    marca_prod=models.CharField(max_length=50)
    # Referencia a la llave primaria personalizada en Proveedor y Categoria
    proveedor = models.ForeignKey(PROVEEDORES, on_delete=models.CASCADE, to_field='id_prov')
    categoria = models.ForeignKey(CATEGORIAS, on_delete=models.CASCADE, to_field='id_categ')
    def __str__(self):
        return f"ID: {self.id_prod} - {self.nombre_prod}"

class USUARIOS(models.Model):
    id_usuario=models.IntegerField(primary_key=True)
    nombre_usuario=models.CharField(max_length=20)
    psw_usuario=models.CharField(max_length=25)
    def __str__(self):
        return f"ID:{self.id_usuario}-{self.nombre_usuario}"

class ROLES(models.Model):
    id_rol=models.IntegerField(primary_key=True)
    tipo_rol=models.CharField(max_length=20)
    def __str__(self):
        return f"ID:{self.id_rol}-{self.tipo_rol}"

class EMPLEADOS(models.Model):
    id_empleado=models.IntegerField(primary_key=True)
    nombre_empleado=models.CharField(max_length=80)
    apellido=models.CharField(max_length=80)
    telefono=models.CharField(max_length=15)
    dui=models.CharField(max_length=15)
    correo_cliente=models.CharField(max_length=80)
    estado=models.IntegerField()
    fechaingreso=models.DateField(default=date.today)
    salario=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    usuario = models.ForeignKey(USUARIOS, on_delete=models.CASCADE,to_field='id_usuario')
    rol = models.ForeignKey(ROLES, on_delete=models.CASCADE,to_field='id_rol')
    def __str__(self):
        return f"ID:{self.id_empleado}-{self.nombre_empleado}"
    
class COMPRAS(models.Model):
    id_compra=models.IntegerField(primary_key=True)
    num_factura=models.CharField(max_length=10)
    fecha_compra=models.DateField(default=date.today)
    total_compra=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    empleado = models.ForeignKey(EMPLEADOS,on_delete=models.CASCADE,to_field='id_empleado')
    def __str__(self):
        return f"ID: {self.id_compra} - {self.num_factura}"

class DETALLECOMPRA(models.Model):
    id_det_compra=models.IntegerField(primary_key=True)
    precio_unit_compra=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    cantidad=models.IntegerField()
    total_det_compra=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    producto = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE,to_field='id_prod')
    compra = models.ForeignKey(COMPRAS,on_delete=models.CASCADE,to_field='id_compra')
    def __str__(self):
        return f"ID:{self.id_det_compra}-{self.producto}"

class LOTES(models.Model):
    id_lote=models.IntegerField(primary_key=True,)
    fecha_entrada=models.DateField(default=date.today)
    cantidad=models.IntegerField()
    fecha_caducidad=models.DateField()
    precio_venta=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    detalle_compra = models.ForeignKey(DETALLECOMPRA,on_delete=models.CASCADE,to_field='id_det_compra')
    def __str__(self):
        return f"ID:{self.id_lote}-{self.cantidad}"


class CLIENTES(models.Model):
    id_cliente=models.IntegerField(primary_key=True)
    nombre_cliente=models.CharField(max_length=50)
    apellido_cliente=models.CharField(max_length=50)
    telefono_cliente=models.CharField(max_length=20)
    dui_cliente=models.CharField(max_length=15)
    correo_cliente=models.CharField(max_length=30)
    def __str__(self):
        return f"ID:{self.id_cliente}-{self.nombre_cliente}"

class VENTAS(models.Model):
    id_venta=models.IntegerField(primary_key=True)
    num_factura_venta=models.CharField(max_length=10)
    fecha_venta=models.DateField(default=date.today)
    total=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    cliente=models.ForeignKey(CLIENTES,on_delete=models.CASCADE,to_field='id_cliente')
    empleado=models.ForeignKey(EMPLEADOS,on_delete=models.CASCADE,to_field='id_empleado')
    def __str__(self):
        return f"ID:{self.id_venta}-{self.num_factura_venta}"

class DETALLEVENTAS(models.Model):
    id_det_venta=models.IntegerField(primary_key=True)
    precio_unit=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    cantidad=models.IntegerField()
    subtotal=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    venta=models.ForeignKey(VENTAS,on_delete=models.CASCADE,to_field='id_venta')
    producto=models.ForeignKey(PRODUCTO,on_delete=models.CASCADE,to_field='id_prod')
    def __str__(self):
        return f"ID:{self.id_det_venta}-{self.producto}"






