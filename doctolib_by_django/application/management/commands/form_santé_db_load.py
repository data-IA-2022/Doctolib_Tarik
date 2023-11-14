from faker import Faker
import random
from datetime import timedelta
import os
from django.conf import settings
from django.core.management.base import BaseCommand


# Replace 'your_app' with the name of your Django app
from application.models import FormulaireSante

class Command(BaseCommand):
    help = 'Generate FormSante data and insert it into the database'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Define the range of patient IDs
        min_patient_id = 8
        max_patient_id = 23
        
        # Create a dictionary to keep track of the last form date for each patient
        last_form_dates = {}

        # Number of records you want to generate
        num_records = 1000  # Change this to the desired number of records

        # Define the periodicity for each patient
        periodicity = {
            8: 30,
            9: 15,
            10: 20,
            11: 7,
            12: 14,
            13: 20,
            14: 30,
            15: 15,
            16: 30,
            17: 15,
            18: 20,
            19: 7,
            20: 14,
            21: 20,
            22: 30,
            23: 15,
        }
        
        # Initialize dictionaries to keep track of patient data
        patient_data = {}
        patient_weights = {}
        patient_waists = {}  # Rename to patient_waists for clarity
        patient_genders = {}  # Add a dictionary for patient genders
        
        for _ in range(num_records):
            
            # Generate a random patient_id (assuming you have a range of patient IDs)
            patient_id = random.randint(min_patient_id, max_patient_id)
            
            if patient_id not in patient_genders:
                patient_genders[patient_id] = fake.random_element(elements=('M', 'F'))
            genre = patient_genders[patient_id]

            last_date = last_form_dates.get(patient_id, None)

            # Get the next form date for this patient
            if last_date is None:
                date_remplissage = fake.date_between(start_date="-365d", end_date="today")
            else:
                # Calculate the next form date based on patient's periodicity
                date_remplissage = last_date + timedelta(days=periodicity.get(patient_id, 30))

            # Update the last form date for this patient
            last_form_dates[patient_id] = date_remplissage
            
            
            # Based on value set in periodicity for periodicite_jours
            periodicite_jours = periodicity.get(patient_id, 30)

            # Boolean for is_late
            is_late = fake.boolean(chance_of_getting_true=30)

            imc_category = fake.random_element(elements=('healthy', 'overweight', 'obesity1', 'obesity2'))
            if patient_id not in patient_weights:
                if imc_category == 'healthy':
                    poids = round(random.uniform(50, 80) if genre == 'M' else random.uniform(45, 70), 1)
                    tour_de_taille_cm = random.randint(70, 90) if genre == 'M' else random.randint(60, 80)
                elif imc_category == 'overweight':
                    poids = round(random.uniform(80, 100) if genre == 'M' else random.uniform(70, 90), 1)
                    tour_de_taille_cm = random.randint(90, 100) if genre == 'M' else random.randint(80, 90)
                elif imc_category == 'obesity1':
                    poids = round(random.uniform(100, 120) if genre == 'M' else random.uniform(90, 110), 1)
                    tour_de_taille_cm = random.randint(100, 110) if genre == 'M' else random.randint(90, 105)
                elif imc_category == 'obesity2':
                    poids = round(random.uniform(120, 150) if genre == 'M' else random.uniform(110, 140), 1)
                    tour_de_taille_cm = random.randint(110, 125) if genre == 'M' else random.randint(105, 115)
            else:
                # Modifiez légèrement le poids et la taille de tour de taille à partir des valeurs précédentes
                poids = patient_weights[patient_id] + round(random.uniform(-1, 1), 1)
                tour_de_taille_cm = patient_waists[patient_id] + random.randint(-1, 1)

            # Random integer for frequence_cardiaque_min
            frequence_cardiaque_min = random.randint(60, 100)

            # Random integer for tension_arterielle_systolique_matin and tension_arterielle_systolique_soir
            tension_arterielle_systolique_matin = random.randint(100, 140)
            tension_arterielle_systolique_soir = random.randint(100, 140)

            # Random integer for tension_arterielle_diastolique_matin and tension_arterielle_diastolique_soir
            tension_arterielle_diastolique_matin = random.randint(60, 90)
            tension_arterielle_diastolique_soir = random.randint(60, 90)

            # Boolean for symptomes_cardiovasculaires
            symptomes_cardiovasculaires = fake.boolean(chance_of_getting_true=20)

            # Random integer for nb_medicaments_jour
            nb_medicaments_jour = random.randint(0, 5)

            # Boolean for oublie_medicament_matin and oublie_medicament_soir
            oublie_medicament_matin = fake.boolean(chance_of_getting_true=10)
            oublie_medicament_soir = fake.boolean(chance_of_getting_true=10)

            # Boolean for effets_secondaires
            effets_secondaires = fake.boolean(chance_of_getting_true=10)

            # Boolean for symptomes_particuliers
            symptomes_particuliers = fake.boolean(chance_of_getting_true=10)

            # Boolean for consommation_alcool
            consommation_alcool = fake.boolean(chance_of_getting_true=20)

            # Boolean for grignotage_sucre and grignotage_sale
            grignotage_sucre = fake.boolean(chance_of_getting_true=20)
            grignotage_sale = fake.boolean(chance_of_getting_true=20)

            # Random integer for nb_repas_jour
            nb_repas_jour = random.randint(1, 4)

            # Random float for quantite_eau_litres and quantite_alcool_litres
            quantite_eau_litres = round(random.uniform(1, 3), 2)
            quantite_alcool_litres = round(random.uniform(0, 2), 2)

            # Boolean for activite_physique
            activite_physique = fake.boolean(chance_of_getting_true=70)
            
            # List of physical activity options
            physical_activities = ["marche à pied", "vélo", "nage", "football", "pétanque"]
            if not activite_physique:
                nature_activite_physique = None
                duree_activite_physique_min = None
            else:
                # Randomly select a physical activity from the list
                nature_activite_physique = fake.random_element(physical_activities)
                # Random integer for duree_activite_physique_min
                duree_activite_physique_min = random.randint(15, 120)            

            patient_weights[patient_id] = poids
            patient_waists[patient_id] = tour_de_taille_cm
            
            # Boolean for dyspnee
            dyspnee = fake.boolean(chance_of_getting_true=10)

            # Boolean for oedeme
            oedeme = fake.boolean(chance_of_getting_true=10)

            # Boolean for pre_episode_ir
            pre_episode_ir = fake.boolean(chance_of_getting_true=10)

            # Boolean for fievre
            fievre = fake.boolean(chance_of_getting_true=10)

            # Boolean for palpitation
            palpitation = fake.boolean(chance_of_getting_true=10)

            # Boolean for douleur_thoracique
            douleur_thoracique = fake.boolean(chance_of_getting_true=10)

            # Boolean for malaise
            malaise = fake.boolean(chance_of_getting_true=10)
            
            if not palpitation:
                heure_debut_palpitations = None
                duree_total_palpitations_min = None
            else:
                # Random time for heure_debut_palpitations
                heure_debut_palpitations = fake.time()
                duree_total_palpitations_min = random.randint(1, 60)
                
            if not douleur_thoracique:
                heure_debut_douleurs_thoraciques = None
                duree_total_douleurs_thoraciques_min = None
            else:
                # Random time for heure_debut_douleurs_thoraciques
                heure_debut_douleurs_thoraciques = fake.time()
                duree_total_douleurs_thoraciques_min = random.randint(1, 60)
                
            if not malaise:
                heure_debut_malaises = None
                duree_total_malaises_min = None
            else:
                # Random time for heure_debut_malaises
                heure_debut_malaises = fake.time()
                duree_total_malaises_min = random.randint(1, 60)
            

            # Random float for natremie_mmol_per_l, potassium_mmol_per_l, creatinine_umol_per_l, clairance_creatinine_ml_per_min,
            # nt_probnp_ng_per_l, fer_serique_mg_per_l, hemoglobine_g_per_100_ml, vitesse_sedimentation_mm,
            # proteine_c_reactive_mg_per_l, troponine_ug_per_l, vitamine_d_ng_per_ml, and acide_urique_mg_per_l
            natremie_mmol_per_l = round(random.uniform(135, 145), 1)
            potassium_mmol_per_l = round(random.uniform(3.5, 5.5), 1)
            creatinine_umol_per_l = round(random.uniform(50, 120), 1)
            clairance_creatinine_ml_per_min = round(random.uniform(60, 120), 2)
            nt_probnp_ng_per_l = round(random.uniform(50, 300), 1)
            fer_serique_mg_per_l = round(random.uniform(12, 18), 1)
            hemoglobine_g_per_100_ml = round(random.uniform(12, 18), 1)
            vitesse_sedimentation_mm = random.randint(1, 10)
            proteine_c_reactive_mg_per_l = round(random.uniform(0.1, 10), 1)
            troponine_ug_per_l = round(random.uniform(0, 1), 2)
            vitamine_d_ng_per_ml = round(random.uniform(10, 60), 1)
            acide_urique_mg_per_l = round(random.uniform(2, 7), 2)

            # Random float for inr
            inr = round(random.uniform(0.8, 4), 2)

            
            # Create a new FormulaireSante instance and save it to the database
            form_sante = FormulaireSante(
                date_remplissage=date_remplissage,
                periodicite_jours=periodicite_jours,
                is_late=is_late,
                poids=poids,
                tour_de_taille_cm=tour_de_taille_cm,
                frequence_cardiaque_min=frequence_cardiaque_min,
                tension_arterielle_systolique_matin=tension_arterielle_systolique_matin,
                tension_arterielle_systolique_soir=tension_arterielle_systolique_soir,
                tension_arterielle_diastolique_matin=tension_arterielle_diastolique_matin,
                tension_arterielle_diastolique_soir=tension_arterielle_diastolique_soir,
                symptomes_cardiovasculaires=symptomes_cardiovasculaires,
                nb_medicaments_jour=nb_medicaments_jour,
                oublie_medicament_matin=oublie_medicament_matin,
                oublie_medicament_soir=oublie_medicament_soir,
                effets_secondaires=effets_secondaires,
                symptomes_particuliers=symptomes_particuliers,
                consommation_alcool=consommation_alcool,
                grignotage_sucre=grignotage_sucre,
                grignotage_sale=grignotage_sale,
                nb_repas_jour=nb_repas_jour,
                quantite_eau_litres=quantite_eau_litres,
                quantite_alcool_litres=quantite_alcool_litres,
                activite_physique=activite_physique,
                nature_activite_physique=nature_activite_physique,
                duree_activite_physique_min=duree_activite_physique_min,
                dyspnee=dyspnee,
                oedeme=oedeme,
                pre_episode_ir=pre_episode_ir,
                fievre=fievre,
                palpitation=palpitation,
                douleur_thoracique=douleur_thoracique,
                malaise=malaise,
                heure_debut_palpitations=heure_debut_palpitations,
                duree_total_palpitations_min=duree_total_palpitations_min,
                heure_debut_douleurs_thoraciques=heure_debut_douleurs_thoraciques,
                duree_total_douleurs_thoraciques_min=duree_total_douleurs_thoraciques_min,
                heure_debut_malaises=heure_debut_malaises,
                duree_total_malaises_min=duree_total_malaises_min,
                natremie_mmol_per_l=natremie_mmol_per_l,
                potassium_mmol_per_l=potassium_mmol_per_l,
                creatinine_umol_per_l=creatinine_umol_per_l,
                clairance_creatinine_ml_per_min=clairance_creatinine_ml_per_min,
                nt_probnp_ng_per_l=nt_probnp_ng_per_l,
                fer_serique_mg_per_l=fer_serique_mg_per_l,
                hemoglobine_g_per_100_ml=hemoglobine_g_per_100_ml,
                vitesse_sedimentation_mm=vitesse_sedimentation_mm,
                proteine_c_reactive_mg_per_l=proteine_c_reactive_mg_per_l,
                troponine_ug_per_l=troponine_ug_per_l,
                vitamine_d_ng_per_ml=vitamine_d_ng_per_ml,
                acide_urique_mg_per_l=acide_urique_mg_per_l,
                inr=inr,
                patient_id=patient_id
            )
            
            form_sante.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created {num_records} FormSante records.'))