# Generated by Django 3.2.5 on 2021-09-08 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
