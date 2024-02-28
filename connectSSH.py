import os
import sys
from importPip import sshImport
sshImport()
import paramiko
from scp import SCPClient
import subprocess
import locale
import threading

def create_directory_if_not_exists(ssh, directory_path):
    # Exécuter la commande pour vérifier si le répertoire existe
    _, stdout, stderr = ssh.exec_command(f'test -d "{directory_path}" && echo "Exists" || echo "Not exists"')

    # Lire la sortie de la commande
    output = stdout.read().decode('utf-8')

    # Si le répertoire n'existe pas, le créer
    if "Not exists" in output:
        ssh.exec_command(f'mkdir -p "{directory_path}"')
        print(f"Le répertoire '{directory_path}' a été créé avec succès.")
    else:
        print(f"Le répertoire '{directory_path}' existe déjà.")

def connect_ssh(hostname,username,password,type_ia):

    port = 22

    # Création d'un objet SSHClient
    ssh_client = paramiko.SSHClient()

    # Ignorer la vérification des clés SSH
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connexion au serveur SSH
        # ssh_client.connect(hostname, port, username, password)
        ssh_client.connect(hostname, username=username, password=password)
        # ssh_client.connect('169.254.67.101', 'pi', 'raspberry')
        
        create_directory_if_not_exists(ssh_client,"benchmark_ml_dl")
        
        # ssh_client.exec_command('cd benchmark_ml_dl')

        # Création d'un objet SCPClient
        with SCPClient(ssh_client.get_transport()) as scp:

            # Copie du fichier local vers le serveur distant
            local_file = "benchmark.py"
            remote_path = "benchmark_ml_dl/"
            scp.put(local_file, remote_path)
            
            local_file = "importPip.py"
            scp.put(local_file, remote_path)
            
            # Chemin local du dossier à copier
            local_folder = type_ia
            # Chemin distant où le dossier sera copié
            remote_folder = "benchmark_ml_dl/"
            # Copie récursive du dossier et de ses sous-dossiers
            scp.put(local_folder, recursive=True, remote_path=remote_folder)

        stdin, stdout, stderr = ssh_client.exec_command(f'python3 benchmark_ml_dl/benchmark.py {type_ia}')
        # print(stdout.read().decode())
        stdout.read().decode() #pour attendre la fin

        #stdin, stdout, stderr = ssh_client.exec_command('python3 '+ desktop_path+"oui/oui.py")
        # print(stdout.read().decode())
        # print(stderr.read().decode())

        with SCPClient(ssh_client.get_transport()) as scp:
            #Copie du fichier du serveur distant vers la machine locale
            remote_file = os.path.join("benchmark_ml_dl/", 'donner_'+type_ia+'.txt')
            local_path = './'
            scp.get(remote_file, local_path)


    finally:
        # Fermeture de la connexion SSH
        ssh_client.close()
    
    try:
        os.rename('donner_'+type_ia+'.txt', 'donner_' + hostname + '_' + type_ia + '.txt')
        # print("Le fichier a été renommé avec succès.")
    except FileNotFoundError:
        print("Le fichier n'existe pas.")
    except FileExistsError:
        print("Un fichier avec le nouveau nom existe déjà.")
    except Exception as e:
        print("Une erreur s'est produite :", e)

def ssh_thread(hostname, username, password, type_ia):
    connect_ssh(hostname, username, password, type_ia)

encodage_console = locale.getpreferredencoding()

with open("document.txt", "r", encoding=encodage_console) as docu:
    docuOui = docu.read()

threads = []

while(docuOui.find("\n") != -1):
    hostname = docuOui[:docuOui.find("\t")]
    docuOui = docuOui[docuOui.find("\t")+1:]
    username = docuOui[:docuOui.find("\t")]
    docuOui = docuOui[docuOui.find("\t")+1:]
    password = docuOui[:docuOui.find("\t")]
    docuOui = docuOui[docuOui.find("\t")+1:]
    type_ia = docuOui[:docuOui.find("\n")]
    type_ia = type_ia.lower()
    docuOui = docuOui[docuOui.find("\n")+1:]

    # Thread pour chaque connexion SSH
    thread = threading.Thread(target=ssh_thread, args=(hostname, username, password, type_ia))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

subprocess.run("python3 fuuusion_ya.py", shell=True, capture_output=True, text=True)

print("Fin de l'exécution.")