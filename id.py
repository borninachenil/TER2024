import json

def nettoyer_terme(terme):
    return terme.strip('"').strip()

def charger_dictionnaire(chemin):
    dico = {}
    with open(chemin, 'r', encoding='utf-8', errors="replace") as fichier:
        for ligne in fichier:
            elements = ligne.strip().split(';')
            if len(elements) >= 2:
                id_ = elements[0]
                terme = nettoyer_terme(elements[1])
                dico[terme] = id_ 
    return dico

def trouver_id(mot, dictionnaire):
    return dictionnaire.get(mot)

chemin_dictionnaire = 'dictionnaire.txt'
dictionnaire_termes = charger_dictionnaire(chemin_dictionnaire)
chemin_json = 'phrases.json'
with open(chemin_json, 'r', encoding='utf-8', errors="replace") as fichier_json:
    phrases = json.load(fichier_json)
phrases_avec_id = []
for phrase in phrases:
    nouvelle_phrase = []
    for mot in phrase:
        id_mot = trouver_id(mot, dictionnaire_termes) 
        if id_mot:
            nouvelle_phrase.append({'mot': mot, 'id': id_mot})
        else:
            nouvelle_phrase.append({'mot': mot})
    phrases_avec_id.append(nouvelle_phrase)
chemin_sortie_json = 'phrases_avec_id.json'
with open(chemin_sortie_json, 'w', encoding='utf-8') as fichier_sortie:
    json.dump(phrases_avec_id, fichier_sortie, ensure_ascii=False, indent=4)

