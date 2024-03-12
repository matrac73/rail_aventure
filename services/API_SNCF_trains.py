import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_SNCF = os.getenv("API_KEY_SNCF")


def page_train(numero_page):
    return requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?start_page={}')
        .format(numero_page), auth=(API_KEY_SNCF, ''))


page_initiale = page_train(0)
item_per_page = page_initiale.json()['pagination']['items_per_page']
total_items = page_initiale.json()['pagination']['total_result']
dfs = []

nb_pages = int(total_items/item_per_page)
# limiter le nombre d'inférence pour éviter la limite 13667 > 5000
if nb_pages <= 10:
    nb_inference = nb_pages
else:
    nb_inference = 10

for page in range(1, nb_inference+1):
    trains_page = page_train(page).json()

    if 'vehicle_journeys' not in trains_page:
        # pas de trains => prochaine itération
        continue

    train = {}

    # on ne retient que les informations qui nous intéressent
    for train_raw in trains_page['vehicle_journeys']:

        train['name'] = train_raw['name']
        print(train['name'])

        train['id'] = train_raw['id']
        print(train['id'])

        train['journey_pattern'] = train_raw['journey_pattern']['id']
        print(train['journey_pattern'])

        train['headsign'] = train_raw['headsign']
        print(train['headsign'])

        train['stops'] = {}
        nb_stop = len(train_raw['stop_times'])
        for i in range(nb_stop):
            train['stops']['name'] = train_raw['stop_times'][i]['stop_point']['id']
            train['stops']['arrival_hour'] = train_raw['stop_times'][i]['arrival_time']
            train['stops']['departure_hour'] = train_raw['stop_times'][i]['departure_time']
        print(train['stops'])

    try:
        dp = pd.DataFrame(train)
    except Exception as e:
        raise Exception("Problème de données\n{0}".format(train)) from e

    dfs.append(dp)
    if page % 10 == 0:
        print("je suis à la page", page, "---", dp.shape)

df = pd.concat(dfs)
df.to_csv("./SNCF_trains.csv")
