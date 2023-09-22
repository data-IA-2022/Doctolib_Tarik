from django.contrib import admin

from .models import AdminCompte, MédecinPatient, FormulaireSante, FormulaireEvalStress
from authentification.models import Utilisateurs

# User Admin
# @admin.register(Utilisateurs)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email','is_superuser', 'role','date_joined',)
    
admin.site.register(Utilisateurs, UtilisateurAdmin)

# Register the MédecinPatient model
class MédecinPatientAdmin(admin.ModelAdmin):
    list_display = ('médecin', 'patient')

admin.site.register(MédecinPatient, MédecinPatientAdmin)

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
