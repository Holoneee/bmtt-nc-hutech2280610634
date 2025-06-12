import socket
import ssl
import threading

server_address = ('localhost', 12345)

clients = []  # Đổi thành 'clients' để thống nhất tên biến

def handle_client(client_socket):
    clients.append(client_socket)
    print("Đã kết nối với:", client_socket.getpeername())
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))

            # Gửi data cho các client khác
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        clients.remove(client)
    except Exception as e:
        print("Lỗi xử lý client:", e)
    finally:
        print("Đã ngắt kết nối:", client_socket.getpeername())
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Tạo SSL context 1 lần, bên ngoài vòng lặp
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./certificates/server-cert.crt", keyfile="./certificates/server-key.key")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server đang chờ kết nối...")

while True:
    client_socket, client_address = server_socket.accept()
    # Wrap socket với SSL
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    # Tạo thread xử lý client
    client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
    client_thread.start()
