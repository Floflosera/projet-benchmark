import socket
import subprocess
import locale
import os
import platform

system_type = platform.system()

def get_hostname_from_ip(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return "?"

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

for fichier in fichiers_donner:
    chemin_fichier = os.path.join(dossier, fichier)
    os.remove(chemin_fichier)

if os.path.exists("document.txt"):
    os.remove("document.txt")

# Obtenez l'encodage par défaut du système de la console
encodage_console = locale.getpreferredencoding()

# Exécuter la commande arp -a et capturer la sortie
resultat = subprocess.run("arp -a", shell=True, capture_output=True, text=True)

# Écrire la sortie dans un fichier texte en utilisant l'encodage de la console
with open("resultat_arp.txt", "w", encoding=encodage_console) as fichier_sortie:
    fichier_sortie.write(resultat.stdout)

arpOui = str(resultat.stdout)

sortieOui = ""

if(system_type == "Windows"):
    while arpOui.find("192.168.") != -1:

        arpOui = arpOui[arpOui.find("Interface")+1:]

        arpOui = arpOui[arpOui.find("192.168.")+8:]

        ipPing = arpOui[:arpOui.find(".")]

        # print(str(ipPing))

        with open(os.devnull, 'w') as DEVNULL:
            for i in range(1, 254):
                subprocess.Popen('ping -n 1 192.168.' + ipPing + '.' + str(i), shell=True, stdout=DEVNULL, stderr=DEVNULL)
            process = subprocess.Popen('ping -n 1 192.168.' + ipPing + '.254', shell=True, stdout=DEVNULL, stderr=DEVNULL)

        process.wait()

        arpOui = arpOui[arpOui.find("192.168.")+1:]

    # Commande arp et capture de la sortie
    resultat = subprocess.run("arp -a", shell=True, capture_output=True, text=True)

    # Écrire la sortie dans un fichier texte en utilisant l'encodage de la console
    with open("resultat_arp.txt", "w", encoding=encodage_console) as fichier_sortie:
        fichier_sortie.write(resultat.stdout)

    # print(resultat.stdout)

    arpOui = str(resultat.stdout)

    while(arpOui.find("dynamique") != -1):

        arpOui = arpOui[arpOui.find("Interface"):]
        ipVerif = arpOui[arpOui.find(" ")+1:arpOui.find(".")+1]
        arpOui = arpOui[arpOui.find(".")+1:]
        ipVerif += arpOui[:arpOui.find(".")+1]
        # print(ipVerif)

        arpTemp = arpOui[:arpOui.find("Interface")]

        while(arpTemp.find("dynamique") != -1):
            arpTemp = arpTemp[arpTemp.find(ipVerif):]
            if(arpTemp.find("dynamique") < 90 and arpTemp.find("dynamique") != -1):
                arpTemp = arpTemp[arpTemp.find(ipVerif):]

                ipOui = arpTemp[:arpTemp.find(" ")]

                # print(ipOui)

                nomHost = get_hostname_from_ip(ipOui)

                # '''print(nomHost)'''

                sortieOui += nomHost + "/" + ipOui + "\n"

            arpTemp = arpTemp[arpTemp.find(ipVerif)+1:]

        arpOui = arpOui[arpOui.find("Interface"):]

elif(system_type == "Linux"):
    # Commande arp et capture de la sortie
    resultat = subprocess.run("arp -a", shell=True, capture_output=True, text=True)

    arpOui = str(resultat.stdout)

    while(arpOui.find(".") != -1):
        nomHost = arpOui[:arpOui.find(" ")]

        # print(nomHost)

        arpOui = arpOui[arpOui.find(" ")+2:]

        ipOui = arpOui[:arpOui.find(")")]

        # print(ipOui)

        sortieOui += nomHost + "/" + ipOui + "\n"

        if(arpOui.find("\n") != -1):
            arpOui = arpOui[arpOui.find("\n")+1:]
        else:
            break

else:
    print("Ce système d'exploitation n'a pas été prévu pour la recherche d'IP.")

with open("tree.txt", 'w', encoding='utf-8') as trucOui:
    trucOui.write(sortieOui[:-1])