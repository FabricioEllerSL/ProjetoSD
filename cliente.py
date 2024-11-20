import socket
import os

def download_file(server_ip, port, filename, local_path):
    try:
        # Verificar progresso existente
        start_pos = os.path.getsize(local_path) if os.path.exists(local_path) else 0
        print(f"[INFO] Iniciando download do arquivo '{filename}' a partir do byte {start_pos}.")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        
        # Enviar nome do arquivo e posição inicial
        client_socket.send(f"{filename}::{start_pos}".encode())

        response = client_socket.recv(1024)
        if response == b"OK":
            with open(local_path, "r+b" if os.path.exists(local_path) else "wb") as f:
                f.seek(start_pos)  # Garante que escrevemos a partir do ponto correto
                while chunk := client_socket.recv(1024):
                    f.write(chunk)
                    start_pos += len(chunk)  # Atualiza a posição do byte recebido
        else:
            print("[ERRO] Arquivo não encontrado no servidor.")

        print("[INFO] Download concluído com sucesso.")
    except (socket.error, KeyboardInterrupt):
        print(f"[ALERTA] Download interrompido no byte {start_pos}.")
        raise  # Lança o erro para permitir a tentativa no servidor réplica
    finally:
        client_socket.close()

# Tentativa de download
try:
    download_file("127.0.0.1", 8080, "arquivo.txt", "arquivo_baixado.txt")
except:
    print("[INFO] Tentando continuar o download com o servidor réplica...")
    download_file("127.0.0.1", 8081, "arquivo.txt", "arquivo_baixado.txt")
