import json

def nettoyer_mot(mot):
    corrections = {
        'Ã©': 'é', 'Ã¨': 'è', 'Ã ': 'à', 'Ã§': 'ç', 'Ã´': 'ô',
        'Ãª': 'ê', 'Ã«': 'ë', 'Ã®': 'î', 'Ã¯': 'ï', 'Ã¢': 'â',
        'Ã»': 'û', 'Ã¹': 'ù', 'Ã¤': 'ä', 'Ã¶': 'ö', 'Ã¼': 'ü',
        'â€™': '’',  
    }
    for incorrect, correct in corrections.items():
        mot = mot.replace(incorrect, correct)
    return mot

chemin_fichier = 'BDD.txt'
phrases = []  
phrase_courante = [] 

with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
    for ligne in fichier:
        mots = ligne.strip().split()

        for mot in mots:
            mot_nettoye = nettoyer_mot(mot)
            if mot_nettoye.endswith(')'):
                mot_nettoye = mot_nettoye.rstrip(')')
            if mot_nettoye.endswith('.'):
                mot_nettoye = mot_nettoye.rstrip('.')
                phrase_courante.append(mot_nettoye)
                phrases.append(phrase_courante)
                phrase_courante = []
            else:
                phrase_courante.append(mot_nettoye)


if phrase_courante:
    phrases.append(phrase_courante)

with open('phrases.json', 'w', encoding='utf-8') as fichier_json:
    json.dump(phrases, fichier_json, ensure_ascii=False, indent=4)
