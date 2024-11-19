# Generated by Django 5.0.7 on 2024-09-18 21:30

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookstorea', '0003_rename_id_categoria_producto_categoria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLIENTES',
            fields=[
                ('id_cliente', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(max_length=50)),
                ('apellido_cliente', models.CharField(max_length=50)),
                ('telefono_cliente', models.CharField(max_length=20)),
                ('dui_cliente', models.CharField(max_length=15)),
                ('correo_cliente', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='COMPRAS',
            fields=[
                ('id_compra', models.IntegerField(primary_key=True, serialize=False)),
                ('num_factura', models.IntegerField(max_length=8)),
                ('fecha_compra', models.DateField(default=datetime.date.today)),
                ('total_compra', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='EMPLEADOS',
            fields=[
                ('id_empleado', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_empleado', models.CharField(max_length=80)),
                ('apellido', models.CharField(max_length=80)),
                ('telefono', models.CharField(max_length=15)),
                ('dui', models.CharField(max_length=15)),
                ('correo_cliente', models.CharField(max_length=80)),
                ('estado', models.IntegerField()),
                ('fechaingreso', models.DateField(default=datetime.date.today)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ROLES',
            fields=[
                ('id_rol', models.IntegerField(primary_key=True, serialize=False)),
                ('tipo_rol', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='USUARIOS',
            fields=[
                ('id_usuario', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_usuario', models.CharField(max_length=20)),
                ('psw_usuario', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='DETALLECOMPRA',
            fields=[
                ('id_det_compra', models.IntegerField(primary_key=True, serialize=False)),
                ('precio_unit_compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.IntegerField()),
                ('total_det_compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.compras')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.producto')),
            ],
        ),
        migrations.AddField(
            model_name='compras',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.empleados'),
        ),
        migrations.CreateModel(
            name='LOTES',
            fields=[
                ('id_lote', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_entrada', models.DateField(default=datetime.date.today)),
                ('cantidad', models.IntegerField()),
                ('fecha_caducidad', models.DateField()),
                ('precio_venta', models.IntegerField()),
                ('detalle_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.detallecompra')),
            ],
        ),
        migrations.AddField(
            model_name='empleados',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.roles'),
        ),
        migrations.AddField(
            model_name='empleados',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.usuarios'),
        ),
        migrations.CreateModel(
            name='VENTAS',
            fields=[
                ('id_venta', models.IntegerField(primary_key=True, serialize=False)),
                ('num_factura_venta', models.CharField(max_length=10)),
                ('fecha_venta', models.DateField(default=datetime.date.today)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.clientes')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.empleados')),
            ],
        ),
        migrations.CreateModel(
            name='DETALLEVENTAS',
            fields=[
                ('id_det_venta', models.IntegerField(primary_key=True, serialize=False)),
                ('precio_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.ventas')),
            ],
        ),
    ]