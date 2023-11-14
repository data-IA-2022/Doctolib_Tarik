from faker import Faker
import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from application.models import Utilisateurs, FormulaireEvalStress

class Command(BaseCommand):
    help = 'Generate FormulaireEvalStress data and insert it into the database'

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

        for _ in range(num_records):
            # Generate a random patient_id (assuming you have a range of patient IDs)
            patient_id = random.randint(min_patient_id, max_patient_id)

            last_date = last_form_dates.get(patient_id, None)
            end_date = datetime(2023, 11, 10) 
            # Get the next form date for this patient
            if last_date is None:
                date_remplissage = fake.date_between(start_date="-365d", end_date=end_date)
            else:
                # Calculate the next form date based on the patient's periodicity
                date_remplissage = last_date + timedelta(days=periodicity.get(patient_id, 30))

            # Update the last form date for this patient
            last_form_dates[patient_id] = date_remplissage

            # Generate random data for all fields with 0, 1, 5, or 10 values
            data = {
                'date_remplissage': date_remplissage,
                'periodicite_jours': periodicity.get(patient_id, 30),
                'is_late': fake.boolean(chance_of_getting_true=30),
                'is_early': fake.boolean(chance_of_getting_true=30),
                'irritabilite': random.choice([0, 1, 5, 10]),
                'sentiments_depressifs': random.choice([0, 1, 5, 10]),
                'bouche_seche_gorge_seche': random.choice([0, 1, 5, 10]),
                'actions_gestes_impulsifs': random.choice([0, 1, 5, 10]),
                'grincement_dents': random.choice([0, 1, 5, 10]),
                'difficulte_rester_assis': random.choice([0, 1, 5, 10]),
                'cauchemars': random.choice([0, 1, 5, 10]),
                'diarrhee': random.choice([0, 1, 5, 10]),
                'attaques_verbales': random.choice([0, 1, 5, 10]),
                'hauts_bas_emotifs': random.choice([0, 1, 5, 10]),
                'grande_envie_de_pleurer': random.choice([0, 1, 5, 10]),
                'grande_envie_de_fuir': random.choice([0, 1, 5, 10]),
                'grande_envie_de_faire_mal': random.choice([0, 1, 5, 10]),
                'pensees_embrouillees': random.choice([0, 1, 5, 10]),
                'debit_plus_rapide': random.choice([0, 1, 5, 10]),
                'fatigue_lourdeur_generalisees': random.choice([0, 1, 5, 10]),
                'sentiment_surcharge': random.choice([0, 1, 5, 10]),
                'sentiment_emotionnellement_fragile': random.choice([0, 1, 5, 10]),
                'sentiment_tristesse': random.choice([0, 1, 5, 10]),
                'sentiment_anxiete': random.choice([0, 1, 5, 10]),
                'tension_emotionnelle': random.choice([0, 1, 5, 10]),
                'hostilite_vers_autres': random.choice([0, 1, 5, 10]),
                'tremblements_gestes_nerveux': random.choice([0, 1, 5, 10]),
                'begaiements_hesitations_verbales': random.choice([0, 1, 5, 10]),
                'incapacite_difficulte_concentrer': random.choice([0, 1, 5, 10]),
                'difficulte_organiser_pensees': random.choice([0, 1, 5, 10]),
                'difficulte_dormir_nuit_sans_reveiller': random.choice([0, 1, 5, 10]),
                'besoin_frequent_uriner': random.choice([0, 1, 5, 10]),
                'maux_estomac_difficultes_digerer': random.choice([0, 1, 5, 10]),
                'geste_sentiment_impatience': random.choice([0, 1, 5, 10]),
                'maux_tete': random.choice([0, 1, 5, 10]),
                'douleurs_dos_nuque': random.choice([0, 1, 5, 10]),
                'perte_gain_appetit': random.choice([0, 1, 5, 10]),
                'perte_interet_sexe': random.choice([0, 1, 5, 10]),
                'oublis_frequents': random.choice([0, 1, 5, 10]),
                'douleurs_serrements_poitrine': random.choice([0, 1, 5, 10]),
                'conflits_significatifs_avec_autres': random.choice([0, 1, 5, 10]),
                'difficulte_lever_apres_sommeil': random.choice([0, 1, 5, 10]),
                'sentiment_choses_hors_de_controle': random.choice([0, 1, 5, 10]),
                'difficulte_longue_activite_continue': random.choice([0, 1, 5, 10]),
                'mouvements_retrait_isolement': random.choice([0, 1, 5, 10]),
                'difficulte_s_endormir': random.choice([0, 1, 5, 10]),
                'difficulte_se_remettre_evenement_contrariant': random.choice([0, 1, 5, 10]),
                'mains_moites': random.choice([0, 1, 5, 10]),
                'total_impact_stress': random.choice([0, 1, 5, 10])
            }

            # Create a new FormulaireEvalStress instance and save it to the database
            patient = Utilisateurs.objects.get(pk=patient_id)
            form_eval_stress = FormulaireEvalStress(patient=patient, **data)
            form_eval_stress.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_records} FormulaireEvalStress records.'))
