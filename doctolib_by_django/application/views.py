from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_time
from .forms import AccountGenerationForm, EmailAssociationForm, FormulaireSanteForm, PeriodiciteForm, FormulaireSanteEditForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.forms.models import model_to_dict
from django.db.models import F

from django.contrib import messages
from authentification.models import Utilisateurs
from application.models import AdminCompte, MedecinPatient, FormulaireSante, MedecinPatientAssociation, AdminCompteAssociation
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
 
import datetime
from django.utils.dateparse import parse_date



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
    user_role = request.session.get('role')
    user_id = request.user.id

    champsFormulaireSante = [field.name for field in FormulaireSante._meta.get_fields()]

    # Initialize the form with no instance
    form = PeriodiciteForm()

    if request.method == 'POST':
        form = PeriodiciteForm(request.POST)
        if form.is_valid():
            periodicite = form.cleaned_data['periodicite']
            # Fetch all associations for the medecin and update periodicite
            associations = MedecinPatientAssociation.objects.filter(medecin__medecin_id=user_id)
            for association in associations:
                association.periodicite = periodicite
                association.save()
            return redirect('historique')

     # Fetch data based on user role
    if user_role in ['admin', 'superadmin']:
        queryset = FormulaireSante.objects.all()
    elif user_role == 'medecin':
        patient_ids = MedecinPatientAssociation.objects.filter(medecin__medecin_id=user_id).values_list('patient', flat=True)
        queryset = FormulaireSante.objects.filter(patient_id__in=patient_ids).annotate(patient_username=F('patient__username'))
    elif user_role == 'patient':
        queryset = FormulaireSante.objects.filter(patient_id=user_id)  # This line is added for patient role
    else:
        queryset = []

    dataFormulaireSante = [model_to_dict(obj) for obj in queryset]
    for data in dataFormulaireSante:
        patient_id = data['patient']
        patient_user = Utilisateurs.objects.get(id=patient_id)
        data['patient'] = patient_user.username

    context = {
        "form": form,
        "dataFormulaireSante": dataFormulaireSante,
        "champsFormulaireSante": champsFormulaireSante,
        "user_role": user_role,  # Pass the user_role to the template
    }
    return render(request, "historique.html", context)

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
    user_role = request.session.get('role', '')  # Get the role from the session
    user_id = request.user.id  # Get the current user's ID
    
    # If the user is a medecin, filter the medecins queryset to include only the current user
    if user_role == "medecin":
        medecins = Utilisateurs.objects.filter(id=user_id, role="medecin")
    else:
        medecins = Utilisateurs.objects.filter(role="medecin")

    patients = Utilisateurs.objects.filter(role="patient")
    medecin_patient_associations = MedecinPatient.objects.select_related('medecin').prefetch_related('patient')

    if request.method == "POST":
        # Check if the request is for admin validation
        if 'validate_association' in request.POST:
            association_id = request.POST.get('validate_association')
            if user_role in ['admin', 'superadmin']:
                association = get_object_or_404(MedecinPatient, id=association_id)
                association.is_admin_validation = True
                association.save()
            else:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        
        else:  # The request is for creating/updating an association
            medecin_id = request.POST.get("medecin")
            patient_ids = request.POST.getlist("patients")
            
            # Get the selected medic, ensuring the medic is the current user if they are a medecin
            if user_role == "medecin" and str(user_id) != medecin_id:
                # Handle error: medecin can only modify their own associations
                # Redirect to an error page or show an error message
                return redirect("associationMedecinPatient")

            medic = Utilisateurs.objects.get(id=medecin_id)
            
            # Get or create the association instance
            medecin_patient, created = MedecinPatient.objects.get_or_create(medecin=medic)
            
            # If new patients are added, reset the admin validation flag
            if not created:
                existing_patient_ids = set(medecin_patient.patient.values_list('id', flat=True))
                new_patient_ids = set(map(int, patient_ids))
                if not new_patient_ids.issubset(existing_patient_ids):
                    medecin_patient.is_admin_validation = False
                    medecin_patient.save()

            # Associate the selected patients with the medic
            for patient_id in patient_ids:
                patient = Utilisateurs.objects.get(id=patient_id)
                medecin_patient.patient.add(patient)
            
        # Redirect after POST
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
    # Fetch the periodicite for the logged-in patient from the MedecinPatientAssociation
    try:
        association = MedecinPatientAssociation.objects.get(patient_id=request.user.id)
        periodicite_value = association.periodicite
    except MedecinPatientAssociation.DoesNotExist:
        periodicite_value = None  # Default value if the association does not exist

    if request.method == 'GET':
        # Check if it's too early to submit the form
        try:
            last_formulaire = FormulaireSante.objects.filter(patient_id=request.user.id).latest('date_remplissage')
            last_date_remplissage = last_formulaire.date_remplissage
        except FormulaireSante.DoesNotExist:
            last_date_remplissage = None

        next_due_date = (last_date_remplissage + datetime.timedelta(days=periodicite_value)) if last_date_remplissage and periodicite_value is not None else datetime.date.today()

        if datetime.date.today() < next_due_date:
            return render(request, 'too_early.html', {'next_due_date': next_due_date.strftime("%Y-%m-%d")})

        form = FormulaireSanteForm()
        return render(request, 'form_sante.html', {'form': form})
    
    elif request.method == 'POST':
        # Connection à la table de jointure pour periodicité du patient_id
        # Fetch the periodicite for the logged-in patient from the MedecinPatientAssociation
        try:
            association = MedecinPatientAssociation.objects.get(patient_id=request.user.id)
            periodicite_value = association.periodicite
        except MedecinPatientAssociation.DoesNotExist:
            # Handle the case where the association does not exist
            periodicite_value = None  # Or set a default value as appropriate
        
        print(periodicite_value)  # For debugging, should show the periodicite or None 
         # Fetch the last date_remplissage for the patient
        try:
            last_formulaire = FormulaireSante.objects.filter(patient_id=request.user.id).latest('date_remplissage')
            last_date_remplissage = last_formulaire.date_remplissage
        except FormulaireSante.DoesNotExist:
            last_date_remplissage = None

        # Determine the next due date
        if periodicite_value is not None and last_date_remplissage:
            next_due_date = last_date_remplissage + datetime.timedelta(days=periodicite_value)
        else:
            next_due_date = datetime.date.today() + datetime.timedelta(days=30)  # default value

        # Determine is_late and is_early
        today = datetime.date.today()
        is_late = today > next_due_date
        is_early = today < next_due_date
        
        # Calculate the next due date based on current submission
        new_next_due_date = datetime.date.today() + datetime.timedelta(days=periodicite_value if periodicite_value is not None else 30)
        
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
            'periodicite_jours': periodicite_value if periodicite_value is not None else 30,  # Use the retrieved value or a default
            'is_late': is_late,  # Assuming this is a mandatory field with a default value
            'is_early': is_early,  # Assuming this is a mandatory field with a default value
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

        return render(request, 'form_send.html', {'next_due_date': new_next_due_date.strftime("%Y-%m-%d")})

    else:
        form = FormulaireSanteForm()

    return render(request, 'form_sante.html', {'form': form})

