import os
import socket
localIP = socket.gethostbyname(socket.gethostname())

os.system(f'python manage.py runserver {localIP}:9191')