# Generated by Django 4.2.5 on 2023-10-20 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_alter_formulairesante_poids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulairesante',
            name='poids',
            field=models.FloatField(default=float("nan")),
        ),
    ]