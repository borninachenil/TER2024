import json
import sys
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

def trouver_mots_intermediaires(phrases, motifs):
    resultats = []
    for phrase in phrases:
        mots = [mot["mot"] for mot in phrase]
        for motif, relation, _ in motifs:
            if motif in " ".join(mots):
                index_debut = " ".join(mots).find(motif)
                mots_avant = " ".join(mots)[:index_debut].split()[-1] if " ".join(mots)[:index_debut].split() else ""
                mots_apres = " ".join(mots)[index_debut+len(motif):].split()[0] if " ".join(mots)[index_debut+len(motif):].split() else ""
                if mots_apres != "" and mots_avant != "":
                    resultats.append((mots_avant, mots_apres, relation))
    return resultats

def ecrire_resultats(filename, resultats):
    with open(filename, 'w', encoding='utf-8') as f:
        for mots_avant, mots_apres, relation in resultats:
            f.write(f"{mots_avant};{mots_apres};{relation}\n")
if __name__ == "__main__":
    chemin_json = sys.argv[1]
    chemin_template = 'stiches.txt'
    phrases = lire_json(chemin_json)
    motifs = lire_template(chemin_template)
    resultats = trouver_mots_intermediaires(phrases, motifs)
    chemin_json = chemin_json.split('/')
    chemin_json = chemin_json[1].split('.')[0]
    chemin_sortie = f'resultats/resultats{chemin_json}.txt'
    ecrire_resultats(chemin_sortie, resultats)
