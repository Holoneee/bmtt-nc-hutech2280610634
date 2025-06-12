import socket
import ssl
import threading

server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))  # Sửa decode đúng
    except Exception as e:
        print("Lỗi khi nhận dữ liệu:", e)
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

# Tạo socket TCP bình thường
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSLContext cho client, chuẩn nhất là tạo context mặc định
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
# Nếu server dùng cert tự ký, bạn có thể tạm thời bỏ qua kiểm tra cert (không an toàn trong production)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Bọc socket TCP bằng SSL socket
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

try:
    ssl_socket.connect(server_address)
except Exception as e:
    print("Lỗi khi kết nối:", e)
    ssl_socket.close()
    exit(1)

# Thread nhận dữ liệu từ server
receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
receive_thread.start()

try:
    while True:
        message = input("Nhập tin nhắn: ")
        if message.lower() == 'exit':
            break
        ssl_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\nNgắt kết nối bằng bàn phím.")
except Exception as e:
    print("Lỗi khi gửi dữ liệu:", e)
finally:
    ssl_socket.close()
    receive_thread.join()
    print("Client đã đóng kết nối.")
