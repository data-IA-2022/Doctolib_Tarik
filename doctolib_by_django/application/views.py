from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def accueil(request):
    prenom = request.user.username
    return render(request, "accueil.html", {"prenom": prenom})
  
