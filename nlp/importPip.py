import subprocess
import importlib

def installer_bibliotheque(nom_bibliotheque):
    try:
        importlib.import_module(nom_bibliotheque)
        print(f"{nom_bibliotheque} est déjà installé.")
    except ImportError:
        print(f"{nom_bibliotheque} n'est pas installé. Installation en cours...")
        if(nom_bibliotheque == "sklearn"):
            nom_bibliotheque = "scikit-learn"
        subprocess.check_call(["pip3", "install", nom_bibliotheque])
        print(f"{nom_bibliotheque} a été installé avec succès.")

def nlpImport():
    installer_bibliotheque("psutil")
    installer_bibliotheque("pandas")
    installer_bibliotheque("numpy")
    installer_bibliotheque("seaborn")
    installer_bibliotheque("matplotlib")
    installer_bibliotheque("nltk")
    installer_bibliotheque("sklearn")
    installer_bibliotheque("gensim")

#skimage -> scikit-image
#sklearn -> scikit-learn