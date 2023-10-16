from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AccountGenerationForm, EmailAssociationForm
from django.contrib import messages
from authentification.models import Utilisateurs
from .models import AdminCompte, MedecinPatient
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string




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



