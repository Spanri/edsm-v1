# Generated by Django 2.2.1 on 2019-06-16 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20190616_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_get_notif_expired_email',
            new_name='is_get_block',
        ),
    ]
