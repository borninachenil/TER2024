import json
import sys
import os
import string
import re
import spacy
nlp = spacy.load("fr_core_news_sm")

def tete(words):
    doc = nlp(" ".join(words))
    for token in doc:
        if token.pos_ == 'NOUN' and token.dep_ in ('nsubj', 'obj', 'ROOT'):  
            return token.text
    return ""  

def lire_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def lire_template(filename):
    motifs = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) == 3:
                motifs.append((parts[0], parts[1], int(parts[2])))
    return motifs

def ponc(word):
    return all(char in string.punctuation for char in word)

def process_motif(joined_mots, motif_text, relation, type, phrase):
    subresultats = []
    pattern = r'\b{}\b'.format(re.escape(motif_text))
    for match in re.finditer(pattern, joined_mots):
        debut = match.start()
        fin = match.end()
        
        avant = joined_mots[:debut].split()
        apres = joined_mots[fin:].split()

        avantc = [mot for mot in avant[-5:] if not ponc(mot)]
        apresc = [mot for mot in apres[:5] if not ponc(mot)]
        
        mots_avant_head = tete(avantc)
        mots_apres_head = tete(apresc)
        
        if mots_avant_head and mots_apres_head:
            interm_words = joined_mots[debut:fin]
            subresultats.append((mots_avant_head, mots_apres_head, relation, type, interm_words))
    return subresultats

def mots_intermediaires(phrases, motifs):
    resultats = []
    for phrase in phrases:
        mots_noms = [mot["nom"] for mot in phrase if not ponc(mot["nom"])]
        mots_lemmes = [mot["lemme"] for mot in phrase if not ponc(mot["lemme"])]
        noms = " ".join(mots_noms)
        lemmes = " ".join(mots_lemmes)
        for motif_text, relation, _ in motifs:
            resultats += process_motif(noms, motif_text, relation, "nom", phrase)
            resultats += process_motif(lemmes, motif_text, relation, "lemme", phrase)
    return resultats

def ecrire_resultats(filename, resultats):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        for mots_avant, mots_apres, relation, type, interm_words in resultats:
            f.write(f"{mots_avant};{mots_apres};{relation};{type};{interm_words}\n")

if __name__ == "__main__":
    chemin_json = sys.argv[1]
    chemin_template = 'stiches.txt'
    phrases = lire_json(chemin_json)
    motifs = lire_template(chemin_template)
    resultats = mots_intermediaires(phrases, motifs)
    chemin_json = chemin_json.split('/')
    chemin_json = chemin_json[1].split('.')[0]
    chemin_sortie = f'resultats/resultats_{chemin_json}.txt'
    ecrire_resultats(chemin_sortie, resultats)
    print("Traitement terminé.")
