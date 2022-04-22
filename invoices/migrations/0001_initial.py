# Generated by Django 4.0.4 on 2022-04-22 20:54

from django.db import migrations, models
import django.db.models.deletion
import invoices.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order_number', models.CharField(blank=True, max_length=32, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=7)),
                ('vat', models.DecimalField(decimal_places=2, max_digits=7)),
                ('delivery', models.DecimalField(decimal_places=2, max_digits=7)),
                ('promotion', models.DecimalField(decimal_places=2, max_digits=7)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('attachment', models.FileField(blank=True, null=True, upload_to=invoices.models.invoice_upload_path)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='suppliers.supplier')),
            ],
            options={
                'db_table': 'invoice',
                'ordering': ['-date_ordered'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price_ex_vat', models.DecimalField(decimal_places=2, max_digits=7)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='invoices.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
        ),
    ]
