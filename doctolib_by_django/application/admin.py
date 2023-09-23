from django.contrib import admin

from .models import AdminCompte, MedecinPatient, FormulaireSante, FormulaireEvalStress
from authentification.models import Utilisateurs

# User Admin
# @admin.register(Utilisateurs)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email','is_superuser', 'role','date_joined',)
    
admin.site.register(Utilisateurs, UtilisateurAdmin)

# Register the MedecinPatient model
class MedecinPatientAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'display_patients')

    def display_patients(self, obj):
        # Return a comma-separated list of patient usernames
        return ', '.join(patient.username for patient in obj.patient.all())

    display_patients.short_description = 'Patients'  # Sets the column header

admin.site.register(MedecinPatient, MedecinPatientAdmin)

# Register the AdminMédecin model
class AdminCompteAdmin(admin.ModelAdmin):
    list_display = ('admin', 'display_users')

    def display_users(self, obj):
        # Assuming you want to display a comma-separated list of user names
        return ", ".join([user.username for user in obj.users.all()])
    display_users.short_description = 'Users'  # Customize the column header

admin.site.register(AdminCompte, AdminCompteAdmin)

# Register the FormulaireSante model
class FormulaireSanteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date_remplissage', 'periodicite_jours')

admin.site.register(FormulaireSante, FormulaireSanteAdmin)

# Register the FormulaireEvalStress model
class FormulaireEvalStressAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date_remplissage', 'periodicite_jours')

admin.site.register(FormulaireEvalStress, FormulaireEvalStressAdmin)
