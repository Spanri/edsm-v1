# Generated by Django 2.2 on 2019-05-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190518_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='owner',
            field=models.BooleanField(default=False),
        ),
    ]
