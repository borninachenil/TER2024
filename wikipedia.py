import wikipediaapi
import json
import sys
import os
import spacy
nlp = spacy.load("fr_core_news_sm")

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

def normal(text):
    return text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace("\n", " ")

def clean(token):
    return token.strip().replace("\n", " ")

def motsphrases(texte):
    texte = normal(texte)
    doc = nlp(texte)
    phrases = []
    phrase_en_cours = []

    for token in doc:
        if token.is_punct and token.text not in {'.', '?', '!', ':', ';', ',', '(', ')'}:
            continue
        mot_nettoye = clean(token.text)
        if mot_nettoye:
            mot_lemmatise = token.lemma_
            mot_dict = {"nom": mot_nettoye, "lemme": mot_lemmatise}
            phrase_en_cours.append(mot_dict)
        if token.text in {'.', '?', '!', ':', ';'}:
            if phrase_en_cours:
                phrases.append(phrase_en_cours)
                phrase_en_cours = []

    if phrase_en_cours:
        phrases.append(phrase_en_cours)

    return phrases

if __name__ == "__main__":
    if len(sys.argv) == 2:
        page_title = sys.argv[1]
    else:
        print("Utilisation : python wikipedia.py NomPageWikipedia")
        sys.exit()

    page_content = wikipedia(page_title)
    if page_content != "La page n'existe pas.":
        phrases = motsphrases(page_content)
        nom_fichier_sans_espaces = page_title.replace(" ", "_").replace("/", "_")
        nom_fichier_json = f"json/{nom_fichier_sans_espaces}.json"
        with open(nom_fichier_json, 'w', encoding='utf-8') as fichier_json:
            json.dump(phrases, fichier_json, ensure_ascii=False, indent=4)
