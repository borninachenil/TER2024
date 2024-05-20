import subprocess
import os
if os.path.exists("json"):
    fichiers = os.listdir("json")
    for fichier in fichiers:
        chemin_complet = os.path.join("json", fichier)
        if os.path.isfile(chemin_complet):
            titre_page = fichier
            commande = ["python", "result.py", f"json/{titre_page}"]
            subprocess.run(commande)
