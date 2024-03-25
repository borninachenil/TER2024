import subprocess
import time
pages_medicales = [
    "Tableau périodique des éléments", "Liaison chimique", "Réaction d'oxydo-réduction",
    "Chimie organique", "Chimie inorganique", "Spectroscopie RMN", "Chromatographie",
    "Cristallographie", "Polymères et plastiques", "Cinétique chimique", "Thermodynamique chimique",
    "Électrochimie", "Chimie verte", "Catalyse", "Synthèse organique", "Chimie analytique",
    "Acides et bases", "Chimie des colloïdes", "Mécanismes réactionnels", "Chimie supramoléculaire",
    "Chimie de coordination", "Photocatalyse", "Chimie des matériaux", "Nanochimie",
    "Biochimie", "Chimie médicinale", "Chimie théorique", "Dynamique moléculaire",
    "Chimie environnementale", "Chimie des polymères", "Métallurgie", "Chimie quantique",
    "Résonance magnétique nucléaire", "Spectrométrie de masse", "Rayons X et diffraction",
    "Chimie des surfaces", "Chimie des peptides", "Toxicologie chimique", "Chimie alimentaire",
    "Chimie des cosmétiques", "Pétrochimie", "Gaz nobles et leur chimie", "Alchimie à la chimie moderne",
    "Histoire de la chimie", "Prix Nobel de chimie", "Sécurité en laboratoire chimique",
    "Règles de nomenclature", "Molécules d'importance historique", "Chimie atmosphérique",
    "Acides nucléiques", "Photosynthèse", "Chimie des colorants", "Énergie et chimie",
    "Chimie pharmaceutique", "Procédés chimiques industriels", "Recyclage chimique",
    "Synthèse de médicaments", "Chimie des solides", "Solutions et solvants", "Réactions en chaîne",
    "Propriétés des gaz", "Équilibre chimique", "Extraction et purification", "Corrosion et protection des matériaux",
    "Combustion et flammes", "Explosifs et pyrotechnie", "Détecteurs chimiques",
    "Chimie des terres rares", "Énergie des réactions chimiques", "Chimie du quotidien",
    "Molécules dans l'espace", "Transition énergétique et chimie", "Éthique en chimie",
    "Simulation en chimie", "Chimie et art", "Chimie nucléaire", "Dégradation des polymères",
    "Chimie et technologie alimentaire", "Antibiotiques : découverte et mécanismes",
    "Vitamines et chimie", "Métalloprotéines", "Élaboration de nouveaux matériaux",
    "Chimie et changement climatique", "Pigments et teintures", "Isomérie",
    "Réactions pericycliques", "Solubilité et précipitation", "Acidification des océans",
    "Nouveaux carburants", "Chimie de l'eau", "Matériaux pour l'électronique",
    "Chimie des énergies renouvelables", "Cycles biogéochimiques", "Composés hétérocycliques",
    "Principe de Le Châtelier", "Tests chimiques qualitatifs", "Chimie du carbone",
    "Optique non linéaire", "Matériaux poreux", "Chimie des interfaces", "Molécules chirales",
    "Membranes synthétiques", "Hydrates de gaz", "Chimie des nanostructures", "Filtration moléculaire",
]

for page in pages_medicales:
    subprocess.run(["python", "wikipedia.py", page])
    time.sleep(1)