import socket
import os

def download_file(server_ip, port, filename, local_path):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        client_socket.send(filename.encode())

        response = client_socket.recv(1024)
        if response == b"OK":
            with open(local_path, "ab") as f:
                while chunk := client_socket.recv(1024):
                    f.write(chunk)
            print("Download concluído!")
        else:
            print("Arquivo não encontrado no servidor.")
    except (socket.error, KeyboardInterrupt):
        print("Conexão perdida!")
        raise
    finally:
        client_socket.close()

try:
    print("Baixando do Servidor Principal...")
    download_file("127.0.0.1", 8080, "arquivo.txt", "arquivo.txt")
except:
    print("Tentando o servidor réplica...")
    download_file("127.0.0.1", 8081, "arquivo.txt", "arquivo.txt")
