<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAK Scraper Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }

        h1, h2, h3 {
            color: #333;
        }

        pre {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }

        code {
            font-family: "Courier New", Courier, monospace;
            color: #d6336c;
        }

        a {
            color: #1d68a7;
        }

        footer {
            margin-top: 20px;
            text-align: center;
            font-size: 0.9em;
        }
    </style>
</head>
<body>

    <h1>WAK Scraper</h1>
    <p><strong>WAK Scraper</strong> est une bibliothèque Python permettant de récupérer des données financières des sociétés cotées à la Bourse de Casablanca, telles que les dividendes, les cours historiques des actions, et d'autres informations disponibles sur le site officiel.</p>

    <h2>Installation</h2>
    <p>Pour installer WAK, utilisez la commande suivante :</p>
    <pre><code>pip install wak</code></pre>

    <h2>Utilisation</h2>
    <h3>Fonction principale : <code>get_stock_history()</code></h3>
    <p>La fonction <code>get_stock_history()</code> permet d'importer l'historique des cours des actions de la Bourse de Casablanca.</p>
    <p><strong>Paramètres :</strong></p>
    <ul>
        <li><code>names</code> : Le ticker (symbole) de l'action, par exemple <code>"BCP"</code> pour la Banque Centrale Populaire.</li>
        <li><code>start</code> : La date de début au format <code>"YYYY-MM-DD"</code>.</li>
        <li><code>end</code> : La date de fin au format <code>"YYYY-MM-DD"</code>.</li>
    </ul>

    <p><strong>Exemple d'utilisation :</strong></p>
    <pre><code>from wak import get_stock_history

# Récupérer les cours historiques de la BCP entre 2020-01-01 et 2020-12-31
get_stock_history(names="BCP", start="2020-01-01", end="2020-12-31")</code></pre>

    <h3>Autres Fonctions</h3>

    <h4><code>get_dividendes(name)</code></h4>
    <p>La fonction <code>get_dividendes()</code> renvoie les dividendes versés par une société cotée.</p>
    <p><strong>Exemple d'utilisation :</strong></p>
    <pre><code>from wak import get_dividendes

# Récupérer les dividendes de la BCP
get_dividendes(name="BCP")</code></pre>

    <h4><code>get_ratios(name)</code></h4>
    <p>La fonction <code>get_ratios()</code> renvoie les principaux ratios boursiers d'une société cotée.</p>
    <p><strong>Exemple d'utilisation :</strong></p>
    <pre><code>from wak import get_ratios

# Récupérer les ratios boursiers de la BCP
get_ratios(name="BCP")</code></pre>

    <h4><code>get_carnet_ordres(name)</code></h4>
    <p>La fonction <code>get_carnet_ordres()</code> renvoie le carnet d'ordres (ordres d'achat et de vente) d'une action pour la journée en cours.</p>
    <p><strong>Exemple d'utilisation :</strong></p>
    <pre><code>from wak import get_carnet_ordres

# Récupérer le carnet d'ordres de la BCP pour aujourd'hui
get_carnet_ordres(name="BCP")</code></pre>

    <h2>Contribuer</h2>
    <p>Les contributions sont les bienvenues ! N'hésitez pas à soumettre des demandes de fonctionnalités, des rapports de bugs, ou des pull requests via notre <a href="https://github.com/votre-utilisateur/WAK">dépôt GitHub</a>.</p>

    <h2>Contact</h2>
    <p>Pour plus d'informations, visitez notre <a href="https://votre-site-web.com">site web</a> ou contactez-nous à <a href="mailto:votre.email@example.com">votre.email@example.com</a>.</p>

    <footer>
        <p>&copy; 2024 WAK Scraper - Tous droits réservés</p>
    </footer>

</body>
</html>
