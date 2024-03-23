import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import requests
from dotenv import load_dotenv
import os
import csv

load_dotenv()
API_KEY_SNCF = os.getenv("API_KEY_SNCF")

trains_demo = {
    'train_0': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 50, "co2": 30, "depart_heure": 1, "arrivee_heure": 3},
    'train_1': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 50, "co2": 30, "depart_heure": 4, "arrivee_heure": 6},
    'train_2': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 10, "co2": 20, "depart_heure": 2, "arrivee_heure": 6},
    'train_3': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 10, "co2": 20, "depart_heure": 7, "arrivee_heure": 11},
    'train_4': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 70, "co2": 100, "depart_heure": 1, "arrivee_heure": 6},
    'train_5': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 50, "co2": 30, "depart_heure": 7, "arrivee_heure": 10},
    'train_6': {"depart": "Bordeaux Saint-Jean", "arrivee": "Marseille Saint-Charles", "prix": 10, "co2": 20, "depart_heure": 7, "arrivee_heure": 14},
    'train_7': {"depart": "Bordeaux Saint-Jean", "arrivee": "Marseille Saint-Charles", "prix": 50, "co2": 30, "depart_heure": 10, "arrivee_heure": 12},
    'train_8': {"depart": "Marseille Saint-Charles", "arrivee": "Nice", "prix": 10, "co2": 10, "depart_heure": 15, "arrivee_heure": 17},
    'train_9': {"depart": "Marseille Saint-Charles", "arrivee": "Nice", "prix": 30, "co2": 15, "depart_heure": 13, "arrivee_heure": 15},
}

