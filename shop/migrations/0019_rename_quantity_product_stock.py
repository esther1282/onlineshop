# Generated by Django 3.2.13 on 2022-06-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_product_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='stock',
        ),
    ]
