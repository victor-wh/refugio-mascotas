# Generated by Django 3.2.13 on 2022-05-04 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0002_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adopcion.persona'),
        ),
    ]