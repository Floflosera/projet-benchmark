import subprocess
import importlib

def installer_bibliotheque(nom_bibliotheque):
    try:
        importlib.import_module(nom_bibliotheque)
        print(f"{nom_bibliotheque} est déjà installé.")
    except ImportError:
        print(f"{nom_bibliotheque} n'est pas installé. Installation en cours...")
        subprocess.check_call(["pip3", "install", nom_bibliotheque])
        print(f"{nom_bibliotheque} a été installé avec succès.")

def sshImport():
    installer_bibliotheque("paramiko")
    installer_bibliotheque("scp")
    
def benchImport():
    installer_bibliotheque("psutil")
    installer_bibliotheque("time")
    installer_bibliotheque("socket")
    installer_bibliotheque("signal")