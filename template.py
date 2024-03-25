import json
import sys

def charger_paires(relations):
    paires = {}
    with open(relations, 'r', encoding='utf-8', errors='ignore') as f:
        for ligne in f:
            elements = ligne.strip().split(';')
            if len(elements) >= 3:
                paires[(elements[1], elements[2])] = True
    return paires

def charger_resultats_existants(fichier_template):
    resultats_existant = {}
    try:
        with open(fichier_template, 'r', encoding='utf-8') as f:
            for ligne in f:
                elements = ligne.strip().split(';')
                if len(elements) == 3:
                    cle = (elements[0], elements[1])
                    resultats_existant[cle] = int(elements[2])
    except FileNotFoundError:
        pass
    return resultats_existant

def extraire_mots_intermediaires(json_filename, paires, resultats_existant):
    with open(json_filename, 'r', encoding='utf-8' , errors='ignore') as f:
        data = json.load(f)

    for phrase in data:
        mots = [mot['mot'] for mot in phrase]
        n = len(mots)
        for i in range(n):
            for j in range(i + 2, min(i + 9, n)):
                pair_directe = (mots[i], mots[j])
                if pair_directe in paires or pair_directe[::-1] in paires:
                    mots_intermediaires = " ".join(mots[i+1:j])
                    cle = (mots_intermediaires, relations)
                    resultats_existant[cle] = resultats_existant.get(cle, 0) + 1
    return resultats_existant

def enregistrer_resultats(resultats_existant, fichier_template):
    lignes = [f"{mots_intermediaires};{relations.split('\\')[-1]};{occurrences}\n" for (mots_intermediaires, relations), occurrences in resultats_existant.items()]
    with open(fichier_template, 'w', encoding='utf-8') as f:
        f.writelines(lignes)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py relations json_file")
        sys.exit(1)
    
    relations = sys.argv[1]
    json_filename = sys.argv[2]
    fichier_template = 'template.txt'
    
    paires = charger_paires(relations)
    resultats_existant = charger_resultats_existants(fichier_template)
    resultats_mis_a_jour = extraire_mots_intermediaires(json_filename, paires, resultats_existant)
    
    enregistrer_resultats(resultats_mis_a_jour, fichier_template)

    print("Traitement terminé.")