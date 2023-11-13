from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_time
from .forms import AccountGenerationForm, EmailAssociationForm, FormulaireSanteForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib import messages
from authentification.models import Utilisateurs
from .models import AdminCompte, MedecinPatient
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
 
import datetime

from application.models import FormulaireSante



# Create your views here.
@login_required
def accueil(request):
    # prenom = request.user.username
    # role = "superuser" if request.user.is_superuser else request.user.role
    return render(request, "accueil.html")

@login_required
def menu(request):
    return render(request, "menu.html")

@login_required
def historique(request):
     # Je récupère les champs de la table formulaire santé
    champsFormulaireSante = [field.name for field in FormulaireSante._meta.get_fields()]
    # Je récupère les ids des lignes de la table formulaire santé
    idDesFormulaires = [valeur.id for valeur in FormulaireSante.objects.all()]
    # Je crée une liste qui contiendra les valeurs des lignes
    # Il y a autant d'élément que de ligne, donc que d'ids récupéré
    # FormulaireSante.objects.filter(id=id).values()[0].values()
    # Dans le code ci-dessus je récupère la ligne ayant un certain id
    # Ensuite je récupère les valeurs de la ligne .values
    # Le 1er élément qui est le dictionnaire des colonnes/valeurs
    # et enfin uniquement les valeurs
    dataFormulaireSante = [FormulaireSante.objects.filter(id=id).values()[0].values() for id in idDesFormulaires]    
    return render(request, "historique.html",{"dataFormulaireSante" : dataFormulaireSante,
                   "champsFormulaireSante" : champsFormulaireSante})

@login_required
def edaia(request):
    if request.user.role != "medecin":
        return redirect("https://media.tenor.com/2euSOQYdz8oAAAAj/this-was-technically-illegal-maclen-stanley.gif")
    else:
        return render(request, "edaia.html")
    

@login_required
def comptes(request):
    if request.user.is_superuser != 1:
        return redirect("https://media.tenor.com/2euSOQYdz8oAAAAj/this-was-technically-illegal-maclen-stanley.gif")
    else:
        if request.method == 'POST':
            form = AccountGenerationForm(request.POST)
            if form.is_valid():
                num_accounts = form.cleaned_data['num_accounts']
                account_type = form.cleaned_data['account_type']
                
                # Find the highest existing ID for the specified account type
                existing_accounts = Utilisateurs.objects.filter(username__startswith=account_type[0].upper())
                if existing_accounts.exists():
                    highest_id = max(int(account.username[1:]) for account in existing_accounts)
                else:
                    highest_id = 1000

                created_accounts = []

                for i in range(num_accounts):
                    # Generate a unique username based on the account type and the highest existing ID
                    username = f'{account_type.upper()[0]}{highest_id + i + 1}'
                    role = account_type

                    # Password can be set as username + a default value, change as needed
                    password = f'{username}MDP'

                    # Create the user account
                    nouveauCompte = Utilisateurs.objects.create_user(username=username, password=password, role=role)
                    created_accounts.append(nouveauCompte)
                
                messages.success(request, f'{num_accounts} {account_type} account(s) created successfully.')
                # Fetch user accounts that need activation (customize this filter as needed)
                selected_accounts = Utilisateurs.objects.filter(needs_activation=True)
                return render(request, 'comptes.html', {'form': form, 'created_accounts': created_accounts, 'selected_accounts': selected_accounts})
        else:
            form = AccountGenerationForm()
    
    return render(request, 'comptes.html', {'form': form})
  
@login_required
def associationAdminsComptes(request):
    admins = Utilisateurs.objects.filter(role="admin")
    users_not_assigned = Utilisateurs.objects.exclude(role="admin").exclude(admins__isnull=False).exclude(is_superuser=True)
    admin_associations = AdminCompte.objects.all()
    
    if request.method == "POST":
        admin_ids = request.POST.getlist("admins")
        user_ids = request.POST.getlist("users")
        
        # Associate selected admins with selected users
        for admin_id in admin_ids:
            admin = Utilisateurs.objects.get(id=admin_id)
            for user_id in user_ids:
                user = Utilisateurs.objects.get(id=user_id)
                admin_compte, created = AdminCompte.objects.get_or_create(admin=admin)
                admin_compte.users.add(user)
        
        return redirect("associationAdminsComptes")
    
    return render(request, "associationAdminsComptes.html", {
        "admins": admins,
        "users_not_assigned": users_not_assigned,
        "admin_associations": admin_associations,
    })
    
