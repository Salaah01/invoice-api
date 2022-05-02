# Generated by Django 4.0.4 on 2022-05-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_invoiceitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='price_ex_vat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
