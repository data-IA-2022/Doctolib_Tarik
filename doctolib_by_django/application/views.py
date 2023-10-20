from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
        # Extract data from the request.POST dictionary
        patient_id = request.user.id
        print("patient id : " + str(patient_id))
        date_remplissage = datetime.date.today()  # Import 'datetime' for this
        periodicite_jours = 30
        is_late = False # Change this to the actual field name
        poids = request.POST.get("poids")
        tour_de_taille_cm = request.POST.get("tour_de_taille_cm")
        frequence_cardiaque_min = request.POST.get("frequence_cardiaque_min")
        tension_arterielle_systolique_matin = request.POST.get("tension_arterielle_systolique_matin")
        tension_arterielle_systolique_soir = request.POST.get("tension_arterielle_systolique_soir")
        tension_arterielle_diastolique_matin = request.POST.get("tension_arterielle_diastolique_matin")
        tension_arterielle_diastolique_soir = request.POST.get("tension_arterielle_diastolique_soir")
        symptomes_cardiovasculaires = request.POST.get("symptomes_cardiovasculaires")
        nb_medicaments_jour = request.POST.get("nb_medicaments_jour")
        oublie_medicament_matin = request.POST.get("oublie_medicament_matin") == "True"
        oublie_medicament_soir = request.POST.get("oublie_medicament_soir") == "True"
        effets_secondaires = request.POST.get("effets_secondaires") == "True"
        symptomes_particuliers = request.POST.get("symptomes_particuliers") == "True"
        consommation_alcool = request.POST.get("consommation_alcool") == "True"
        grignotage_sucre = request.POST.get("grignotage_sucre") == "True"
        grignotage_sale = request.POST.get("grignotage_sale") == "True"
        nb_repas_jour = request.POST.get("nb_repas_jour")
        quantite_eau_litres = request.POST.get("quantite_eau_litres")
        quantite_alcool_litres = request.POST.get("quantite_alcool_litres")
        activite_physique = request.POST.get("activite_physique") == "True"
        nature_activite_physique = request.POST.get("nature_activite_physique")
        duree_activite_physique_min = request.POST.get("duree_activite_physique_min")
        dyspnee = request.POST.get("dyspnee") == "True"
        oedeme = request.POST.get("oedeme") == "True"
        pre_episode_ir = request.POST.get("pre_episode_ir") == "True"
        fievre = request.POST.get("fievre") == "True"
        palpitation = request.POST.get("palpitation") == "True"
        douleur_thoracique = request.POST.get("douleur_thoracique") == "True"
        malaise = request.POST.get("malaise") == "True"
        heure_debut_palpitations_str = request.POST.get("heure_debut_palpitations")
        heure_debut_palpitations = datetime.datetime.strptime(heure_debut_palpitations_str, '%H:%M').time() if heure_debut_palpitations_str else None

        duree_total_palpitations_min = request.POST.get("duree_total_palpitations_min")
        heure_debut_douleurs_thoraciques_str = request.POST.get("heure_debut_douleurs_thoraciques")
        heure_debut_douleurs_thoraciques = datetime.datetime.strptime(heure_debut_douleurs_thoraciques_str, '%H:%M').time() if heure_debut_douleurs_thoraciques_str else None

        duree_total_douleurs_thoraciques_min = request.POST.get("duree_total_douleurs_thoraciques_min")
        
        heure_debut_malaises_str = request.POST.get("heure_debut_malaises")
        heure_debut_malaises = datetime.datetime.strptime(heure_debut_malaises_str, '%H:%M').time() if heure_debut_malaises_str else None
        
        duree_total_malaises_min = request.POST.get("duree_total_malaises_min")
        natremie_mmol_per_l = request.POST.get("natremie_mmol_per_l")
        potassium_mmol_per_l = request.POST.get("potassium_mmol_per_l")
        creatinine_umol_per_l = request.POST.get("creatinine_umol_per_l")
        clairance_creatinine_ml_per_min = request.POST.get("clairance_creatinine_ml_per_min")
        nt_probnp_ng_per_l = request.POST.get("nt_probnp_ng_per_l")
        fer_serique_mg_per_l = request.POST.get("fer_serique_mg_per_l")
        hemoglobine_g_per_100_ml = request.POST.get("hemoglobine_g_per_100_ml")
        vitesse_sedimentation_mm = request.POST.get("vitesse_sedimentation_mm")
        proteine_c_reactive_mg_per_l = request.POST.get("proteine_c_reactive_mg_per_l")
        troponine_ug_per_l = request.POST.get("troponine_ug_per_l")
        vitamine_d_ng_per_ml = request.POST.get("vitamine_d_ng_per_ml")
        acide_urique_mg_per_l = request.POST.get("acide_urique_mg_per_l")
        inr = request.POST.get("inr")
        
        # Create an instance of the model and save it
        form_data = FormulaireSante(
            patient_id=patient_id,
            date_remplissage=date_remplissage,
            periodicite_jours=periodicite_jours,
            is_late=is_late,
            poids=poids,
            tour_de_taille_cm=tour_de_taille_cm,
            frequence_cardiaque_min=frequence_cardiaque_min,
            tension_arterielle_systolique_matin=tension_arterielle_systolique_matin,
            tension_arterielle_systolique_soir=tension_arterielle_systolique_soir,
            tension_arterielle_diastolique_matin=tension_arterielle_diastolique_matin,
            tension_arterielle_diastolique_soir=tension_arterielle_diastolique_soir,
            symptomes_cardiovasculaires=symptomes_cardiovasculaires,
            nb_medicaments_jour=nb_medicaments_jour,
            oublie_medicament_matin=oublie_medicament_matin,
            oublie_medicament_soir=oublie_medicament_soir,
            effets_secondaires=effets_secondaires,
            symptomes_particuliers=symptomes_particuliers,
            consommation_alcool=consommation_alcool,
            grignotage_sucre=grignotage_sucre,
            grignotage_sale=grignotage_sale,
            nb_repas_jour=nb_repas_jour,
            quantite_eau_litres=quantite_eau_litres,
            quantite_alcool_litres=quantite_alcool_litres,
            activite_physique=activite_physique,
            nature_activite_physique=nature_activite_physique,
            duree_activite_physique_min=duree_activite_physique_min,
            dyspnee=dyspnee,
            oedeme=oedeme,
            pre_episode_ir=pre_episode_ir,
            fievre=fievre,
            palpitation=palpitation,
            douleur_thoracique=douleur_thoracique,
            malaise=malaise,
            heure_debut_palpitations=heure_debut_palpitations,
            duree_total_palpitations_min=duree_total_palpitations_min,
            heure_debut_douleurs_thoraciques=heure_debut_douleurs_thoraciques,
            duree_total_douleurs_thoraciques_min=duree_total_douleurs_thoraciques_min,
            heure_debut_malaises=heure_debut_malaises,
            duree_total_malaises_min=duree_total_malaises_min,
            natremie_mmol_per_l=natremie_mmol_per_l,
            potassium_mmol_per_l=potassium_mmol_per_l,
            creatinine_umol_per_l=creatinine_umol_per_l,
            clairance_creatinine_ml_per_min=clairance_creatinine_ml_per_min,
            nt_probnp_ng_per_l=nt_probnp_ng_per_l,
            fer_serique_mg_per_l=fer_serique_mg_per_l,
            hemoglobine_g_per_100_ml=hemoglobine_g_per_100_ml,
            vitesse_sedimentation_mm=vitesse_sedimentation_mm,
            proteine_c_reactive_mg_per_l=proteine_c_reactive_mg_per_l,
            troponine_ug_per_l=troponine_ug_per_l,
            vitamine_d_ng_per_ml=vitamine_d_ng_per_ml,
            acide_urique_mg_per_l=acide_urique_mg_per_l,
            inr=inr,
        )
        form_data.save()
        return HttpResponse('Formulaire envoyé')
    else:
        form = FormulaireSanteForm()

    return render(request, 'form_sante.html', {'form': form})

