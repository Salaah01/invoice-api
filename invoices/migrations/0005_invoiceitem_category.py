# Generated by Django 4.0.4 on 2022-05-02 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_unique_together_and_more'),
        ('invoices', '0004_invoice_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productcategory'),
        ),
    ]
