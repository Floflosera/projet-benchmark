import http.server
import socketserver
import subprocess
import json

PORT = 8000  # Vous pouvez changer le port si nécessaire

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        mime_type = super().guess_type(path)
        if mime_type == 'text/plain':
            return 'application/octet-stream'
        else:
            return mime_type

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        if self.path == "/run_python":
            self.handle_run_python(post_data)
        elif self.path == "/valider":
            self.handle_valider(post_data)
        elif self.path == "/run_connectSSH":
            self.handle_SSH(post_data)
        elif self.path == "/run_graphe":
            self.handle_run_graphe()
        else:
            self.send_error(404)

    def handle_run_graphe(self):
        result = subprocess.run(["python3", "graphe.py"], capture_output=True, text=True)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"output": result.stdout}).encode('utf-8'))

    def handle_run_python(self, post_data):
        result = subprocess.run(["python3", "listIp.py"], capture_output=True, text=True)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"output": result.stdout}).encode('utf-8'))

    def handle_valider(self, post_data):
        donnees = json.loads(post_data)
        ip = donnees['ip']
        nom_utilisateur = donnees['nomUtilisateur']
        mot_de_passe = donnees['motDePasse']
        ia = donnees['ia']

        # Lancer le script test.py avec les informations comme arguments
        subprocess.run(["python3", "test.py", ip[:-1], nom_utilisateur, mot_de_passe, ia])

        self.send_response(200)
        self.end_headers()
        self.wfile.write("Données reçues et enregistrées avec succès!".encode('utf-8'))

    def handle_SSH(self, post_data):
        result = subprocess.run(["python3", "connectSSH.py"], capture_output=True, text=True)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"output": result.stdout}).encode('utf-8'))


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serveur HTTP démarré sur le port", PORT)
    httpd.serve_forever()