trains = {
    'train_0': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 50, "co2": 30, "depart_heure": 1, "arrivee_heure": 3},
    'train_1': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 50, "co2": 30, "depart_heure": 4, "arrivee_heure": 6},
    'train_2': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 10, "co2": 20, "depart_heure": 2, "arrivee_heure": 6},
    'train_3': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 10, "co2": 20, "depart_heure": 7, "arrivee_heure": 11},
    'train_4': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 70, "co2": 100, "depart_heure": 1, "arrivee_heure": 6},
    'train_5': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 50, "co2": 30, "depart_heure": 7, "arrivee_heure": 10},
    'train_6': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 50, "co2": 30, "depart_heure": 7, "arrivee_heure": 10},
    'train_7': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 50, "co2": 15, "depart_heure": 8, "arrivee_heure": 16},
    'train_8': {"depart": "Marseille Saint-Charles", "arrivee": "Nice", "prix": 30, "co2": 20, "depart_heure": 9, "arrivee_heure": 11},
    'train_9': {"depart": "Bordeaux Saint-Jean", "arrivee": "Paris - Gare de Lyon - Hall 1 & 2", "prix": 50, "co2": 15, "depart_heure": 10, "arrivee_heure": 18},
    'train_10': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 50, "co2": 20, "depart_heure": 7, "arrivee_heure": 9},
    'train_11': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 60, "co2": 35, "depart_heure": 2, "arrivee_heure": 5},
    'train_12': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 55, "co2": 35, "depart_heure": 5, "arrivee_heure": 7},
    'train_13': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 40, "co2": 25, "depart_heure": 3, "arrivee_heure": 7},
    'train_14': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 40, "co2": 25, "depart_heure": 8, "arrivee_heure": 12},
    'train_15': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 75, "co2": 110, "depart_heure": 2, "arrivee_heure": 7},
    'train_16': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 55, "co2": 35, "depart_heure": 8, "arrivee_heure": 11},
    'train_17': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 80, "co2": 30, "depart_heure": 8, "arrivee_heure": 10},
    'train_18': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 55, "co2": 20, "depart_heure": 9, "arrivee_heure": 17},
    'train_19': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 10, "co2": 20, "depart_heure": 10, "arrivee_heure": 14},
    'train_20': {"depart": "Bordeaux Saint-Jean", "arrivee": "Paris - Gare de Lyon - Hall 1 & 2", "prix": 55, "co2": 20, "depart_heure": 11, "arrivee_heure": 19},
    'train_21': {"depart": "Marseille Saint-Charles", "arrivee": "Lyon Part Dieu", "prix": 55, "co2": 25, "depart_heure": 8, "arrivee_heure": 10},
    'train_22': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 65, "co2": 40, "depart_heure": 4, "arrivee_heure": 6},
    'train_23': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 60, "co2": 40, "depart_heure": 6, "arrivee_heure": 8},
    'train_24': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 45, "co2": 30, "depart_heure": 5, "arrivee_heure": 9},
    'train_25': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 45, "co2": 30, "depart_heure": 9, "arrivee_heure": 13},
    'train_26': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 80, "co2": 105, "depart_heure": 3, "arrivee_heure": 8},
    'train_27': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 60, "co2": 35, "depart_heure": 9, "arrivee_heure": 12},
    'train_28': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 70, "co2": 30, "depart_heure": 15, "arrivee_heure": 18},
    'train_29': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 60, "co2": 25, "depart_heure": 10, "arrivee_heure": 18},
    'train_30': {"depart": "Nice", "arrivee": "Marseille Saint-Charles", "prix": 20, "co2": 25, "depart_heure": 11, "arrivee_heure": 13},
    'train_31': {"depart": "Bordeaux Saint-Jean", "arrivee": "Paris - Gare de Lyon - Hall 1 & 2", "prix": 10, "co2": 25, "depart_heure": 12, "arrivee_heure": 20},
    'train_32': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 60, "co2": 30, "depart_heure": 9, "arrivee_heure": 11},
    'train_33': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 70, "co2": 45, "depart_heure": 6, "arrivee_heure": 8},
    'train_34': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 65, "co2": 45, "depart_heure": 7, "arrivee_heure": 9},
    'train_35': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 50, "co2": 35, "depart_heure": 7, "arrivee_heure": 11},
    'train_36': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 50, "co2": 35, "depart_heure": 10, "arrivee_heure": 14},
    'train_37': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 10, "co2": 20, "depart_heure": 4, "arrivee_heure": 9},
    'train_38': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 65, "co2": 40, "depart_heure": 10, "arrivee_heure": 13},
    'train_39': {"depart": "Marseille Saint-Charles", "arrivee": "Nice", "prix": 30, "co2": 20, "depart_heure": 20, "arrivee_heure": 22},
    'train_40': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 65, "co2": 30, "depart_heure": 11, "arrivee_heure": 19},
    'train_41': {"depart": "Marseille Saint-Charles", "arrivee": "Lyon Part Dieu", "prix": 40, "co2": 30, "depart_heure": 12, "arrivee_heure": 14},
    'train_42': {"depart": "Bordeaux Saint-Jean", "arrivee": "Paris - Gare de Lyon - Hall 1 & 2", "prix": 10, "co2": 30, "depart_heure": 13, "arrivee_heure": 21},
    'train_43': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 65, "co2": 35, "depart_heure": 10, "arrivee_heure": 12},
    'train_44': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 75, "co2": 50, "depart_heure": 7, "arrivee_heure": 9},
    'train_45': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 70, "co2": 50, "depart_heure": 8, "arrivee_heure": 10},
    'train_46': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Lyon Part Dieu", "prix": 55, "co2": 40, "depart_heure": 8, "arrivee_heure": 12},
    'train_47': {"depart": "Lyon Part Dieu", "arrivee": "Marseille Saint-Charles", "prix": 55, "co2": 40, "depart_heure": 11, "arrivee_heure": 15},
    'train_48': {"depart": "Paris - Gare de Lyon - Hall 1 & 2", "arrivee": "Bordeaux Saint-Jean", "prix": 90, "co2": 120, "depart_heure": 5, "arrivee_heure": 10},
    'train_49': {"depart": "Marseille Saint-Charles", "arrivee": "Bordeaux Saint-Jean", "prix": 70, "co2": 45, "depart_heure": 11, "arrivee_heure": 14},
}


