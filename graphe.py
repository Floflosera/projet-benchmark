import matplotlib.pyplot as plt

# Lecture des données à partir du fichier
with open('donnees.txt', 'r') as file:
    # Ignorer l'en-tête
    next(file)
    # Initialisation des listes pour stocker les données
    noms = []
    temps = []
    cpu = []
    memoire = []
    temp_cpu = []
    # Lire chaque ligne du fichier
    for line in file:
        # Séparer les valeurs en utilisant des tabulations comme délimiteurs
        data = line.split('\t')
        # Extraire les valeurs dans des variables appropriées
        nom = data[0]
        t = float(data[1])
        c = float(data[2])
        mem = float(data[3])
        temp_c = float(data[4])
        # Ajouter les valeurs aux listes correspondantes
        noms.append(nom)
        temps.append(t)
        cpu.append(c)
        memoire.append(mem)
        temp_cpu.append(temp_c)

# Créer les sous-graphiques
fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# Tracer les graphiques pour chaque catégorie
axs[0].bar(noms, temps, color='skyblue')
axs[0].set_title('Temps (s)')

axs[1].bar(noms, cpu, color='salmon')
axs[1].set_title('CPU (%)')

axs[2].bar(noms, memoire, color='lightgreen')
axs[2].set_title('Mémoire (%)')

axs[3].bar(noms, temp_cpu, color='gold')
axs[3].set_title('Température CPU (°C)')

# Ajuster les espacements entre les sous-graphiques
plt.tight_layout()

# Sauvegarder l'image en tant que fichier PNG sur le PC
plt.savefig('mon_image.png', format='png')

# Afficher les graphiques
plt.show()
