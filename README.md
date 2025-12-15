Features: 

Lecture d’un fichier JSON ligne par ligne 
Agrégation du chiffre d’affaires par marketplace
Calcul du chiffre d’affaires total 
Détection des commandes suspectes : 
- Montant invalide - Montant négatif 
- Marketplace manquante 
- Date invalide 
- Filtrage optionnel par date de création (`created_at`) 


Récupérer le projet depuis Git : 

git clone <URL_DU_REPO_GIT>
cd ecom-orders-Vigie

Lancer projet : 

python tests.py
python tests.py TestOrdersProcessing.test_with_display
python tests.py TestOrdersProcessing.test_basic_aggregation
python tests.py TestOrdersProcessing.test_created_at_filter


Questions “mindset”

Si ce programme tournait en production, que surveiller / logger en priorité ?
-- Erreurs de parsing JSON car sans lecture valide du fichier, le traitement s’arrête.
-- Nombre de commandes traitées
-- Nombre et type de commandes suspectes
Si le fichier passait de 10 Ko → 10 Go, que changerais-tu dans ton approche ?
-- si le fichier passe de 10Ko a 10Go on essaye de  lire le fichier ligne par ligne, éviter toute accumulation d’objets en mémoire, de remplacer les logs détaillés par des métriques agrégées et de parser uniquement les champs nécessaires.
Quel est selon toi le cas de test prioritaire, et pourquoi ?
-- Le cas prioritaire est la gestion des montants invalides ou négatifs, car il impacte directement le chiffre d’affaires, il révèle souvent des erreurs de données ou de flux amont et il peut fausser tous les calculs financiers
