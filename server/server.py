import socket
import os
from _thread import *
import ast
from shutil import copyfile

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, address):
    global ThreadCount
    #connection.send(str.encode('Welcome to the Server'))

    # Recibir el ID del usuario
    user_id = connection.recv(2048).decode('utf-8')
    try:
        _ = int(user_id)
    except:
        connection.send(str.encode(f'invalid id: {user_id}'))
        connection.close()
        print(f'Disonnected from: {address}')
        ThreadCount -= 1
        print('Thread Number: ' + str(ThreadCount))
        return



    # Saludo del server
    print(f"Bienvenido Usuario {user_id}")
    connection.sendall(str.encode(f"usuario {user_id} conectado")) #da el saludo a los cliente

    #copiar carpetas y archivos de los clientes 
    dir_name = f"client_files/{user_id}_files"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    
    # Recibir los titulos de los archivos, y copiarlos de los directorios originales
    dir_info = connection.recv(2048).decode('utf-8').split("|") #informacion de carpeta y archivos del cliente
    #print(dir_info)
    client_files_dir = dir_info[0] #nombre carpeta del cleinte
    client_files_names = ast.literal_eval(dir_info[1]) #lista archivos de la carpeta del clinte
    for file_name in client_files_names:
        #print(f"{client_files_dir}{file_name}", f"{dir_name}/{file_name}")
        #copia del directorio original al destino
        copyfile(f"{client_files_dir}{file_name}", f"{dir_name}/{file_name}")
    

    while True:
        menu = """
        LISTA DE OPCIONES
        -----------------

        1. LISTAR ARCHIVO
        2. LEER ARCHIVO (MANDAR NOMBRE CON EXTENSIÓN, ID DEL CLIENTE, TODO
        SEPARADO POR COMMA (,))
        3. BORRAR ARCHIVO (MANDAR NOMBRE CON EXTENSIÓN, ID DEL CLIENTE, TODO
        SEPARADO POR COMMA (,))

        NOTA: SI PONES UNA OPCIÓN NO LISTADA, EL SERVIDOR EXPLOTARÁ'
        
        """
        connection.send(str.encode(menu))
        option = connection.recv(2048).decode('utf-8')

        if option[0] == "1":
            lista_Archivos = []
            for clienteId in range(1,4):
                dir_name = f"client_files"
                if os.path.isdir(f"{dir_name}/{clienteId}_files"):
                    client_file_list = os.listdir(f"{dir_name}/{clienteId}_files")
                    lista_Archivos.append(client_file_list)
                    
            #aqui podemos hacer un if para hacer que devuelva un string en caso de que no hayan archivos para mostrar
            connection.send(str.encode(str(lista_Archivos)))
        elif option[0] == "2":

            file_name = option.split(",")[1]
            cliente = option.split(",")[2]

            existe = False
            
            dir_name = f"client_files/{cliente}_files" 
            if os.path.isfile(f"{dir_name}/{file_name}"):
                existe = True
                connection.send(str.encode(open(f"{dir_name}/{file_name}","r").read()))
            if existe == False:
                connection.send(str.encode(f"error: archivo {file_name} no existe"))

                #-----------------------------------------------
        elif option[0] == "3":
            file_name = option.split(",")[1]
            cliente = option.split(",")[2]
            existe = False
            
            dir_name = f"client_files/{cliente}_files" 
            if os.path.isfile(f"{dir_name}/{file_name}"):
                existe = True
                #Elimina archivo
                os.remove(f"{dir_name}/{file_name}")
                client_file_list = os.listdir(dir_name)
                connection.send(str.encode(f"borrado : {file_name}"))
            if existe == False:
                connection.send(str.encode(f"error: archivo {file_name} no existe"))
        else:
            break

    connection.close()
    print(f'Disonnected from: {address}')
    ThreadCount -= 1
    print('Thread Number: ' + str(ThreadCount) + '\n')
    

while True:
    Client, address = ServerSocket.accept()
    address = address[0] + ':' + str(address[1])
    print(f'Connected to: {address}')
    start_new_thread(threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()