from django import forms
from .models import Utilisateurs

class AccountGenerationForm(forms.Form):
    num_accounts = forms.IntegerField(label='Number of Accounts', min_value=1)
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=[
            ('admin', 'Admin'),
            ('medecin', 'Medecin'),
            ('patient', 'Patient'),
        ],
        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    
class EmailAssociationForm(forms.Form):
    usernames = forms.ModelMultipleChoiceField(
        queryset=Utilisateurs.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        required=True,
    )
    email = forms.EmailField(label='Email', required=True)