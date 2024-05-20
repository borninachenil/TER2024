import wikipediaapi
import json
import sys
import re
import os

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
        'â€™': ' ', '(' : '' , ')' : '',
    }
    for incorrect, correct in corrections.items():
        mot = mot.replace(incorrect, correct)
    mot = mot.strip(":,;!?()[]«»{}%1234567890/\\")
    return mot if mot else None

def toMots(texte):
    pattern = re.compile(r"\b\w+'?\w*\b\.?")
    mots_trouves = pattern.findall(texte)
    mots_nettoyes = []
    for mot in mots_trouves:
        mot_nettoye = clean(mot)
        if mot_nettoye:
            if "'" in mot_nettoye:
                partie1, partie2 = mot_nettoye.split("'", 1)
                mots_nettoyes.append(partie1 + "'")
                mots_nettoyes.append(partie2)
            else:
                mots_nettoyes.append(mot_nettoye)
    return mots_nettoyes

def creerPhrases(mots):
    phrases = []
    phrase_en_cours = []
    for mot in mots:
        if mot.endswith('.'):
            phrase_en_cours.append(mot[:-1])
            phrases.append(phrase_en_cours)
            phrase_en_cours = []
        else:
            phrase_en_cours.append(mot)
    if phrase_en_cours:
        phrases.append(phrase_en_cours)
    return phrases

def Dictionnaire(chemin):
    dico = {}
    with open(chemin, 'r', encoding='utf-8', errors="replace") as fichier:
        for ligne in fichier:
            elements = ligne.strip().split(';')
            if len(elements) >= 2:
                id_, terme = elements[0], elements[1].strip('"')
                dico[terme.lower()] = id_
    return dico

def id(mots, dictionnaire):
    return [{"mot": mot, "id": dictionnaire.get(mot.lower(), "NULL")} for mot in mots]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        page_title = sys.argv[1]
    else:
        print("Utilisation : python wikipedia.py NomPageWikipedia")
        sys.exit()

    page_content = wikipedia(page_title)
    if page_content != "La page n'existe pas.":
        mots = toMots(page_content)
        phrases = creerPhrases(mots)
        dictionnaire_termes = Dictionnaire('singleton.txt')
        mots_avec_id = [id(phrase, dictionnaire_termes) for phrase in phrases]
        nom_fichier_sans_espaces = page_title.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        nom_fichier_json = f"json/{nom_fichier_sans_espaces}.json"
        with open(nom_fichier_json, 'w', encoding='utf-8') as fichier_json:
            json.dump(mots_avec_id, fichier_json, ensure_ascii=False, indent=4)