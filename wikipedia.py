import wikipediaapi
import json
import sys

def wikipedia(page_title):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='fr',
        user_agent='SemanticExplorers/1.0 (theo.flament@etu.umontpellier.fr)'
    )
    page = wiki_wiki.page(page_title)
    return page.text if page.exists() else f"La page n'existe pas."

def clean(mot):
    corrections = {
        'Ã©': 'é', 'Ã¨': 'è', 'Ã ': 'à', 'Ã§': 'ç', 'Ã´': 'ô',
        'Ãª': 'ê', 'Ã«': 'ë', 'Ã®': 'î', 'Ã¯': 'ï', 'Ã¢': 'â',
        'Ã»': 'û', 'Ã¹': 'ù', 'Ã¤': 'ä', 'Ã¶': 'ö', 'Ã¼': 'ü',
        'â€™': '’', '(' : '' , ')' : '',
    }
    for incorrect, correct in corrections.items():
        mot = mot.replace(incorrect, correct)
    return mot

def toMot(texte):
    mots = texte.replace("\n", " ").split(" ")
    mots_nettoyes = [clean(mot) for mot in mots if mot]
    return mots_nettoyes
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
    return [{"mot": mot, "id": dictionnaire.get(mot, "NULL")} for mot in mots]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        page_title = sys.argv[1]
    else:
        print("python wikipedia.py NomPageWikipedia")
        sys.exit()
    page_content = wikipedia(page_title)
    mots = toMot(page_content)
    dictionnaire_termes = Dictionnaire('dictionnaire.txt')
    mots_avec_id = id(mots, dictionnaire_termes)
    nom_fichier_sans_espaces = page_title.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    nom_fichier_json = f"{nom_fichier_sans_espaces}_resultat_final.json"
    with open(nom_fichier_json, 'w', encoding='utf-8') as fichier_json:
        json.dump(mots_avec_id, fichier_json, ensure_ascii=False, indent=4)
