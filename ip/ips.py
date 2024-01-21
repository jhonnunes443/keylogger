import socket
import requests

ip_local = socket.gethostbyname(socket.gethostname())
print(f'IP Local: {ip_local}')

ip_publico = requests.get('https://api.ipify.org/').text
print(f'IP Publico: {ip_publico}')

