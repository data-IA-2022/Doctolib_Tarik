"""
URL configuration for doctolib_by_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views

from application.views import accueil, comptes, menu, historique, edaia, associationAdminsComptes, associationMedecinPatient, formulaire_sante_gen, crud_form_sante
from authentification.views import connexion, deconnexion, activate_account


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil', accueil, name="accueil"),
    path("", connexion, name="connexion"),
    path("comptes", comptes, name="comptes"),
    path('activate_account', activate_account, name='activate_account'),
    path("edaia", edaia, name="edaia"),
    path("historique", historique, name="historique"),
    path("form_sante", formulaire_sante_gen, name="form_sante"),
    path("associationAdminsComptes", associationAdminsComptes, name="associationAdminsComptes"),
    path("associationMedecinPatient", associationMedecinPatient, name="associationMedecinPatient"),
    path('menu', menu, name='menu'),
    path("deconnexion", deconnexion, name="deconnexion"),
    path("crud_form_sante", crud_form_sante, name="crud_form_sante"),
    path('get-dates-for-patient/<int:patient_id>', views.get_dates_for_patient, name='get-dates-for-patient'),
    path('update-success/', views.update_success, name='update_success'),
]
