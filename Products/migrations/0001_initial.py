# Generated by Django 4.2.1 on 2023-09-02 14:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, null=True)),
                ('visibility', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('payment_type', models.CharField(choices=[('UNIQ', 'Uniq'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], default='UNIQ', max_length=255)),
                ('images', models.JSONField(default=list)),
                ('status', models.CharField(choices=[('SOLD', 'Sold'), ('FOR_SALE', 'For sale'), ('EXCHANGED', 'Exchanged'), ('TO_EXCHANGE', 'To exchange'), ('REFUNDED', 'Refunded'), ('PENDING_REFUND', 'Pending_refund'), ('RESERVED', 'Reserved'), ('PENDING_PAYMENT', 'Pending_payment'), ('NEGOTIATING', 'Negotiating')], default='FOR_SALE', max_length=255)),
                ('condition', models.CharField(choices=[('MINT', 'Mint'), ('EXCELLENT', 'EXCELLENT'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('POOR', 'Poor')], max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Categories.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
