# Generated by Django 5.1.4 on 2025-01-13 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productgallery_reviewrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=1500),
        ),
    ]
