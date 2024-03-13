import networkx as nx
import matplotlib.pyplot as plt

trains = {
    'train_0': {"depart": "Paris", "arrivee": "Marseille", "prix": 80, "co2": 20, "depart_heure": 8, "arrivee_heure": 12},
    'train_1': {"depart": "Marseille", "arrivee": "Lyon", "prix": 40, "co2": 10, "depart_heure": 11, "arrivee_heure": 13},
    'train_2': {"depart": "Lyon", "arrivee": "Paris", "prix": 60, "co2": 10, "depart_heure": 15, "arrivee_heure": 17},
    'train_3': {"depart": "Paris", "arrivee": "Marseille", "prix": 70, "co2": 20, "depart_heure": 1, "arrivee_heure": 5},
    'train_4': {"depart": "Marseille", "arrivee": "Paris", "prix": 80, "co2": 20, "depart_heure": 2, "arrivee_heure": 6},
    'train_5': {"depart": "Marseille", "arrivee": "Lyon", "prix": 30, "co2": 10, "depart_heure": 13, "arrivee_heure": 15},
    'train_6': {"depart": "Paris", "arrivee": "Nice", "prix": 90, "co2": 30, "depart_heure": 9, "arrivee_heure": 15},
    'train_7': {"depart": "Marseille", "arrivee": "Bordeaux", "prix": 50, "co2": 15, "depart_heure": 12, "arrivee_heure": 16},
    'train_8': {"depart": "Lyon", "arrivee": "Nice", "prix": 50, "co2": 15, "depart_heure": 18, "arrivee_heure": 22},
    'train_9': {"depart": "Bordeaux", "arrivee": "Paris", "prix": 50, "co2": 15, "depart_heure": 16, "arrivee_heure": 18},
    'train_10': {"depart": "Nice", "arrivee": "Marseille", "prix": 30, "co2": 10, "depart_heure": 18, "arrivee_heure": 20},
}


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


def lister_gares(trains):
    gares = set()
    for _, details in trains.items():
        gares.add(details['depart'])
        gares.add(details['arrivee'])

    return list(gares)


def find_optimal_journey(gare_départ, gare_arrivée, heure_départ, poids_heure, poids_prix, poids_CO2):
    heure_départ = float(heure_départ)

    arbre = transform_data_tree(trains, gare_départ, heure_départ, 0, 0)

    resultat_json = find_optimal_path_DFS(arbre, gare_arrivée, poids_heure, poids_prix, poids_CO2)

    img_graph = display_graph(trains, gare_départ, 0)

    if resultat_json:
        return (f"Heure: {resultat_json['heure']}h\n"
                f"Prix: {resultat_json['prix']}€\n"
                f"CO2: {resultat_json['co2']}gCO2\n"
                f"Chemin: {' -> '.join(resultat_json['path'])}", img_graph)
    else:
        return (f"Aucun chemin trouvé vers {gare_arrivée}", img_graph)
