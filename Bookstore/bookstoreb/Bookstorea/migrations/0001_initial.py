# Generated by Django 5.0.7 on 2024-09-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGORIA',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=200)),
            ],
        ),
    ]