def lister_gares(trains):
    gares = set()
    for _, details in trains.items():
        gares.add(details['depart'])
        gares.add(details['arrivee'])

    return list(gares)


def transform_data_tree(trains, gare, heure, prix, co2):
    arbre = {'gare': gare, 'heure': heure, 'prix': prix, 'co2': co2, 'trains': []}
    for train_id, train_info in trains.items():
        if (gare == "" or train_info['depart'] == gare) and train_info['depart_heure'] > heure:
            prochaine_gare = train_info['arrivee']
            prochaine_heure = train_info['arrivee_heure']
            prochain_prix = prix + train_info['prix']
            prochain_co2 = co2 + train_info['co2']
            prochain_noeud = transform_data_tree(trains, prochaine_gare, prochaine_heure, prochain_prix, prochain_co2)
            arbre['trains'].append({train_id: prochain_noeud})
    return arbre


def transform_tree_graph(arbre, parent=None, graph=None):
    if graph is None:
        graph = nx.DiGraph()
    current_node = arbre['gare'] + '_' + str(arbre['heure']) + 'h_' + str(arbre['prix']) + '€_' + str(arbre['co2']) + 'gCO2'
    if parent:
        parent_node = parent['gare'] + '_' + str(parent['heure']) + 'h_' + str(parent['prix']) + '€_' + str(parent['co2']) + 'gCO2'
        for train in parent['trains']:
            if list(train.values())[0] == arbre:
                train_taken = list(train.keys())[0]
                break
        graph.add_edge(parent_node, current_node, train=train_taken)
    for train in arbre['trains']:
        child = list(train.values())[0]
        transform_tree_graph(child, arbre, graph)
    return graph


