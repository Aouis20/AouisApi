# Generated by Django 4.2.1 on 2023-12-26 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_user_favoris'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='language',
        ),
        migrations.RemoveField(
            model_name='user',
            name='salutation',
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.JSONField(default=dict),
        ),
    ]
