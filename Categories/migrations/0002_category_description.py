# Generated by Django 4.2.1 on 2023-11-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]