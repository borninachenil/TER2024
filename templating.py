import subprocess
import os

def call():
    if not os.path.exists('relations') or not os.path.exists('json'):
        print("erreur dossier inexistant!")
        return
    relations = os.listdir('relations')
    json = os.listdir('json')
    for fichier_relation in relations:
        for fichier_json in json:
            chemin_relation = os.path.join('relations', fichier_relation)
            chemin_json = os.path.join('json', fichier_json)
            commande = ['python', 'template.py', chemin_relation, chemin_json]
            subprocess.run(commande)
            print(f"Script template.py appelé pour {chemin_relation} et {chemin_json}")

if __name__ == "__main__":
    call()
