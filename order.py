import sys

def lire_fichier_entree(chemin):
    termes = []
    with open(chemin, 'r', encoding='Windows-1254', errors='ignore') as fichier:
        for ligne in fichier:
            elements = ligne.strip().split(';')
            if len(elements) >= 2:  # Ensure there are at least two elements (ID and term)
                id_terme = elements[0]
                # Join elements after the first, removing a trailing quote if present
                terme = ';'.join(elements[1:]).rstrip('"')
                termes.append((id_terme, terme))
            else:
                print(f"Ignoring invalid line: {ligne}")
    return termes

def trier_termes_par_nombre_de_mots(termes):
    # Sort terms by the number of words in the term, from largest to smallest
    return sorted(termes, key=lambda x: len(x[1].split()), reverse=True)

def ecrire_fichier_sortie(chemin, termes_tries):
    with open(chemin, 'w', encoding='Windows-1254') as fichier:
        for terme in termes_tries:
            # Write only terms composed of a single word
            if len(terme[1].split()) == 1:
                fichier.write(f"{terme[0]};{terme[1]}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)

    chemin_entree = sys.argv[1]
    chemin_sortie = sys.argv[2]

    termes = lire_fichier_entree(chemin_entree)
    termes_tries = trier_termes_par_nombre_de_mots(termes)
    ecrire_fichier_sortie(chemin_sortie, termes_tries)

    print("Completed! The output file has been successfully created.")
