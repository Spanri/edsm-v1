# Generated by Django 2.2.1 on 2019-06-17 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0018_auto_20190617_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='hash',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doc_h', to='docs.Block'),
        ),
    ]