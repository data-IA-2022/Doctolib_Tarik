from django import forms

class AccountGenerationForm(forms.Form):
    num_accounts = forms.IntegerField(label='Number of Accounts', min_value=1)
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=[
            ('admin', 'Admin'),
            ('medecin', 'Medecin'),
            ('patient', 'Patient'),
        ]
    )