@login_required
def associationMedecinPatient(request):
    medecins = Utilisateurs.objects.filter(role="medecin")
    patients = Utilisateurs.objects.filter(role="patient")
    medecin_patient_associations = MedecinPatient.objects.all()
    
    if request.method == "POST":
        medecin_id = request.POST["medecin"]
        patient_ids = request.POST.getlist("patients")
        print("Medecin ID:", medecin_id)
        print("Patient IDs:", patient_ids)

        # Get the selected medic
        medic = Utilisateurs.objects.get(id=medecin_id)
        print(medic)

        # Associate the selected patients with the medic
        medecin_patient, created = MedecinPatient.objects.get_or_create(medecin=medic)
        for patient_id in patient_ids:
            patient = Utilisateurs.objects.get(id=patient_id)
            medecin_patient.patient.add(patient)
        
        return redirect("associationMedecinPatient")

    return render(request, "associationMedecinPatient.html", {
        "medecins": medecins,
        "patients": patients,
        "medecin_patient_associations": medecin_patient_associations,
    })


########## Formulaire de santé multi step ############################

# @login_required
# def form_sante(request):
    
#     return render(request, "form_sante.html")
@login_required
def formulaire_sante_gen(request):
    if request.method == 'POST':
        # Helper function to convert field values
        def convert_field_value(value, field_type):
            if value.strip() == '':
                if field_type in ['int', 'float']:
                    return None
                elif field_type == 'bool':
                    return False
                return ''
            if field_type == 'int':
                return int(value)
            elif field_type == 'float':
                return float(value)
            elif field_type == 'bool':
                return value == 'True'
            return value

        # Function to parse time fields
        def parse_time_field(field_value):
            if field_value.strip():
                try:
                    return parse_time(field_value)
                except ValueError:
                    return None
            return None
        
        # Process each field from the form
        form_data = {
            'patient_id': request.user.id,
            'date_remplissage': datetime.date.today(),
            'periodicite_jours': 30,
            'is_late': False,  # Assuming this is a mandatory field with a default value
            'poids': convert_field_value(request.POST.get("poids", ''), 'float'),
            'tour_de_taille_cm': convert_field_value(request.POST.get("tour_de_taille_cm", ''), 'float'),
            'frequence_cardiaque_min': convert_field_value(request.POST.get("frequence_cardiaque_min", ''), 'int'),
            'tension_arterielle_systolique_matin': convert_field_value(request.POST.get("tension_arterielle_systolique_matin", ''), 'float'),
            'tension_arterielle_systolique_soir': convert_field_value(request.POST.get("tension_arterielle_systolique_soir", ''), 'float'),
            'tension_arterielle_diastolique_matin': convert_field_value(request.POST.get("tension_arterielle_diastolique_matin", ''), 'float'),
            'tension_arterielle_diastolique_soir': convert_field_value(request.POST.get("tension_arterielle_diastolique_soir", ''), 'float'),
            'symptomes_cardiovasculaires': request.POST.get("symptomes_cardiovasculaires", ''),
            'nb_medicaments_jour': convert_field_value(request.POST.get("nb_medicaments_jour", ''), 'int'),
            'oublie_medicament_matin': convert_field_value(request.POST.get("oublie_medicament_matin", ''), 'bool'),
            'oublie_medicament_soir': convert_field_value(request.POST.get("oublie_medicament_soir", ''), 'bool'),
            'effets_secondaires': convert_field_value(request.POST.get("effets_secondaires", ''), 'bool'),
            'symptomes_particuliers': request.POST.get("symptomes_particuliers", ''),
            'consommation_alcool': convert_field_value(request.POST.get("consommation_alcool", ''), 'bool'),
            'grignotage_sucre': convert_field_value(request.POST.get("grignotage_sucre", ''), 'bool'),
            'grignotage_sale': convert_field_value(request.POST.get("grignotage_sale", ''), 'bool'),
            'nb_repas_jour': convert_field_value(request.POST.get("nb_repas_jour", ''), 'int'),
            'quantite_eau_litres': convert_field_value(request.POST.get("quantite_eau_litres", ''), 'float'),
            'quantite_alcool_litres': convert_field_value(request.POST.get("quantite_alcool_litres", ''), 'float'),
            'activite_physique': convert_field_value(request.POST.get("activite_physique", ''), 'bool'),
            'nature_activite_physique': request.POST.get("nature_activite_physique", ''),
            'duree_activite_physique_min': convert_field_value(request.POST.get("duree_activite_physique_min", ''), 'int'),
            'dyspnee': convert_field_value(request.POST.get("dyspnee", ''), 'bool'),
            'oedeme': convert_field_value(request.POST.get("oedeme", ''), 'bool'),
            'pre_episode_ir': convert_field_value(request.POST.get("pre_episode_ir", ''), 'bool'),
            'fievre': convert_field_value(request.POST.get("fievre", ''), 'bool'),
            'palpitation': convert_field_value(request.POST.get("palpitation", ''), 'bool'),
            'douleur_thoracique': convert_field_value(request.POST.get("douleur_thoracique", ''), 'bool'),
            'malaise': convert_field_value(request.POST.get("malaise", ''), 'bool'),
            'heure_debut_palpitations': parse_time_field(request.POST.get("heure_debut_palpitations", '')),
            'duree_total_palpitations_min': convert_field_value(request.POST.get("duree_total_palpitations_min", ''), 'int'),
            'heure_debut_douleurs_thoraciques': parse_time_field(request.POST.get("heure_debut_douleurs_thoraciques", '')),
            'duree_total_douleurs_thoraciques_min': convert_field_value(request.POST.get("duree_total_douleurs_thoraciques_min", ''), 'int'),
            'heure_debut_malaises': parse_time_field(request.POST.get("heure_debut_malaises", '')),
            'duree_total_malaises_min': convert_field_value(request.POST.get("duree_total_malaises_min", ''), 'int'),
            'natremie_mmol_per_l': convert_field_value(request.POST.get("natremie_mmol_per_l", ''), 'float'),
            'potassium_mmol_per_l': convert_field_value(request.POST.get("potassium_mmol_per_l", ''), 'float'),
            'creatinine_umol_per_l': convert_field_value(request.POST.get("creatinine_umol_per_l", ''), 'float'),
            'clairance_creatinine_ml_per_min': convert_field_value(request.POST.get("clairance_creatinine_ml_per_min", ''), 'float'),
            'nt_probnp_ng_per_l': convert_field_value(request.POST.get("nt_probnp_ng_per_l", ''), 'float'),
            'fer_serique_mg_per_l': convert_field_value(request.POST.get("fer_serique_mg_per_l", ''), 'float'),
            'hemoglobine_g_per_100_ml': convert_field_value(request.POST.get("hemoglobine_g_per_100_ml", ''), 'float'),
            'vitesse_sedimentation_mm': convert_field_value(request.POST.get("vitesse_sedimentation_mm", ''), 'float'),
            'proteine_c_reactive_mg_per_l': convert_field_value(request.POST.get("proteine_c_reactive_mg_per_l", ''), 'float'),
            'troponine_ug_per_l': convert_field_value(request.POST.get("troponine_ug_per_l", ''), 'float'),
            'vitamine_d_ng_per_ml': convert_field_value(request.POST.get("vitamine_d_ng_per_ml", ''), 'float'),
            'acide_urique_mg_per_l': convert_field_value(request.POST.get("acide_urique_mg_per_l", ''), 'float'),
            'inr': convert_field_value(request.POST.get("inr", ''), 'float'),
        }

        # Create and save the model instance
        formulaire_sante = FormulaireSante(**form_data)
        formulaire_sante.save()

        return HttpResponse('Formulaire envoyé')

    else:
        form = FormulaireSanteForm()

    return render(request, 'form_sante.html', {'form': form})

