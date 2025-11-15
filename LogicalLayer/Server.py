from urllib.parse import parse_qs
from DB_Connect import DB_Connect
from Hash_function import Hash
from threading import Thread
import socket


class Server:
    def __init__(self, host, port):
        self.db = DB_Connect()
        self.hash = Hash()
        self.port = port
        self.host = host

    def making_path(self, relative_path):
        import os.path
        import sys

        return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), relative_path)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            request = client_socket.recv(1024).decode('utf-8')
            print(f"Request:\n{request}")

            response = self.handle_request(request)
            client_socket.send(response.encode())

            client_socket.close()

            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr}")
            thread = Thread(target=self.handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request from {addr}:\n{request}")

        response = self.handle_request(request)
        client_socket.send(response.encode())
        client_socket.close()

    def handle_request(self, request):
        # Разбиваем на строки
        lines = request.splitlines()
        if not lines:
            return "HTTP/1.1 400 Bad Request\r\n\r\n"

        request_line = lines[0]
        method, path, version = request_line.split()

        if method == "GET":
            if path == "/link-shortener":
                try:
                    with open(self.making_path("../FrontEnd/index.html"), "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    response_body = content
                except FileNotFoundError:
                    return "HTTP/1.1 404 Not Found\r\n\r\nFile not found"
            else:
                response_body = "Упс страница не найдена"
            response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""


        elif method == "POST":
            if path == "/add_id":
                # Найдем тело запроса
                body_start = request.find("\r\n\r\n") + 4
                body = request[body_start:]

                # Пример: обработка form-data
                data = parse_qs(body)
                id = data.get("id", [""])[0]

                self.db.add_user(int(id), "anonymous")
                with open(self.making_path("../FrontEnd/index.html"), "r", encoding="utf-8") as f:
                    content = f.read()
                    
                response_body = content
                return f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""
            
            elif path == "/url":
                pass
            
            else:
                return "HTTP/1.1 404 Not Found\r\n\r\n"

        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

        return response