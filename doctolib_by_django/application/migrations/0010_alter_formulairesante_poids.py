# Generated by Django 4.2.5 on 2023-10-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_alter_formulairesante_tour_de_taille_cm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulairesante',
            name='poids',
            field=models.FloatField(blank=True, null=True),
        ),
    ]