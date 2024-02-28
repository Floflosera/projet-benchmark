import subprocess
import importlib

def installer_bibliotheque(nom_bibliotheque):
    try:
        importlib.import_module(nom_bibliotheque)
        print(f"{nom_bibliotheque} est déjà installé.")
    except ImportError:
        print(f"{nom_bibliotheque} n'est pas installé. Installation en cours...")
        if(nom_bibliotheque == "skimage"):
            nom_bibliotheque = "scikit-image"
        subprocess.check_call(["pip3", "install", nom_bibliotheque])
        print(f"{nom_bibliotheque} a été installé avec succès.")

def visionImport():
    installer_bibliotheque("psutil")
    installer_bibliotheque("pickle")
    installer_bibliotheque("skimage")
    installer_bibliotheque("numpy")

#skimage -> scikit-image
#sklearn -> scikit-learn