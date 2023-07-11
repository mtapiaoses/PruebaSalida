# Generated by Django 4.2.3 on 2023-07-11 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_total', models.IntegerField(null=True)),
                ('precio_total', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
                ('descripcion', models.CharField(max_length=255)),
                ('imagen_b', models.BinaryField()),
                ('imagen_f', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('calle_entrega', models.CharField(max_length=200)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.carrito')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.comuna')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.estadopedido')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.region')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=200, unique=True)),
                ('direccion', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=100)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('permiso_empleado', 'puede acceder a las intefaces del empleado')],
            },
        ),
        migrations.CreateModel(
            name='DetalleProductoSocilicitado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_producto', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.carrito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=200, unique=True)),
                ('direccion', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=100)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('permiso_cliente', 'puede acceder a las intefaces del cliente')],
            },
        ),
        migrations.AddField(
            model_name='carrito',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.cliente'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='empleado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.empleado'),
        ),
    ]
