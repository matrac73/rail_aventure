import requests
import pandas as pd
from datetime import datetime, timedelta
import csv
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_SNCF = os.getenv("API_KEY_SNCF")


def convertir_en_temps(chaine):
    ''' on convertit en date la chaine de caractères de l API'''
    return datetime.strptime(chaine.replace('T', ''), '%Y%m%d%H%M%S')


def convertir_en_chaine(dt):
    ''' on convertit en chaîne de caractères un datetime'''
    return datetime.strftime(dt, '%Y%m%dT%H%M%S')


def convertir_en_code_gare(nom_gare):
    with open("SNCF_gares.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[2] == nom_gare:
                return row[1]
    return "Gare non trouvée"


def convertir_en_nom_gare(code_gare):
    with open("SNCF_gares.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] == code_gare:
                return row[2]
    return "Gare non trouvée"


def détails_trajet(gare_depart, gare_arrivee, date_depart):
    code_gare_depart = convertir_en_code_gare(gare_depart)
    code_gare_arrivee = convertir_en_code_gare(gare_arrivee)
    trajet = requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/journeys?from={}&to={}&datetime={}')
        .format(code_gare_depart, code_gare_arrivee, date_depart),
        auth=(API_KEY_SNCF, '')).json()

    session = trajet['journeys'][0]['sections'][1]
    rows = []
    if "stop_date_times" in session:
        for i in session['stop_date_times']:
            rows.append(dict(name=i['stop_point']['name'],
                             depart=convertir_en_temps(i['departure_date_time']),
                             arrivee=convertir_en_temps(i['arrival_date_time'])))
    return pd.DataFrame(rows)


def prochains_departs(gare, date):
    """Affiche les 10 prochains départs d'une gare a une date donnée"""
    departs = requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/stop_areas/'+convertir_en_code_gare(gare)+'/departures?from_datetime='+convertir_en_chaine(date)),
        auth=(API_KEY_SNCF, '')).json()

    informations_depart = []

    for depart in departs['departures']:
        info_depart = {
            'direction': depart['display_informations']['direction'],
            'heure_depart': depart['stop_date_time']['departure_date_time'],
            'heure_arrivee': depart['stop_date_time']['arrival_date_time']
        }
        informations_depart.append(info_depart)

    return informations_depart


def destination_tgv(origine, datetime):
    '''10 prochains départs d'une gare donnée '''
    return requests.get('https://api.sncf.com/v1/coverage/sncf/stop_areas/{}/departures?from_datetime={}'
                        .format(origine, datetime), auth=(API_KEY_SNCF, '')).json()


def trajets_periode(gare_depart, date_X, date_Y):
    '''informations sur des trajets partant d'une gare entre une date X et une date Y'''

    destinations = []
    gare_code = convertir_en_code_gare(gare_depart)
    while convertir_en_temps(date_X) < convertir_en_temps(date_Y):
        resultats = destination_tgv(gare_code, date_X)
        for resultat in resultats['departures']:
            info_depart = {
                'direction': resultat['display_informations']['direction'],
                'heure_depart': resultat['stop_date_time']['departure_date_time'],
                'heure_arrivee': resultat['stop_date_time']['arrival_date_time']
            }
            if convertir_en_temps(info_depart['heure_depart']) < convertir_en_temps(date_Y):
                destinations.append(info_depart)

        nombre_resultats = resultats['pagination']['items_on_page']
        if nombre_resultats <= 0:
            break
        date_X = resultats['departures'][nombre_resultats-1]['stop_date_time']['departure_date_time']
    return destinations


print(trajets_periode('Lyon Part Dieu', convertir_en_chaine(datetime.now()), convertir_en_chaine(datetime.now()+timedelta(1))))
