# Generated by Django 2.2 on 2019-06-01 02:48

from django.db import migrations, models
import django_auth.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0008_auto_20190601_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='file',
            field=models.FileField(blank=True, null=True, storage=django_auth.storage_backends.MediaStorage(), upload_to=''),
        ),
    ]
