# Generated by Django 4.1.5 on 2023-01-29 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='counrty',
            new_name='country',
        ),
    ]
