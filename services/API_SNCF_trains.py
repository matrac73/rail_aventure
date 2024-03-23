import math
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_SNCF = os.getenv("API_KEY_SNCF")


def page_train(numero_page):
    return requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?start_page={}')
        .format(numero_page), auth=(API_KEY_SNCF, ''))


def L2(departure_coord, arrival_coord):
    lat1, lon1 = departure_coord
    lat2, lon2 = arrival_coord
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)


def transform_data(api_data):
    trains_demo = {}

    for i, disruption in enumerate(api_data['disruptions']):
        for stop in disruption['impacted_objects'][0]['impacted_stops']:
            train_key = f'train_{i}'
            if train_key not in trains_demo:
                trains_demo[train_key] = {}

            departure_coord = (float(stop['stop_point']['coord']['lat']), float(stop['stop_point']['coord']['lon']))
            arrival_coord = (float(api_data['disruptions'][i+1]['impacted_objects'][0]['impacted_stops'][0]['stop_point']['coord']['lat']), float(api_data['disruptions'][i+1]['impacted_objects'][0]['impacted_stops'][0]['stop_point']['coord']['lon']))
            distance = L2(departure_coord, arrival_coord)

            trains_demo[train_key]['depart'] = stop['stop_point']['name']
            trains_demo[train_key]['arrivee'] = api_data['disruptions'][i+1]['impacted_objects'][0]['impacted_stops'][0]['stop_point']['name'] if i < len(api_data['disruptions']) - 1 else "Unknown"
            trains_demo[train_key]['prix'] = math.ceil(distance / 10)
            trains_demo[train_key]['co2'] = math.ceil(distance / 100)
            trains_demo[train_key]['depart_heure'] = int(stop['base_departure_time'][:2])
            trains_demo[train_key]['arrivee_heure'] = int(stop['base_arrival_time'][:2])

    return trains_demo


# page_initiale = page_train(0)
# item_per_page = page_initiale.json()['pagination']['items_per_page']
# total_items = page_initiale.json()['pagination']['total_result']
# dfs = []

# nb_pages = int(total_items/item_per_page)
# # limiter le nombre d'inférence pour éviter la limite 13667 > 5000
# if nb_pages <= 10:
#     nb_inference = nb_pages
# else:
#     nb_inference = 10

# for page in range(1, nb_inference+1):
#     trains_page = page_train(page).json()

#     if 'vehicle_journeys' not in trains_page:
#         # pas de trains => prochaine itération
#         continue

#     train = {}

#     # on ne retient que les informations qui nous intéressent
#     for train_raw in trains_page['vehicle_journeys']:

#         train['name'] = train_raw['name']
#         print(train['name'])

#         train['id'] = train_raw['id']
#         print(train['id'])

#         train['journey_pattern'] = train_raw['journey_pattern']['id']
#         print(train['journey_pattern'])

#         train['headsign'] = train_raw['headsign']
#         print(train['headsign'])

#         train['stops'] = {}
#         nb_stop = len(train_raw['stop_times'])
#         for i in range(nb_stop):
#             train['stops']['name'] = train_raw['stop_times'][i]['stop_point']['id']
#             train['stops']['arrival_hour'] = train_raw['stop_times'][i]['arrival_time']
#             train['stops']['departure_hour'] = train_raw['stop_times'][i]['departure_time']
#         print(train['stops'])

#     try:
#         dp = pd.DataFrame(train)
#     except Exception as e:
#         raise Exception("Problème de données\n{0}".format(train)) from e

#     dfs.append(dp)
#     if page % 10 == 0:
#         print("je suis à la page", page, "---", dp.shape)

# df = pd.concat(dfs)
# df.to_csv("./data/SNCF_trains.csv")
