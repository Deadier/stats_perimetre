import csv
import requests
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor

# Définition des opérateurs et générations au niveau global
opérateurs = ["ORANGE", "SFR", "BOUYGUES TELECOM", "FREE MOBILE"]
générations = ["2G", "3G", "4G", "5G"]

def construire_url_api(lat, lon, rayon, opérateur=None, génération=None, pour_pylônes=False):
    """
    Construit l'URL pour l'API ANFR en fonction des paramètres donnés.
    """
    base_url = "https://data.anfr.fr/d4c/api/records/1.0/search/"
    params = {
        "rows": 1000,
        "dataset": "observatoire_2g_3g_4g",
        "refine.statut": ["En service", "Techniquement opérationnel"],
        "lang": "fr"
    }

    if pour_pylônes:
        params["facet"] = "sup_id"
    else:
        if opérateur:
            params["refine.adm_lb_nom"] = opérateur
        if génération:
            params["refine.generation"] = génération

    url_params = urlencode(params, doseq=True)
    url_params = url_params.replace('+', '%20').replace('%2C', ',')
    geofilter = f"geofilter.distance={lat},{lon},{rayon}"
    return f"{base_url}?{url_params}&{geofilter}"

def effectuer_requête_api(url, nb_essais=3, timeout=60):
    """
    Effectue une requête HTTP GET à l'URL spécifiée et renvoie la réponse JSON.
    Réessaye en cas d'échec de la requête jusqu'à un nombre maximal d'essais.
    """
    essai = 0
    while essai < nb_essais:
        try:
            print(f"Essai {essai + 1}: Effectuer requête API: {url}")
            réponse = requests.get(url, timeout=timeout)
            réponse.raise_for_status()
            print("Réponse reçue avec succès.")
            return réponse.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            essai += 1
            if essai == nb_essais:
                return None

def compter_antennes(json_response):
    """
    Compte le nombre d'antennes à partir de la réponse JSON de l'API ANFR.
    """
    antennes = json_response.get("nhits", 0) if json_response else 0
    print(f"Nombre d'antennes trouvées : {antennes}")
    return antennes

def compter_pylônes_uniques(lat, lon, rayon):
    """
    Compte le nombre unique de pylônes dans une zone spécifiée.
    """
    url = construire_url_api(lat, lon, rayon, pour_pylônes=True)
    réponse = effectuer_requête_api(url)
    if réponse:
        pylônes = len(set(record['fields']['sup_id'] for record in réponse.get('records', [])))
        print(f"Nombre de pylônes uniques trouvés : {pylônes}")
        return pylônes
    else:
        return 0

def compter_pylônes_par_opérateur(lat, lon, rayon, opérateur):
    """
    Compte le nombre unique de pylônes pour un opérateur spécifique dans une zone spécifiée.
    """
    url = construire_url_api(lat, lon, rayon, opérateur=opérateur, pour_pylônes=True)
    réponse = effectuer_requête_api(url)
    if réponse:
        pylônes = len(set(record['fields']['sup_id'] for record in réponse.get('records', [])))
        print(f"Nombre de pylônes uniques pour {opérateur} : {pylônes}")
        return pylônes
    else:
        return 0

def traiter_ligne(ligne, rayon):
    """
    Traite chaque ligne du fichier CSV d'entrée avec un rayon spécifié et effectue les requêtes API nécessaires.
    """
    ville, lat, lon, densité = ligne['VILLE'], ligne['LATITUDE'], ligne['LONGITUDE'], ligne['DENSITÉ']
    données_sortie = ligne.copy()

    for op in opérateurs:
        pylônes_opérateur = compter_pylônes_par_opérateur(lat, lon, rayon, op)
        données_sortie[f"PYLONES {op}"] = pylônes_opérateur

        for gen in générations:
            url = construire_url_api(lat, lon, rayon, opérateur=op, génération=gen)
            réponse = effectuer_requête_api(url)
            antennes = compter_antennes(réponse)
            données_sortie[f"{op} {gen}"] = antennes

    pylônes_tous = compter_pylônes_uniques(lat, lon, rayon)
    données_sortie["PYLONES TOUS OPERATEURS"] = pylônes_tous

    return données_sortie

def traiter_fichier(fichier_entrée, fichier_sortie, rayon):
    """
    Traite le fichier CSV d'entrée avec un rayon donné et écrit les résultats dans un fichier de sortie spécifié.
    """
    with open(fichier_entrée, mode='r', encoding='utf-8') as fichier_in, \
         open(fichier_sortie, mode='w', encoding='utf-8', newline='') as fichier_out:

        lecteur_csv = csv.DictReader(fichier_in, delimiter=';')
        noms_colonnes = (lecteur_csv.fieldnames +
                         [f"{op} {gen}" for op in opérateurs for gen in générations] +
                         [f"PYLONES {op}" for op in opérateurs] +
                         ["PYLONES TOUS OPERATEURS"])
        écrivain_csv = csv.DictWriter(fichier_out, fieldnames=noms_colonnes, delimiter=';')
        écrivain_csv.writeheader()

        with ThreadPoolExecutor(max_workers=5) as executor:
            for ligne in lecteur_csv:
                résultat = executor.submit(traiter_ligne, ligne, rayon).result()
                écrivain_csv.writerow(résultat)

# Paramètres de base
fichier_entrée = "entree.csv"
rayons = [1500, 2500, 5000]

# Traitement pour chaque rayon spécifié
for rayon in rayons:
    fichier_sortie = f"sortie_{rayon}.csv"
    print(f"Traitement des données avec un rayon de {rayon} mètres.")
    traiter_fichier(fichier_entrée, fichier_sortie, rayon)

print("Traitement terminé pour tous les rayons.")