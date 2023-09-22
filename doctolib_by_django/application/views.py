from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AccountGenerationForm
from django.contrib import messages
from authentification.models import Utilisateurs






# Create your views here.
@login_required
def accueil(request):
    prenom = request.user.username
    role = "superuser" if request.user.is_superuser else request.user.role
    return render(request, "accueil.html", {"prenom": prenom, "role": role})

@login_required
def menu(request):
    username = request.user.username
    role = "superuser" if request.user.is_superuser else request.user.role
    return render(request, "menu.html", {"username": username, "role": role})

@login_required
def comptes(request):
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

            return render(request, 'comptes.html', {'form': form, 'created_accounts': created_accounts})
    else:
        form = AccountGenerationForm()
    
    return render(request, 'comptes.html', {'form': form})
  
