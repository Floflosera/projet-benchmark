import os
import locale

encodage_console = locale.getpreferredencoding()

donnees = "nom\ttemps (s)\tcpu (%)\tmemoire (%)\ttemperature cpu (degre C)\ttemperature gpu (degre C)"

# Spécifiez le chemin du dossier
dossier = './'

# Liste pour stocker les noms des fichiers commençant par "donner"
fichiers_donner = []

# Lire tous les fichiers du dossier
fichiers_dossier = os.listdir(dossier)

# Filtrer les fichiers commençant par "donner"
for fichier in fichiers_dossier:
    if fichier.startswith('donner'):
        fichiers_donner.append(fichier)

with open("donnees.txt", "w", encoding=encodage_console) as fichier_sortie:
    fichier_sortie.write(donnees)
    for fichier in fichiers_donner:
        chemin_fichier = os.path.join(dossier, fichier)
        with open(chemin_fichier, 'r') as f:
            contenu = f.read()
            fichier_sortie.write("\n"+contenu)

