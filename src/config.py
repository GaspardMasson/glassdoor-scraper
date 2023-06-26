import json
import shutil
import os

# Liste des liens à parcourir
liens = [
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?locKeyword=France&srs=RECENT_SEARCHES",
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?fromAge=1",
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?fromAge=3",
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?fromAge=7",
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?fromAge=14",
    "https://www.glassdoor.fr/Emploi/france-data-scientist-emplois-SRCH_IL.0,6_IN86_KO7,21.htm?fromAge=30",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?context=Jobs&clickSource=searchBox",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?fromAge=1",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?fromAge=3",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?fromAge=7",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?fromAge=14",
    "https://www.glassdoor.fr/Emploi/france-data-analyst-emplois-SRCH_IL.0,6_IN86_KO7,19.htm?fromAge=30",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?context=Jobs&clickSource=searchBox",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?fromAge=1",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?fromAge=3",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?fromAge=7",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?fromAge=14",
    "https://www.glassdoor.fr/Emploi/france-data-engineer-emplois-SRCH_IL.0,6_IN86_KO7,20.htm?fromAge=30"
]

# Chemin du fichier config.json
config_file = "config.json"

# Copie du fichier config.json vers un fichier temporaire
temp_config_file = "temp_config.json"
shutil.copyfile(config_file, temp_config_file)

# Parcours des liens et mise à jour du fichier config.json
for lien in liens:
    # Chargement du contenu du fichier temporaire
    with open(temp_config_file, "r") as f:
        config_data = json.load(f)
    
    # Mise à jour du lien dans le fichier config.json
    config_data["base_url"] = lien
    
    # Écriture des modifications dans le fichier temporaire
    with open(temp_config_file, "w") as f:
        json.dump(config_data, f, indent=4)

    # Effacer le contenu du fichier de configuration
    open(config_file, 'w').close()

    # Copie du fichier temporaire vers le fichier de configuration d'origine
    shutil.copyfile(temp_config_file, config_file)

    # Exécution du script principal avec le fichier config.json mis à jour
    os.system("python main.py")
