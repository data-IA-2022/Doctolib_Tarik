from django import forms
from .models import Utilisateurs, FormulaireSante, MedecinPatientAssociation

class AccountGenerationForm(forms.Form):
    num_accounts = forms.IntegerField(label='Number of Accounts', min_value=1)
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=[
            ('admin', 'Admin'),
            ('medecin', 'Medecin'),
            ('patient', 'Patient'),
        ],
        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    
class EmailAssociationForm(forms.Form):
    usernames = forms.ModelMultipleChoiceField(
        queryset=Utilisateurs.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        required=True,
    )
    email = forms.EmailField(label='Email', required=True)
    
###### formulaire santé #############

class FormulaireSanteForm(forms.ModelForm):
    class Meta:
        model = FormulaireSante
        fields = '__all__'

class PeriodiciteForm(forms.ModelForm):
    class Meta:
        model = MedecinPatientAssociation
        fields = ['periodicite']
        
class FormulaireSanteEditForm(forms.ModelForm):
    class Meta:
        model = FormulaireSante
        fields = [
            'poids', 
            'tour_de_taille_cm', 
            'frequence_cardiaque_min',
            'tension_arterielle_systolique_matin', 
            'tension_arterielle_systolique_soir', 
            'tension_arterielle_diastolique_matin', 
            'tension_arterielle_diastolique_soir', 
            'symptomes_cardiovasculaires', 
            'nb_medicaments_jour', 
            'oublie_medicament_matin', 
            'oublie_medicament_soir', 
            'effets_secondaires', 
            'symptomes_particuliers', 
            'consommation_alcool', 
            'grignotage_sucre', 
            'grignotage_sale', 
            'nb_repas_jour', 
            'quantite_eau_litres', 
            'quantite_alcool_litres', 
            'activite_physique', 
            'nature_activite_physique', 
            'duree_activite_physique_min', 
            'dyspnee', 
            'oedeme', 
            'pre_episode_ir', 
            'fievre', 
            'palpitation', 
            'douleur_thoracique', 
            'malaise', 
            'heure_debut_palpitations', 
            'duree_total_palpitations_min', 
            'heure_debut_douleurs_thoraciques', 
            'duree_total_douleurs_thoraciques_min', 
            'heure_debut_malaises', 
            'duree_total_malaises_min', 
            'natremie_mmol_per_l', 
            'potassium_mmol_per_l', 
            'creatinine_umol_per_l', 
            'clairance_creatinine_ml_per_min', 
            'nt_probnp_ng_per_l', 
            'fer_serique_mg_per_l', 
            'hemoglobine_g_per_100_ml', 
            'vitesse_sedimentation_mm', 
            'proteine_c_reactive_mg_per_l', 
            'troponine_ug_per_l', 
            'vitamine_d_ng_per_ml', 
            'acide_urique_mg_per_l', 
            'inr'
        ]
    def __init__(self, *args, **kwargs):
        super(FormulaireSanteEditForm, self).__init__(*args, **kwargs)
        
        # Set all fields to not required
        for field_name in self.fields:
            self.fields[field_name].required = False 