def display_graph(trains, gare_depart, heure_depart):
    arbre = transform_data_tree(trains, gare_depart, heure_depart, 0, 0)
    graph = transform_tree_graph(arbre)
    pos = nx.spring_layout(graph, k=0.15, iterations=20)  # default k=0.1 and iterations=50

    # Trouver le nœud initial
    initial_node = None
    for node in graph.nodes():
        if graph.in_degree(node) == 0:
            initial_node = node
            break

    # Définition des options
    node_colors = ['red' if node == initial_node
                   else 'lightblue' for node in graph.nodes()]
    node_size = 300
    edge_color = 'gray'
    width = 2.0
    style = 'solid'
    font_size = 10
    font_color = 'black'
    alpha = 0.8

    # Dessiner le graphique avec les options personnalisées
    nx.draw(graph, pos, with_labels=True, arrows=True,
            node_color=node_colors, node_size=node_size,
            edge_color=edge_color, width=width, style=style,
            font_size=font_size, font_color=font_color,
            alpha=alpha)

    # Ajouter les étiquettes des arêtes
    edge_labels = {(n1, n2): d['train'] for n1, n2, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Afficher le graphique
    temp_file = "/tmp/graph_image.png"  # Utilisez un chemin de fichier approprié
    plt.savefig(temp_file, format="png")

    return temp_file


def heuristique(heure, prix, co2, poids_heure, poids_prix, poids_co2):
    valeur_heuristique = poids_heure * heure + poids_prix * prix + poids_co2 * co2
    return valeur_heuristique


def find_optimal_path_DFS(node, destination, poids_heure, poids_prix, poids_CO2, current_time=0, current_price=0, current_co2=0):
    if node['gare'] == destination:
        return {
            'heure': current_time,
            'prix': current_price,
            'co2': current_co2,
            'path': [destination]
        }

    best_path = None

    for train in node['trains']:
        nom_train = list(train.keys())[0]
        next_node = train[nom_train]
        next_time = train[nom_train]['heure']
        next_price = train[nom_train]['prix']
        next_co2 = train[nom_train]['co2']

        path_result = find_optimal_path_DFS(next_node, destination, poids_heure, poids_prix, poids_CO2, next_time, next_price, next_co2)

        if path_result:
            path_result['path'].insert(0, nom_train)
            path_result['path'].insert(0, node['gare'])
            if not best_path:
                best_path = path_result
            else:
                heuristique_path = heuristique(path_result['heure'], path_result['prix'], path_result['co2'], poids_heure, poids_prix, poids_CO2)
                heuristique_best_path = heuristique(best_path['heure'], best_path['prix'], best_path['co2'], poids_heure, poids_prix, poids_CO2)
                if heuristique_path < heuristique_best_path:
                    best_path = path_result

    return best_path


def find_optimal_path_BFS(start_node, destination, poids_heure, poids_prix, poids_CO2):
    queue = [(start_node, [], 0, 0, 0)]  # (node, path, time, price, co2)

    while queue:
        queue.sort(key=lambda x: heuristique(x[2], x[3], x[4], poids_heure, poids_prix, poids_CO2))
        node, path, current_time, current_price, current_co2 = queue.pop(0)

        if node['gare'] == destination:
            return {
                'heure': current_time,
                'prix': current_price,
                'co2': current_co2,
                'path': path + [destination]
            }

        for train in node['trains']:
            nom_train = list(train.keys())[0]
            next_node = train[nom_train]
            next_time = train[nom_train]['heure']
            next_price = train[nom_train]['prix']
            next_co2 = train[nom_train]['co2']

            new_path = path + [node['gare'], nom_train]

            queue.append((next_node, new_path, next_time, next_price, next_co2))

    return None


def find_optimal_path_A_star(node, destination, poids_heure, poids_prix, poids_CO2, current_time=0, current_price=0, current_co2=0):
    open_set = [(heuristique(node['heure'], node['prix'], node['co2'], poids_heure, poids_prix, poids_CO2),
                 0,
                 node,
                 current_time,
                 current_price,
                 current_co2,
                 [])]
    closed_set = set()

    while open_set:
        open_set = sorted(open_set, key=lambda x: x[0])
        _, g_score, current_node, time, price, co2, path = open_set.pop(0)
        if len(path) > 0:
            path[-2], path[-1] = path[-1], path[-2]

        if current_node['gare'] == destination:
            return {
                'heure': time,
                'prix': price,
                'co2': co2,
                'path': path + [destination]
            }

        closed_set.add(current_node['gare'])

        for train in current_node['trains']:
            nom_train = list(train.keys())[0]
            next_node = train[nom_train]
            next_time = next_node['heure']
            next_price = next_node['prix']
            next_co2 = next_node['co2']

            if next_node['gare'] not in closed_set:
                g_score_next = g_score + 1  # Assuming each step has a cost of 1, can be adjusted based on the problem
                f_score_next = g_score_next + heuristique(next_node['heure'], next_node['prix'], next_node['co2'], poids_heure, poids_prix, poids_CO2)
                new_path = path + [nom_train, current_node['gare']]

                open_set.append((f_score_next, g_score_next, next_node, next_time, next_price, next_co2, new_path))

    return None  # No path found


def find_optimal_journey(gare_départ, gare_arrivée, heure_départ, choix_algorithme, choix_dataset, poids_heure, poids_prix, poids_CO2):
    heure_départ = float(heure_départ)

    if choix_dataset == "10 trains synthéthiques":
        data_trains = trains_demo
    elif choix_dataset == "50 trains synthéthiques":
        data_trains = trains
    elif choix_dataset == "API SNCF 25 trains":
        data_trains = API_call(1)
    elif choix_dataset == "API SNCF 100 trains":
        data_trains = API_call(4)
    elif choix_dataset == "API SNCF 1000 trains":
        data_trains = API_call(40)

    arbre = transform_data_tree(data_trains, gare_départ, heure_départ, 0, 0)

    if choix_algorithme == "Depth First Search":
        resultat_json = find_optimal_path_DFS(arbre, gare_arrivée, poids_heure, poids_prix, poids_CO2)
    elif choix_algorithme == "A star":
        resultat_json = find_optimal_path_A_star(arbre, gare_arrivée, poids_heure, poids_prix, poids_CO2)
    elif choix_algorithme == "Breadth First Search":
        resultat_json = find_optimal_path_BFS(arbre, gare_arrivée, poids_heure, poids_prix, poids_CO2)

    img_graph = display_graph(data_trains, gare_départ, 0)

    if resultat_json:
        return (f"Heure d'arrivée: {resultat_json['heure']}h\n"
                f"Prix: {resultat_json['prix']}€\n"
                f"CO2: {resultat_json['co2']}gCO2\n"
                f"Chemin: {' -> '.join(resultat_json['path'])}", img_graph)
    else:
        return (f"Aucun chemin trouvé vers {gare_arrivée}", img_graph)


def page_train(numero_page):
    return requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/vehicle_journeys?start_page={}')
        .format(numero_page), auth=(API_KEY_SNCF, ''))