########## Crud formulaire santé par le medecin admin etc ############################

@login_required
def crud_form_sante(request):
    role = "superuser" if request.user.is_superuser else request.user.role
    user = request.user
    patients = Utilisateurs.objects.filter(role='patient') if role in ['admin', 'superadmin'] else Utilisateurs.objects.filter(medecinpatientassociation__medecin__medecin=user)

    selected_patient = request.GET.get('patient')
    selected_date_str = request.GET.get('date')
    dates = []

    if selected_patient:
        dates = FormulaireSante.objects.filter(patient_id=selected_patient).values_list('date_remplissage', flat=True).distinct()

    formulaire_sante = None
    if selected_patient and selected_date_str:
        try:
            formatted_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            formulaire_sante = get_object_or_404(FormulaireSante, patient_id=selected_patient, date_remplissage=formatted_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

    if request.method == 'POST':
        action = request.POST.get('action', 'update')  # Default to 'update' if action is not specified

        if action == 'delete':
            if formulaire_sante:
                formulaire_sante.delete()
                messages.success(request, "Record deleted successfully.")
                return redirect('update_success')  # Replace with your desired redirect URL
            else:
                messages.error(request, "No record to delete.")

        elif action == 'update':
            form = FormulaireSanteEditForm(request.POST, instance=formulaire_sante)
            if form.is_valid():
                form.save()
                messages.success(request, "Form updated successfully.")
                return redirect('update_success')
            else:
                messages.error(request, "Form validation error.")
    else:
        form = FormulaireSanteEditForm(instance=formulaire_sante)

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'dates': dates,
        'selected_date': selected_date_str,
        'form': form
    }
    return render(request, 'crud_form_sante.html', context)

# Success landing page
def get_dates_for_patient(request, patient_id):
    dates = FormulaireSante.objects.filter(patient_id=patient_id).values_list('date_remplissage', flat=True).distinct()
    return JsonResponse({'dates': list(dates)})

def update_success(request):
    return render(request, 'update_success.html')