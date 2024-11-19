# Generated by Django 5.0.7 on 2024-09-15 23:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookstorea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGORIAS',
            fields=[
                ('id_categ', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('nombre_categ', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PRODUCTO',
            fields=[
                ('id_prod', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_prod', models.CharField(max_length=200)),
                ('marca_prod', models.CharField(max_length=50)),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.categorias')),
            ],
        ),
        migrations.CreateModel(
            name='PROVEEDORES',
            fields=[
                ('id_prov', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_prov', models.CharField(max_length=200)),
                ('telefono_prov', models.CharField(max_length=50)),
                ('direccion_prov', models.CharField(max_length=200)),
                ('correo_prov', models.CharField(max_length=80)),
            ],
        ),
        migrations.DeleteModel(
            name='CATEGORIA',
        ),
        migrations.AddField(
            model_name='producto',
            name='id_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookstorea.proveedores'),
        ),
    ]