import subprocess
import os
if os.path.exists("wikipedia"):
    fichiers = os.listdir("wikipedia")
    for fichier in fichiers:
        chemin_complet = os.path.join("wikipedia", fichier)
        if os.path.isfile(chemin_complet):
            titre_page = fichier.replace(".txt", "")
            commande = ["python", "wikipedia.py", titre_page]
            subprocess.run(commande)
