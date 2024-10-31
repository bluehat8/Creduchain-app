# Generated by Django 3.2.6 on 2024-10-31 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credential_hash', models.CharField(max_length=100, unique=True)),
                ('student_name', models.CharField(max_length=255)),
                ('student_id', models.CharField(max_length=50)),
                ('program', models.CharField(max_length=255)),
                ('graduation_date', models.DateField()),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]