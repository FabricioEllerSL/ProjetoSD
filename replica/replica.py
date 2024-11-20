import socket
import os

def start_server(port, directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Servidor ouvindo na porta {port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexão recebida de {addr}")

            # Receber nome do arquivo e posição inicial
            request = client_socket.recv(1024).decode()
            filename, start_pos = request.split("::")
            start_pos = int(start_pos)

            filepath = os.path.join(directory, filename)

            if os.path.exists(filepath):
                client_socket.send(b"OK")
                with open(filepath, "rb") as f:
                    f.seek(start_pos)  # Ir para a posição inicial solicitada
                    while chunk := f.read(1024):
                        client_socket.send(chunk)
            else:
                client_socket.send(b"NOT_FOUND")

            client_socket.close()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    finally:
        server_socket.close()

start_server(8081, "servidor")
