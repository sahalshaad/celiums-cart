# Generated by Django 5.2.1 on 2025-07-03 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_country_order_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='lirst_name',
            new_name='last_name',
        ),
    ]
