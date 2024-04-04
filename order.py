def lire_et_trier_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lignes = [ligne.strip().split(';') for ligne in f if ligne.strip()]

    lignes_triees = sorted(lignes, key=lambda x: int(x[2]), reverse=True)
    return lignes_triees
def ecrire_resultats_tries(filename, lignes_triees):
    with open(filename, 'w', encoding='utf-8') as f:
        for ligne in lignes_triees:
            f.write(';'.join(ligne) + '\n')
if __name__ == "__main__":
    chemin_template = 'templateold.txt'
    chemin_sortie = 'templateold_tries.txt'
    lignes_triees = lire_et_trier_template(chemin_template)
    ecrire_resultats_tries(chemin_sortie, lignes_triees)
    
    print("Fichier trié écrit dans:", chemin_sortie)
