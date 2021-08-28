import socket
import os
import os.path
import shutil

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
user_id = "2"


# Establece conexión con el servidor
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# Mandar el ID del usuario
ClientSocket.send(str.encode(user_id))
Response = ClientSocket.recv(1024).decode('utf-8')
print(Response)
if "invalid" in Response:
    ClientSocket.close()
else:
    # Mandar la información de los archivos
    arr = os.listdir("files")
    data = f"../client_{user_id}/files/|{arr}"
    ClientSocket.send(str.encode(data.replace(" ","")))
    # Ejecución del cliente
    while True:
        # RECIBIR EL MENU DE OPCIONES
        menu = ClientSocket.recv(1024).decode('utf-8')
        print(menu)
        option = input("INGRESA LA OPCIÓN: ")
        ClientSocket.send(str.encode(option))
        Response = ClientSocket.recv(1024).decode('utf-8')
        print(f"\nSERVIDOR DICE: {Response}")

    ClientSocket.close()