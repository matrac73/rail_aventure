import folium
from datetime import datetime
import webbrowser
import trainline
from geopy.geocoders import Nominatim
import csv
import pyautogui


def afficher_train(coord_depart, coord_arrivee, heure_depart, heure_arrivee, m):

    # Ajout de la ligne reliant les points de départ et d'arrivée
    folium.PolyLine(
        locations=[coord_depart, coord_arrivee],
        color='blue',
        opacity=0.5).add_to(m)

    # Calcul de l'intervalle de temps entre l'heure de départ et d'arrivée
    heure_depart = datetime.strptime(heure_depart, "%H:%M")
    heure_arrivee = datetime.strptime(heure_arrivee, "%H:%M")
    # heure_actuelle_str = datetime.now().strftime("%H:%M")
    heure_actuelle_str = "15:00"
    heure_actuelle = datetime.strptime(heure_actuelle_str, "%H:%M")

    # Vérification si l'heure actuelle est avant/après l'heure de départ
    if heure_actuelle < heure_depart:
        return coord_depart

    elif heure_actuelle > heure_arrivee:
        return coord_arrivee

    # Calcul de la progression entre les coordonnées
    duree_trajet = heure_arrivee - heure_depart
    duree_ecoulee = heure_actuelle - heure_depart
    progression = duree_ecoulee.total_seconds() / duree_trajet.total_seconds()

    # Interpolation linéaire pour déterminer les coordonnées actuelles
    coord_actuelle = (
        coord_depart[0] + (coord_arrivee[0] - coord_depart[0]) * progression,
        coord_depart[1] + (coord_arrivee[1] - coord_depart[1]) * progression
    )

    folium.Marker(
            location=coord_actuelle,
            icon=folium.Icon(color='red'),
            popup=f"Time: {heure_actuelle}"
            ).add_to(m)


def obtenir_coordonnees_ville(ville):
    geolocator = Nominatim(user_agent="mon_application")
    location = geolocator.geocode(ville)
    return (location.latitude, location.longitude)


def convertir_heure(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y %H:%M').strftime('%H:%M')


def extraire_informations_ligne(ligne):
    infos = ligne.split(';')
    heure_depart = convertir_heure(infos[0])
    heure_arrivee = convertir_heure(infos[1])
    return heure_depart, heure_arrivee


def afficher_html(chemin_fichier_html, count):
    if count == 0:
        webbrowser.open('file://' + chemin_fichier_html)
    else:
        pyautogui.hotkey('command', 'r')


def load_stations(file):
    with open(file, newline='', encoding='utf-8') as csvfile:
        stations_reader = csv.reader(csvfile, delimiter=';')
        stations = [element[1] for element in list(stations_reader)]
        return stations


def afficher_trajet(departure_station, arrival_station, departure_date, arrival_date, m):
    coord_depart = obtenir_coordonnees_ville(departure_station)
    coord_arrivee = obtenir_coordonnees_ville(arrival_station)

    try:
        results = trainline.search(
            departure_station=departure_station,
            arrival_station=arrival_station,
            from_date=departure_date,
            to_date=arrival_date)

        for ligne in results.csv().split('\n')[1:]:  # Ignorer la première ligne qui contient les en-têtes
            if ligne.strip():  # Vérifie si la ligne n'est pas vide
                heure_depart, heure_arrivee = extraire_informations_ligne(ligne)
                afficher_train(coord_depart, coord_arrivee, heure_depart, heure_arrivee, m)

    except Exception as e:
        print(e)


def main(departure_date, arrival_date, chemin_html):
    m = folium.Map(location=[47, 2], zoom_start=6)
    count = 0
    stations = load_stations('stations.csv')
    for departure_station in stations:
        for arrival_station in stations:
            if departure_station != arrival_station:
                print("Trajet de {} à {} de {} à {}".format(departure_station, arrival_station, departure_date, arrival_date))
                afficher_trajet(departure_station, arrival_station, departure_date, arrival_date, m)
                m.save('carte_trajet.html')
                afficher_html(chemin_html, count)
                count += 1


chemin_html = '/Users/mathieu/Documents/Perso/rail_aventure/carte_trajet.html'
departure_date = "10/03/2024 12:00"
arrival_date = "10/03/2024 18:00"

main(departure_date, arrival_date, chemin_html)
