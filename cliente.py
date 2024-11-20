import socket
import os

def download_file(server_ip, port, filename, local_path):
    try:

        start_pos = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        print(f"[INFO] Iniciando download do arquivo '{filename}' a partir do byte {start_pos}.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        

        client_socket.send(f"{filename}::{start_pos}".encode())

        response = client_socket.recv(1024)
        
        if response == b"OK":
            with open(local_path, "r+b" if os.path.exists(local_path) else "wb") as f:
                f.seek(start_pos)
                while chunk := client_socket.recv(1024):
                    f.write(chunk)
                    start_pos += len(chunk)
        else:
            print("[ERRO] Arquivo não encontrado no servidor.")

        print("[INFO] Download concluído com sucesso.")
    except (socket.error, KeyboardInterrupt):
        print(f"[ALERTA] Download interrompido no byte {start_pos}.")
        raise
    finally:
        client_socket.close()


try:
    print('[INFO] Baixando do Server Principal')
    download_file("192.168.1.158", 8080, "arquivo.txt", "arquivo_baixado.txt")
except:
    print("[INFO] Tentando continuar o download com o servidor réplica...")
    download_file("192.168.1.162", 8081, "arquivo.txt", "arquivo_baixado.txt")
