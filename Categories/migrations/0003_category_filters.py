# Generated by Django 4.2.1 on 2023-12-25 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Categories', '0002_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='filters',
            field=models.JSONField(default=list),
        ),
    ]
