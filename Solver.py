import networkx as nx
import matplotlib.pyplot as plt


def transform_data_tree(trains, gare, heure, prix, co2):
    noeud = {'gare': gare, 'heure': heure, 'prix': prix, 'co2': co2, 'trains': []}
    for train_id, train_info in trains.items():
        if (gare == "" or train_info['depart'] == gare) and train_info['depart_heure'] > heure:
            prochaine_gare = train_info['arrivee']
            prochaine_heure = train_info['arrivee_heure']
            prochain_prix = prix + train_info['prix']
            prochain_co2 = co2 + train_info['co2']
            prochain_noeud = transform_data_tree(trains, prochaine_gare, prochaine_heure, prochain_prix, prochain_co2)
            noeud['trains'].append({train_id: prochain_noeud})
    return noeud


def transform_tree_graph(arbre, parent=None, graph=None):
    if graph is None:
        graph = nx.DiGraph()
    current_node = arbre['gare'] + '_' + str(arbre['heure']) + '_' + str(arbre['prix']) + '_' + str(arbre['co2'])
    if parent:
        parent_node = parent['gare'] + '_' + str(parent['heure']) + '_' + str(parent['prix']) + '_' + str(parent['co2'])
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
    pos = nx.spring_layout(graph)

    # Trouver le nœud initial
    initial_node = None
    for node in graph.nodes():
        if graph.in_degree(node) == 0:
            initial_node = node
            break

    # Définition des options
    node_colors = ['red' if node == initial_node else 'lightblue' for node in graph.nodes()]
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
    plt.show()

    return None


def heuristique(heure, prix, co2):
    poids_heure = 1
    poids_prix = 2
    poids_co2 = 3

    valeur_heuristique = poids_heure * heure + poids_prix * prix + poids_co2 * co2

    return valeur_heuristique


def find_optimal_path_DFS(node, destination, current_time=0, current_price=0, current_co2=0):
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
        next_price = current_price + train[nom_train]['prix']
        next_co2 = current_co2 + train[nom_train]['co2']

        path_result = find_optimal_path_DFS(next_node, destination, next_time, next_price, next_co2)

        if path_result:
            path_result['path'].insert(0, nom_train)
            path_result['path'].insert(0, node['gare'])
            if not best_path:
                best_path = path_result
            else:
                heuristique_path = heuristique(path_result['heure'], path_result['prix'], path_result['co2'])
                heuristique_best_path = heuristique(best_path['heure'], best_path['prix'], best_path['co2'])
                if heuristique_path < heuristique_best_path:
                    best_path = path_result

    return best_path


def find_optimal_journey(trains_data, voyageur):
    arbre = transform_data_tree(trains_data, voyageur['depart'], 0, 0, 0)

    display_graph(trains_data, voyageur['depart'], 0)

    resultat = find_optimal_path_DFS(arbre, voyageur['arrivee'])
    if resultat:
        print("Chemin optimal vers", voyageur['arrivee'], ":")
        print("Heure:", resultat['heure'])
        print("Prix:", resultat['prix'])
        print("CO2:", resultat['co2'])
        print("Chemin:", ' -> '.join(resultat['path']))
    else:
        print("Aucun chemin trouvé vers", voyageur['arrivee'])


voyageur = {"depart": "Gare1", "arrivee": "Gare4", "date_depart": 7}
trains = {
    'train_0': {"depart": "Gare1", "arrivee": "Gare2", "prix": 50, "co2": 10, "depart_heure": 8, "arrivee_heure": 10},
    'train_1': {"depart": "Gare2", "arrivee": "Gare3", "prix": 40, "co2": 8, "depart_heure": 11, "arrivee_heure": 13},
    'train_2': {"depart": "Gare3", "arrivee": "Gare1", "prix": 10, "co2": 4, "depart_heure": 15, "arrivee_heure": 18},
    'train_3': {"depart": "Gare1", "arrivee": "Gare2", "prix": 30, "co2": 11, "depart_heure": 1, "arrivee_heure": 5},
    'train_4': {"depart": "Gare2", "arrivee": "Gare1", "prix": 30, "co2": 11, "depart_heure": 2, "arrivee_heure": 4},
    'train_5': {"depart": "Gare2", "arrivee": "Gare3", "prix": 30, "co2": 11, "depart_heure": 7, "arrivee_heure": 15},
    'train_6': {"depart": "Gare1", "arrivee": "Gare5", "prix": 60, "co2": 15, "depart_heure": 9, "arrivee_heure": 12},
    'train_7': {"depart": "Gare2", "arrivee": "Gare4", "prix": 45, "co2": 12, "depart_heure": 12, "arrivee_heure": 16},
    'train_8': {"depart": "Gare3", "arrivee": "Gare5", "prix": 55, "co2": 14, "depart_heure": 18, "arrivee_heure": 25},
    'train_9': {"depart": "Gare4", "arrivee": "Gare1", "prix": 50, "co2": 13, "depart_heure": 16, "arrivee_heure": 19},
    'train_10': {"depart": "Gare5", "arrivee": "Gare2", "prix": 50, "co2": 13, "depart_heure": 18, "arrivee_heure": 20},
}

find_optimal_journey(trains, voyageur)
