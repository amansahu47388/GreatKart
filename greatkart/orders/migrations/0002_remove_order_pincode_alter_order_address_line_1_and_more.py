# Generated by Django 5.1.4 on 2025-01-09 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pincode',
        ),
        migrations.AlterField(
            model_name='order',
            name='address_line_1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]