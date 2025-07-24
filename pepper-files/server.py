#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os
import urlparse

"""
Servidor HTTP simple para ejecutar un script de Python en el robot Pepper haciendo una petición GET a un endpoint específico.
Este servidor se usa para poder ejecutar el script de python que se encarga de la interaccion con el servidor de IA desde la pagina web.

La ruta a este archivo debe introducirse en el archivo '/home/nao/naoqi/preferences/autoload.ini' para que se ejecute automáticamente al iniciar el robot Pepper.
"""

SCRIPT_PATH = "/home/nao/pepper-chatbot/ai_pepper_script.py"  # Ruta a tu script

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Manejo de preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # Manejo de las peticiones GET
    # El endpoint es http://localhost:8080/run-script al que, como parametro opcional, se le puede pasar el provider de la IA 
    # por ejemplo: http://localhost:8080/run-script?provider=gemini
    def do_GET(self):
        # Parseamos la URL para separar path y query string
        parsed = urlparse.urlparse(self.path)
        path = parsed.path
        query = parsed.query
        params = urlparse.parse_qs(query)
        print("Path:", path)
        print("Query string:", query)
        if 'provider' in params:
            print("Params (provider):", params['provider'])
        else:
            print("Params: 'provider' no especificado")

        if path == '/run-script':
            # Ejecutamos el script externo y capturamos su salida
            try:
                command = ['python', SCRIPT_PATH, '--serverIP', '172.18.33.110', '--serverPort', '5000']

                if 'provider' in params:
                    command.append('--provider')
                    command.append(params['provider'][0])

                print(command)

                # Llama al intérprete python2.7 para ejecutar el script
                output = subprocess.check_output(
                    command,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(SCRIPT_PATH)
                )
                status_code = 200
                body = output
                content_type = 'text/plain'
            except subprocess.CalledProcessError as e:
                status_code = 500
                body = "Error ejecutando el script:\n" + e.output
                content_type = 'text/plain'

            # Enviamos la respuesta HTTP
            self.send_response(status_code)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            # Si la ruta no coincide, devolvemos 404
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found: {}".format(path))

if __name__ == '__main__':
    port = 8080
    httpd = HTTPServer(('0.0.0.0', port), RequestHandler)
    print("Servidor escuchando en http://localhost:{}".format(port))
    httpd.serve_forever()