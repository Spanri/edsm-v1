# Generated by Django 2.2 on 2019-05-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190504_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='position',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
