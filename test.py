import sys

def main():
    # Récupérer les informations transmises en tant qu'arguments
    ip = sys.argv[1]
    nom_utilisateur = sys.argv[2]
    mot_de_passe = sys.argv[3]
    ia = sys.argv[4]

    # Écrire les informations dans un fichier "document.txt"
    with open('document.txt', 'a' , encoding='utf-8') as f:
        f.write(f'{ip}\t{nom_utilisateur}\t{mot_de_passe}\t{ia}\n')

    # Confirmer l'enregistrement des données
    print("Informations enregistrées dans le fichier document.txt")

if __name__ == "__main__":
    main()
