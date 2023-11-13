# Generated by Django 4.2.5 on 2023-10-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_formulairesante_acide_urique_mg_per_l_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulairesante',
            name='acide_urique_mg_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='clairance_creatinine_ml_per_min',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='creatinine_umol_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='date_remplissage',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='duree_activite_physique_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='duree_total_douleurs_thoraciques_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='duree_total_malaises_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='duree_total_palpitations_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='fer_serique_mg_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='frequence_cardiaque_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='hemoglobine_g_per_100_ml',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='heure_debut_douleurs_thoraciques',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='heure_debut_malaises',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='heure_debut_palpitations',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='inr',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='natremie_mmol_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='nature_activite_physique',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='nb_medicaments_jour',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='nb_repas_jour',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='nt_probnp_ng_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='periodicite_jours',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='poids',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='potassium_mmol_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='proteine_c_reactive_mg_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='quantite_alcool_litres',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='quantite_eau_litres',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='symptomes_cardiovasculaires',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='symptomes_particuliers',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='tension_arterielle_diastolique_matin',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='tension_arterielle_diastolique_soir',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='tension_arterielle_systolique_matin',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='tension_arterielle_systolique_soir',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='tour_de_taille_cm',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='troponine_ug_per_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='vitamine_d_ng_per_ml',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='formulairesante',
            name='vitesse_sedimentation_mm',
            field=models.FloatField(null=True),
        ),
    ]