def L2(departure_coord, arrival_coord):
    lat1_km, lon1_km = departure_coord[0] * (40075 / 360), departure_coord[1] * (40075 / 360) * math.cos(math.radians(departure_coord[0]))
    lat2_km, lon2_km = arrival_coord[0] * (40075 / 360), arrival_coord[1] * (40075 / 360) * math.cos(math.radians(arrival_coord[0]))

    distance = math.sqrt((lat2_km - lat1_km)**2 + (lon2_km - lon1_km)**2)
    return distance


def transform_data(api_data):
    trains_demo = {}

    for journey in api_data['vehicle_journeys']:
        train_key = journey['id']
        if train_key not in trains_demo:
            trains_demo[train_key] = {}

        first_stop = journey['stop_times'][0]['stop_point']
        last_stop = journey['stop_times'][-1]['stop_point']

        departure_coord = (float(first_stop['coord']['lat']), float(first_stop['coord']['lon']))
        arrival_coord = (float(last_stop['coord']['lat']), float(last_stop['coord']['lon']))
        distance = L2(departure_coord, arrival_coord)

        trains_demo[train_key]['depart'] = first_stop['name']
        trains_demo[train_key]['arrivee'] = last_stop['name']
        trains_demo[train_key]['prix'] = math.ceil(distance / 10) + np.random.randint(10)
        trains_demo[train_key]['co2'] = math.ceil(distance / 100) + np.random.randint(10)

        depart_hour = int(journey['stop_times'][0]['departure_time'][:2])
        arrivee_hour = int(journey['stop_times'][-1]['arrival_time'][:2])

        trains_demo[train_key]['depart_heure'] = depart_hour
        trains_demo[train_key]['arrivee_heure'] = arrivee_hour

    return trains_demo


def API_call(nb_pages):
    result = {}
    for numero_page in range(nb_pages):
        api_data = page_train(numero_page).json()
        transformed_data = transform_data(api_data)
        result.update(transformed_data)
    return result


def extract_station_names(csv_file):
    station_names = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] != '':
                station_names.append(row['name'])
    return station_names


def get_stations(csv_file):
    stations = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stations.append(row)
    return pd.DataFrame(stations)


def display_train(choix_dataset):

    if choix_dataset == "10 trains synthéthiques":
        return pd.DataFrame(trains_demo).transpose()
    elif choix_dataset == "50 trains synthéthiques":
        return pd.DataFrame(trains).transpose()
    elif choix_dataset == "API SNCF 25 trains":
        nb_pages = 1
    elif choix_dataset == "API SNCF 100 trains":
        nb_pages = 4
    elif choix_dataset == "API SNCF 1000 trains":
        nb_pages = 40

    api_data = API_call(nb_pages)

    train_list = []
    for _, train_info in api_data.items():
        train_dict = {}
        train_dict.update(train_info)
        train_list.append(train_dict)

    train_df = pd.DataFrame(train_list)

    return train_df
