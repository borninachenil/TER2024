import json
import sys

def charger_paires(relations):
    paires = {}
    with open(relations, 'r', encoding='utf-8', errors='ignore') as f:
        for ligne in f:
            elements = ligne.strip().split(';')
            if len(elements) >= 3:
                if '>' in elements[1]:
                    terme1_options = elements[1].split('>')
                    for terme1 in terme1_options:
                        paires[(terme1.strip(), elements[2].strip())] = True
                else:
                    terme1 = elements[1].strip()
                    paires[(terme1, elements[2].strip())] = True
    return paires
def term_exists_in_phrase(term, mots):
    term_words = term.split()
    if not term_words:
        return -1 
    term_length = len(term_words)
    
    for i in range(len(mots) - term_length + 1):
        if mots[i] == term_words[0]:  
            match = True
            for j in range(1, term_length): 
                if i+j >= len(mots) or mots[i+j] != term_words[j]:
                    match = False
                    break
            if match:
                return i  
    return -1
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
def extraire_mots_intermediaires(json_filename, relations_filename, paires, resultats_existant):
    with open(json_filename, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    nom_fichier_relations = relations_filename.split('/')[-1]
    for phrase in data:
        mots = [mot['mot'] for mot in phrase]
        for (terme1, terme2), _ in paires.items():
            index1 = term_exists_in_phrase(terme1, mots)
            index2 = term_exists_in_phrase(terme2, mots)
            if index1 != -1 and index2 != -1:
                end_index1 = index1 + len(terme1.split()) 
                start_index2 = index2 if index1 < index2 else index2 + len(terme2.split())
                if index1 < index2:  
                    mots_intermediaires = " ".join(mots[end_index1:start_index2])
                else: 
                    mots_intermediaires = " ".join(mots[start_index2:end_index1])
                if (abs(index1 - index2) <= 7 or abs(end_index1 - start_index2) <= 7) and mots_intermediaires.strip(): 
                    cle = (mots_intermediaires, nom_fichier_relations)
                    resultats_existant[cle] = resultats_existant.get(cle, 0) + 1    
    return resultats_existant
def enregistrer_resultats(resultats_existant, fichier_template):
    lignes = [f"{mots_intermediaires};{relation.split('\\')[-1]};{occurrences}\n" for ((mots_intermediaires, relation), occurrences) in resultats_existant.items()]
    with open(fichier_template, 'w', encoding='utf-8') as f:
        f.writelines(lignes)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py relations json_file")
        sys.exit(1)
    relations_filename = sys.argv[1]
    json_filename = sys.argv[2]
    fichier_template = "template.txt"
    paires = charger_paires(relations_filename)
    resultats_existant = charger_resultats_existants(fichier_template)
    resultats_mis_a_jour = extraire_mots_intermediaires(json_filename, relations_filename, paires, resultats_existant)
    enregistrer_resultats(resultats_mis_a_jour, fichier_template)

    print("Traitement terminé.")
