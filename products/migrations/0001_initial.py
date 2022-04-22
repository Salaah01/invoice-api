# Generated by Django 4.0.4 on 2022-04-22 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'db_table': 'product_category',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.productcategory')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='suppliers.supplier')),
            ],
            options={
                'db_table': 'product',
                'ordering': ['name'],
                'unique_together': {('name', 'supplier')},
            },
        ),
    ]
