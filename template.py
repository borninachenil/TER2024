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

def distance(mots_lemmes, mots_normaux, paires, resultats_existant, nom_fichier_relations):
    for (terme1, terme2), _ in paires.items():
        index1 = existe(terme1, mots_lemmes)
        index2 = existe(terme2, mots_lemmes)
        if index1 != -1 and index2 != -1:
            end_index1 = index1 + len(terme1.split())
            start_index2 = index2 if index1 < index2 else index2 + len(terme2.split())
            mots_intermediaires_lemmes = " ".join(mots_lemmes[end_index1:start_index2] if index1 < index2 else mots_lemmes[start_index2:end_index1])
            mots_intermediaires_normaux = " ".join(mots_normaux[end_index1:start_index2] if index1 < index2 else mots_normaux[start_index2:end_index1])

            if (abs(index1 - index2) <= 7 or abs(end_index1 - start_index2) <= 7) and (abs(index1 - index2) > 1 or abs(end_index1 - start_index2) > 1):
                cle = nom_fichier_relations
                if cle not in resultats_existant:
                    resultats_existant[cle] = {'lemme': {}, 'normal': {}}

                if mots_intermediaires_lemmes.strip():
                    if mots_intermediaires_lemmes in resultats_existant[cle]['lemme']:
                        resultats_existant[cle]['lemme'][mots_intermediaires_lemmes] += 1
                    else:
                        resultats_existant[cle]['lemme'][mots_intermediaires_lemmes] = 1

                if mots_intermediaires_normaux.strip():
                    if mots_intermediaires_normaux in resultats_existant[cle]['normal']:
                        resultats_existant[cle]['normal'][mots_intermediaires_normaux] += 1
                    else:
                        resultats_existant[cle]['normal'][mots_intermediaires_normaux] = 1


def existe(term, mots):
    term_words = term.split()
    if not term_words:
        return -1
    term_length = len(term_words)
    
    for i in range(len(mots) - term_length + 1):
        if mots[i] == term_words[0]:
            match = True
            for j in range(1, term_length):
                if i + j >= len(mots) or mots[i + j] != term_words[j]:
                    match = False
                    break
            if match:
                return i
    return -1

def charger_r(fichier_template):
    resultats_existant = {}
    with open(fichier_template, 'r', encoding='utf-8') as f:
        for ligne in f:
            elements = ligne.strip().split(';')
            if len(elements) == 4:
                    mots = elements[0]
                    relation = elements[1]
                    type = elements[2]
                    count = int(elements[3])

                    if relation not in resultats_existant:
                        resultats_existant[relation] = {'lemme': {}, 'normal': {}}

                    resultats_existant[relation][type][mots] = count
    return resultats_existant

def mots_intermediaires(fichierJ, relations_filename, paires, resultats_existant):
    with open(fichierJ, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    nom_fichier_relations = relations_filename.split('/')[-1]
    for phrase in data:
        mots_lemmes_full = [mot['lemme'] for mot in phrase if '(' not in mot['lemme'] and ')' not in mot['lemme']]
        mots_normaux_full = [mot['nom'] for mot in phrase if '(' not in mot['nom'] and ')' not in mot['nom']]
        distance(mots_lemmes_full, mots_normaux_full, paires, resultats_existant, nom_fichier_relations)
        text_lemmes = ' '.join(mots_lemmes_full)
        text_normaux = ' '.join(mots_normaux_full)
        if text_lemmes.count(',') >= 2:
            first_comma_index = text_lemmes.find(',')
            second_comma_index = text_lemmes.find(',', first_comma_index + 1)
            
            part1_lemmes = text_lemmes[:first_comma_index]
            part2_lemmes = text_lemmes[second_comma_index + 1:]
            mots_lemmes = part1_lemmes.split() + part2_lemmes.split()
            
            first_comma_index = text_normaux.find(',')
            second_comma_index = text_normaux.find(',', first_comma_index + 1)
            
            part1_normaux = text_normaux[:first_comma_index]
            part2_normaux = text_normaux[second_comma_index + 1:]
            mots_normaux = part1_normaux.split() + part2_normaux.split()
            distance(mots_lemmes, mots_normaux, paires, resultats_existant, nom_fichier_relations)

    return resultats_existant


def enregistrer_resultats(resultats_existant, fichier_template):
    with open(fichier_template, 'w', encoding='utf-8') as f:
        for relation, types in resultats_existant.items():
            for type, words_counts in types.items():
                for words, count in words_counts.items():
                    f.write(f"{words};{relation};{type};{count}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py relations json_file")
        sys.exit(1)
    relations_filename = sys.argv[1]
    fichierJ = sys.argv[2]
    fichier_template = "newtemplate.txt"
    paires = charger_paires(relations_filename)
    resultats_existant = charger_r(fichier_template)
    resultats_mis_a_jour = mots_intermediaires(fichierJ, relations_filename, paires, resultats_existant)
    enregistrer_resultats(resultats_mis_a_jour, fichier_template)
    print("Traitement terminé.")
