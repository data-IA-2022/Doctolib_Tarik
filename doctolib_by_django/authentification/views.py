from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
from authentification.models import Utilisateurs
import random 
import string

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
            return redirect("accueil")
        else:
            messages.error(request, 'username ou/et mot de passe incorrect')
    
    return render(request,
                      "connexion.html", {"message" : message})

def deconnexion(request):
    logout(request)
    return redirect("connexion")


def inscription(request):
    ideeMDP = "".join([random.choice(string.printable) for _ in range(12)]).replace(" ", "")
    if request.method == "POST": 
        email = request.POST["email"]
        username = request.POST["username"]
        motDePasse = request.POST["motDePasse"]
        nouveauCompte = Utilisateurs.objects.create_user(email = email, username = username,
                                    password = motDePasse)
        
        messages.success(request, 'Votre compte à été créé avec succès')
        return redirect("connexion")
    
    return render(request,
                      "inscription.html", {"ideeMDP" : ideeMDP.replace(" ", "")})
