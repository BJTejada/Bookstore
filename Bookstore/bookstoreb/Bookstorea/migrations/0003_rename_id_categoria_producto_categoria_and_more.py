# Generated by Django 5.0.7 on 2024-09-15 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bookstorea', '0002_categorias_producto_proveedores_delete_categoria_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='id_categoria',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='id_proveedor',
            new_name='proveedor',
        ),
    ]
