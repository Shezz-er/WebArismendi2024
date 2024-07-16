# Generated by Django 4.1.2 on 2022-12-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0017_alter_producto_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servicio', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('numero', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
                ('mensaje', models.CharField(max_length=500)),
                ('imagen', models.ImageField(null=True, upload_to='media/imagenes/servicios/')),
            ],
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.FileField(upload_to='media/imagenes/productos/'),
        ),
    ]
