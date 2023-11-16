import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import FormulaireSante
from .views import historique, formulaire_sante_gen
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

@pytest.mark.django_db
def test_historique_view(client):
    # Create a test user
    user = get_user_model().objects.create_user(
        username='M1001',
        password='M1001MDP',
    )

    # Log in the test user
    client.login(username='M1001', password='M1001MDP')

    # Access the historique view
    response = client.get(reverse('historique'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_formulaire_sante_gen_view(client):
    # Create a test user
    user = get_user_model().objects.create_user(
        username='testuser',
        password='testpassword',
    )

    # Log in the test user
    client.login(username='testuser', password='testpassword')

    # Access the formulaire_sante_gen view
    response = client.get(reverse('formulaire_sante_gen'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_submit_formulaire_sante(client):
    # Create a test user
    user = get_user_model().objects.create_user(
        username='A1001',
        password='A1001MDP',
    )

    # Log in the test user
    client.login(username='A1001', password='A1001MDP')

    # Create a test FormulaireSante instance
    form_data = {
        # Provide form field values here
    }

    response = client.post(reverse('formulaire_sante_gen'), data=form_data)

    # Check if the form submission was successful (you may need to customize this assertion)
    assert response.status_code == 200

    # Check if a FormulaireSante object was created
    assert FormulaireSante.objects.filter(patient=user).exists()