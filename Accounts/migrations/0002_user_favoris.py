# Generated by Django 4.2.1 on 2023-09-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favoris',
            field=models.ManyToManyField(blank=True, to='Products.product'),
        ),
    ]
