# Generated by Django 4.2.5 on 2023-10-20 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_alter_formulairesante_acide_urique_mg_per_l_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulairesante',
            name='frequence_cardiaque_min',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
