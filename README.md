#### Description

Ce script est conçu pour analyser les données sur les antennes et pylônes de téléphonie mobile dans différentes zones géographiques. Il effectue des requêtes à l'API de l'ANFR (Agence Nationale des Fréquences) pour obtenir des informations sur le nombre d'antennes et de pylônes pour différents opérateurs télécoms et différentes générations de réseaux mobiles (2G, 3G, 4G, 5G).

#### Fonctionnalités

-   **Traitement de** **d****onnées** **g****éographiques** : Le script lit un fichier CSV contenant des informations géographiques (Ville, Latitude, Longitude, Densité).
    
-   **Requêtes API** **m****ultiples** : Pour chaque ligne du fichier CSV, il effectue plusieurs requêtes à l'API de l'ANFR pour obtenir des données sur les antennes et pylônes.
    
-   **Traitement par** **r****ayon** : Le script exécute trois passages sur les données, chacun avec un rayon différent (1500, 2500, et 5000 mètres), et stocke les résultats dans des fichiers distincts.
    
-   **Gestion d'****e****rreurs de** **c****onnexion** : En cas d'erreur de connexion ou de délai d'attente expiré, il tente de réexécuter la requête.
    

#### Structure du script

1.  **Définition des** **f****onctions**
    
    -   `construire_url_api`: Construit l'URL pour les requêtes à l'API de l'ANFR.
        
    -   `effectuer_requête_api`: Envoie une requête GET à l'URL spécifiée et retourne la réponse JSON.
        
    -   `compter_antennes`: Compte le nombre d'antennes à partir de la réponse JSON.
        
    -   `compter_pylônes_uniques`: Compte le nombre unique de pylônes dans une zone spécifiée.
        
    -   `compter_pylônes_par_opérateur`: Compte les pylônes spécifiques à chaque opérateur.
        
    -   `traiter_ligne`: Traite chaque ligne du fichier CSV et effectue les requêtes API nécessaires.
        
    -   `traiter_fichier`: Orchestre le traitement du fichier CSV d'entrée et écrit les résultats dans un fichier de sortie.
        
2.  **Exécution** **p****rincipale**
    
    -   Le script lit le fichier CSV d'entrée.
        
    -   Il exécute le traitement pour chaque rayon spécifié (1500, 2500, 5000 mètres).
        
    -   Les résultats sont enregistrés dans des fichiers de sortie distincts (`sortie_1500.csv`, `sortie_2500.csv`, `sortie_5000.csv`).
        

#### Utilisation

1.  Préparez un fichier CSV d'entrée nommé `entree.csv` avec les colonnes suivantes : VILLE, LATITUDE, LONGITUDE, DENSITÉ.
    
2.  Exécutez le script Python. Il lira le fichier d'entrée et effectuera le traitement.
    
3.  Consultez les fichiers de sortie générés pour voir les résultats du traitement.
    

#### Gestion des erreurs

-   Le script gère les erreurs de connexion et de délai d'attente lors des requêtes API.
    
-   En cas d'échec de la requête, le script tente de la réexécuter jusqu'à trois fois.
    

#### Configuration et dépendances

-   Python 3.x est requis.
    
-   La bibliothèque `requests` est utilisée pour effectuer des requêtes HTTP.
    
-   Assurez-vous que votre environnement Python dispose d'une connexion Internet stable.
    

#### Logs et suivi

-   Le script fournit des logs détaillés sur les requêtes effectuées, les erreurs rencontrées, et les résultats obtenus.
    
-   Ces logs aident à suivre le progrès et à diagnostiquer les problèmes éventuels.
