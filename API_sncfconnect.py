import requests
import pandas as pd
from datetime import datetime, timedelta
import csv

token_auth = "4c39b866-def2-4257-aa35-7816948e07e6"


def convertir_en_temps(chaine):
    ''' on convertit en date la chaine de caractères de l API'''
    return datetime.strptime(chaine.replace('T', ''), '%Y%m%d%H%M%S')


def convertir_en_chaine(dt):
    ''' on convertit en chaîne de caractères un datetime'''
    return datetime.strftime(dt, '%Y%m%dT%H%M%S')


def trouver_code_gare(nom_gare):
    with open("SNCF_gares.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[2] == nom_gare:
                return row[1]
    return "Gare non trouvée"


def trouver_nom_gare(code_gare):
    with open("SNCF_gares.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] == code_gare:
                return row[2]
    return "Gare non trouvée"


now = datetime.now()
# dt = now + timedelta(14)  # dans deux semaines
date_depart = convertir_en_chaine(now)
gare_depart = 'stop_area:SNCF:87686006'
gare_arrivee = 'stop_area:SNCF:87722025'

paris_lyon = requests.get(
    ('https://api.sncf.com/v1/coverage/sncf/journeys?'
     'from={}&to={}&datetime={}').format(gare_depart, gare_arrivee, date_depart),
    auth=(token_auth, '')).json()

# Fetch les durée des arrêts
# session = paris_lyon['journeys'][0]['sections'][1]
# rows = []
# if "stop_date_times" in session:
#     for i in session['stop_date_times']:
#         rows.append(dict(name=i['stop_point']['name'],
#                          depart=convertir_en_temps(i['departure_date_time']),
#                          arrivee=convertir_en_temps(i['arrival_date_time'])))
# print(pd.DataFrame(rows))


# 10 prochains trains a partir de Paris gare de Lyon
departs_paris = requests.get(
    ('https://api.sncf.com/v1/coverage/sncf/stop_areas/'
     'stop_area:SNCF:87686006/departures'), auth=(token_auth, '')).json()

for depart in departs_paris['departures']:
    print("Direction : ", depart['display_informations']['direction'])
    print("Heure de départ : ", convertir_en_temps(depart['stop_date_time']['departure_date_time']))
    print("Heure d'arrivée : ", convertir_en_temps(depart['stop_date_time']['arrival_date_time']))
