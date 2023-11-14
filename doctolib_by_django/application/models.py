from django.db import models
from authentification.models import Utilisateurs
import numpy as np
# Create your models here.

# # User Model
# class Utilisateurs(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)

# Association Table between Medecins and Patients
class MedecinPatient(models.Model):
    medecin = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name='comptes_medecin', limit_choices_to={'role': 'medecin'})
    patient = models.ManyToManyField(Utilisateurs, through='MedecinPatientAssociation', related_name='medecins', limit_choices_to={'role': 'patient'})
    is_admin_validation = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'MedecinPatient'

class MedecinPatientAssociation(models.Model):
    medecin = models.ForeignKey(MedecinPatient, on_delete=models.CASCADE)
    patient = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    periodicite = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'MedecinPatient_association'  # Your explicit table name

# Association Table between Admins and Medecins
class AdminCompte(models.Model):
    admin = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name='comptes_admin', limit_choices_to={'role': 'admin'})
    users = models.ManyToManyField(Utilisateurs, related_name='admins', limit_choices_to={'role__in': ['admin', 'medecin', 'patient']})
    
    class Meta:
        db_table = 'AdminCompte'



# Health Form Model

class FormulaireSante(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name='formulaires_santé')
    date_remplissage = models.DateField(null=True)
    periodicite_jours = models.IntegerField(null=True)
    is_late = models.BooleanField(default=False)
    is_early = models.BooleanField(default=False)
    poids = models.FloatField(default=np.nan)
    tour_de_taille_cm = models.FloatField(default=0.0, null=True)
    frequence_cardiaque_min = models.IntegerField(default=0.0, null=True)
    tension_arterielle_systolique_matin = models.FloatField(null=True)
    tension_arterielle_systolique_soir = models.FloatField(null=True)
    tension_arterielle_diastolique_matin = models.FloatField(null=True)
    tension_arterielle_diastolique_soir = models.FloatField(null=True)
    symptomes_cardiovasculaires = models.TextField(null=True)
    nb_medicaments_jour = models.IntegerField(null=True)
    oublie_medicament_matin = models.BooleanField(default=False)
    oublie_medicament_soir = models.BooleanField(default=False)
    effets_secondaires = models.BooleanField(default=False)
    symptomes_particuliers = models.TextField(null=True)
    consommation_alcool = models.BooleanField(default=False)
    grignotage_sucre = models.BooleanField(default=False)
    grignotage_sale = models.BooleanField(default=False)
    nb_repas_jour = models.IntegerField(null=True)
    quantite_eau_litres = models.FloatField(null=True)
    quantite_alcool_litres = models.FloatField(null=True)
    activite_physique = models.BooleanField(default=False)
    nature_activite_physique = models.TextField(null=True)
    duree_activite_physique_min = models.IntegerField(null=True)
    dyspnee = models.BooleanField(default=False)
    oedeme = models.BooleanField(default=False)
    pre_episode_ir = models.BooleanField(default=False)
    fievre = models.BooleanField(default=False)
    palpitation = models.BooleanField(default=False)
    douleur_thoracique = models.BooleanField(default=False)
    malaise = models.BooleanField(default=False)
    heure_debut_palpitations = models.TimeField(null=True)
    duree_total_palpitations_min = models.IntegerField(null=True)
    heure_debut_douleurs_thoraciques = models.TimeField(null=True)
    duree_total_douleurs_thoraciques_min = models.IntegerField(null=True)
    heure_debut_malaises = models.TimeField(null=True)
    duree_total_malaises_min = models.IntegerField(null=True)
    natremie_mmol_per_l = models.FloatField(null=True)
    potassium_mmol_per_l = models.FloatField(null=True)
    creatinine_umol_per_l = models.FloatField(null=True)
    clairance_creatinine_ml_per_min = models.FloatField(null=True)
    nt_probnp_ng_per_l = models.FloatField(null=True)
    fer_serique_mg_per_l = models.FloatField(null=True)
    hemoglobine_g_per_100_ml = models.FloatField(null=True)
    vitesse_sedimentation_mm = models.FloatField(null=True)
    proteine_c_reactive_mg_per_l = models.FloatField(null=True)
    troponine_ug_per_l = models.FloatField(null=True)
    vitamine_d_ng_per_ml = models.FloatField(null=True)
    acide_urique_mg_per_l = models.FloatField(null=True)
    inr = models.FloatField(null=True)
    
    class Meta:
        db_table = 'FormulaireSante'

# Stress Evaluation Model
class FormulaireEvalStress(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name='formulaires_eval_stress')
    date_remplissage = models.DateField()
    periodicite_jours = models.IntegerField()
    is_late = models.BooleanField(default=False)
    is_early = models.BooleanField(default=False)
    irritabilite = models.IntegerField()
    sentiments_depressifs = models.IntegerField()
    bouche_seche_gorge_seche = models.IntegerField()
    actions_gestes_impulsifs = models.IntegerField()
    grincement_dents = models.IntegerField()
    difficulte_rester_assis = models.IntegerField()
    cauchemars = models.IntegerField()
    diarrhee = models.IntegerField()
    attaques_verbales = models.IntegerField()
    hauts_bas_emotifs = models.IntegerField()
    grande_envie_de_pleurer = models.IntegerField()
    grande_envie_de_fuir = models.IntegerField()
    grande_envie_de_faire_mal = models.IntegerField()
    pensees_embrouillees = models.IntegerField()
    debit_plus_rapide = models.IntegerField()
    fatigue_lourdeur_generalisees = models.IntegerField()
    sentiment_surcharge = models.IntegerField()
    sentiment_emotionnellement_fragile = models.IntegerField()
    sentiment_tristesse = models.IntegerField()
    sentiment_anxiete = models.IntegerField()
    tension_emotionnelle = models.IntegerField()
    hostilite_vers_autres = models.IntegerField()
    tremblements_gestes_nerveux = models.IntegerField()
    begaiements_hesitations_verbales = models.IntegerField()
    incapacite_difficulte_concentrer = models.IntegerField()
    difficulte_organiser_pensees = models.IntegerField()
    difficulte_dormir_nuit_sans_reveiller = models.IntegerField()
    besoin_frequent_uriner = models.IntegerField()
    maux_estomac_difficultes_digerer = models.IntegerField()
    geste_sentiment_impatience = models.IntegerField()
    maux_tete = models.IntegerField()
    douleurs_dos_nuque = models.IntegerField()
    perte_gain_appetit = models.IntegerField()
    perte_interet_sexe = models.IntegerField()
    oublis_frequents = models.IntegerField()
    douleurs_serrements_poitrine = models.IntegerField()
    conflits_significatifs_avec_autres = models.IntegerField()
    difficulte_lever_apres_sommeil = models.IntegerField()
    sentiment_choses_hors_de_controle = models.IntegerField()
    difficulte_longue_activite_continue = models.IntegerField()
    mouvements_retrait_isolement = models.IntegerField()
    difficulte_s_endormir = models.IntegerField()
    difficulte_se_remettre_evenement_contrariant = models.IntegerField()
    mains_moites = models.IntegerField()
    total_impact_stress = models.IntegerField()
    
    class Meta:
        db_table = 'FormulaireEvalStress'