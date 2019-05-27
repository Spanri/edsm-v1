# Generated by Django 2.2 on 2019-05-27 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='media')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('common', models.BooleanField(default=False)),
                ('preview', models.ImageField(blank=True, upload_to='media')),
                ('signature', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
