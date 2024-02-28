from importPip import benchImport
benchImport()

import psutil
import time
import subprocess
import sys
import socket
import signal
import os

# Fonction pour vérifier si un processus avec un chemin donné est en cours d'exécution
def is_process_running(process_path):
    for process in psutil.process_iter(['name', 'cmdline']):
        if process.info['cmdline'] and process.info['cmdline'][0] == 'python3' and process.info['cmdline'][1] == process_path:
            return True
    return False

def benchM(type_test):    
    # Chemin vers le fichier Python que vous souhaitez exécuter en parallèle
    chemin_fichier = type_test + "/" + type_test + "Test.py"
    
    # Lancer le fichier Python en parallèle
    process = subprocess.Popen(["python3", chemin_fichier])
    
    def clean_pgrm(signum, frame):
        process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, clean_pgrm)

    start_time = time.time()
    
    sommeStat = 0
    cpu_percent = 0
    memory_usage = 0
    temperatures = psutil.sensors_temperatures()
    tabTemperature = []
    
    cTemp = 0
    
    for sensor_name, entries in temperatures.items():
        for entry in entries:
            tabTemperature.append(0)
    
    # Tant que le processus est en cours d'exécution
    while is_process_running(chemin_fichier):
        sommeStat += 1
        cpu_percent += psutil.cpu_percent(interval=1)
        memory_usage += psutil.virtual_memory().percent
        temperatures = psutil.sensors_temperatures()
        
        cTemp = 0
        
        for sensor_name, entries in temperatures.items():
            # print("Capteur:", sensor_name)
            for entry in entries:
                # print("Température actuelle:", entry.current)
                tabTemperature[cTemp] += entry.current
                cTemp += 1
        
        # print(f"Utilisation CPU : {cpu_percent} %")
        # print(f"Mémoire utilisée : {memory_usage} %")
        
        time.sleep(1)  # Attendre une seconde avant la nouvelle vérification
    
    end_time = time.time()
    execution_time = round(end_time - start_time)
    # print(f"Temps d'exécution : {round(execution_time)} secondes")
    
    cpu_percent = round(cpu_percent / sommeStat,2)
    memory_usage = round(memory_usage / sommeStat,2)
    
    cTemp = 0
    for sensor_name, entries in temperatures.items():
        for entry in entries:
            tabTemperature[cTemp] = round(tabTemperature[cTemp] / sommeStat,2)
            cTemp += 1
    
    cTemp = 0
    
    print("Le processus est terminé.")
    
    with open("donner_"+type_test+".txt", 'w', encoding="UTF-8") as file:
        file.write(f"{socket.gethostname()}\t")
        file.write(f"{execution_time}\t")
        file.write(f"{cpu_percent}\t")
        file.write(f"{memory_usage}")
        for sensor_name, entries in temperatures.items():
            for entry in entries:
                file.write("\t" + str(tabTemperature[cTemp]))
                cTemp += 1

if __name__ == "__main__":
    chemin_base = "benchmark_ml_dl/"
    os.chdir(chemin_base)
    benchM(sys.argv[1])