# Generated by Django 3.2.6 on 2024-10-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_credential_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='issuer_address',
            field=models.CharField(default='unknown', max_length=100, unique=True),
        ),
    ]