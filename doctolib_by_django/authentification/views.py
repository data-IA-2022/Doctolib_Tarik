from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from authentification.models import Utilisateurs
import random 
import string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

User = get_user_model()

def connexion(request):
    message = ""
    # A t'on reçu des datas d'un formulaire ? Si oui la condition est True
    if request.method == "POST": 
        username = request.POST["username"]
        motDePasse = request.POST["motDePasse"]
        verification = authenticate(username = username,
                                    password = motDePasse)
        if verification != None:
            login(request, verification)
            request.session['username'] = request.user.username
            request.session['role'] = "superuser" if request.user.is_superuser else request.user.role
            print(request.session['username'])
            print(request.session['role'])
            return redirect("accueil")
        else:
            messages.error(request, 'username ou/et mot de passe incorrect')
    
    return render(request,
                      "connexion.html", {"message" : message})

def deconnexion(request):
    logout(request)
    request.session.pop('username', None)
    request.session.pop('role', None)
    return redirect("connexion")

def activate_account(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                # Handle form submission to update username and password
                new_username = request.POST.get('new_username')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                # Check if passwords match
                if new_password == confirm_password:
                    user.username = new_username
                    user.set_password(new_password)
                    user.save()

                    # Log in the user
                    login(request, user)

                    messages.success(request, 'Your account has been successfully updated and activated.')
                    return redirect('connexion')
                else:
                    # Passwords do not match; display an error message
                    messages.error(request, 'Passwords do not match. Please try again.')

            # Generate a random password for the initial activation page
            ideeMDP = "".join([random.choice(string.printable) for _ in range(12)]).replace(" ", "")

            # Render the activation page with a form to update username and password
            return render(request, 'activation.html', {'user': user, 'ideeMDP': ideeMDP})
        else:
            return render(request, 'activation_error.html')  # Handle invalid token
    except User.DoesNotExist:
        return render(request, 'activation_error.html')  # Handle invalid user
