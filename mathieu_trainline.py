import trainline
from geopy.geocoders import Nominatim


results = trainline.search(
    departure_station="Paris",
    arrival_station="Lyon",
    from_date="09/03/2024 08:00",
    to_date="09/03/2024 21:00")

print(results.csv())


def obtenir_coordonnees_ville(ville):
    geolocator = Nominatim(user_agent="mon_application")
    location = geolocator.geocode(ville)
    return (location.latitude, location.longitude)


print(obtenir_coordonnees_ville("Lille"))
