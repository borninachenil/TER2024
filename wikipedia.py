import wikipediaapi
import json
import os
import sys

def wikipedia(page_title):
    chemin_fichier_texte = f"wikipedia/{page_title}.txt"
    if os.path.exists(chemin_fichier_texte):
        with open(chemin_fichier_texte, 'r', encoding='utf-8') as fichier:
            print("La page existe déjà dans nos fichiers")
            return fichier.read()
    else:
        wiki_wiki = wikipediaapi.Wikipedia(language='fr', user_agent='SemanticExplorers/1.0 (theo.flament@etu.umontpellier.fr)')
        page = wiki_wiki.page(page_title)
        if page.exists():
            with open(chemin_fichier_texte, 'w', encoding='utf-8') as fichier:
                fichier.write(page.text)
            return page.text
        else:
            return "La page n'existe pas."

def clean(mot):
    corrections = {
        'Ã©': 'é', 'Ã¨': 'è', 'Ã ': 'à', 'Ã§': 'ç', 'Ã´': 'ô',
        'Ãª': 'ê', 'Ã«': 'ë', 'Ã®': 'î', 'Ã¯': 'ï', 'Ã¢': 'â',
        'Ã»': 'û', 'Ã¹': 'ù', 'Ã¤': 'ä', 'Ã¶': 'ö', 'Ã¼': 'ü',
        'â€™': '’', '(' : '' , ')' : '', '.' : '',
    }
    for incorrect, correct in corrections.items():
        mot = mot.replace(incorrect, correct)
    mot = mot.strip(":,;!?()[]«»{}%1234567890")
    return mot if mot else None

def toMot(texte):
    mots = texte.replace("\n", " ").replace("'", " ").split(" ")
    mots_nettoyes = [clean(mot) for mot in mots if mot]
    return [mot_nettoye for mot_nettoye in mots_nettoyes if mot_nettoye is not None]

def Dictionnaire(chemin):
    dico = {}
    with open(chemin, 'r', encoding='utf-8', errors="replace") as fichier:
        for ligne in fichier:
            elements = ligne.strip().split(';')
            if len(elements) >= 2:
                id_, terme = elements[0], elements[1].strip('"')
                dico[terme] = id_
    return dico

def id(mots, dictionnaire):
    return [{"mot": mot, "id": dictionnaire.get(mot, "NULL")} for mot in mots if mot is not None]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        page_title = sys.argv[1]
    else:
        print("Utilisation : python wikipedia.py NomPageWikipedia")
        sys.exit()
    page_content = wikipedia(page_title)
    mots = toMot(page_content)
    dictionnaire_termes = Dictionnaire('dictionnaire.txt')
    mots_avec_id = id(mots, dictionnaire_termes)
    if not os.path.exists('wikipedia'):
        os.makedirs('wikipedia')
    if not os.path.exists('json'):
        os.makedirs('json')
    nom_fichier_sans_espaces = page_title.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    chemin_fichier_texte = f"wikipedia/{nom_fichier_sans_espaces}.txt"
    chemin_fichier_json = f"json/{nom_fichier_sans_espaces}.json"
    with open(chemin_fichier_texte, 'w', encoding='utf-8') as fichier_texte:
        fichier_texte.write(page_content)
    with open(chemin_fichier_json, 'w', encoding='utf-8') as fichier_json:
        json.dump(mots_avec_id, fichier_json, ensure_ascii=False, indent=4)
