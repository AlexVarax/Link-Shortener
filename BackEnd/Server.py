from urllib.parse import parse_qs
from DB_Connect import DB_Connect
from Hash_function import Hash
from threading import Thread
import socket
import json
import os


class Server:
    def __init__(self, host, port):
        self.db = DB_Connect()
        self.hash = Hash()
        self.port = port
        self.host = host
        self.work = True

    def making_path(self, relative_path):
        import sys
        return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), relative_path)

    def get_content_type(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
        }
        return types.get(ext, 'application/octet-stream')

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}")

        while self.work:
            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr}")
            thread = Thread(target=self.handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()

    def handle_client(self, client_socket, addr):
        try:
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            print(f"Request from {addr}:\n{request[:500]}...")

            response = self.handle_request(request)

            if isinstance(response, bytes):
                client_socket.send(response)
            else:
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            client_socket.close()

    def handle_request(self, request):
        lines = request.splitlines()
        if not lines:
            return "HTTP/1.1 400 Bad Request\r\n\r\n"

        request_line = lines[0]
        method, path, version = request_line.split()

        if method == "GET":
            print(f"\n\n\n\n{path[1:]}\n\n\n\n\n")

            if path == "/link-shortener":
                try:
                    with open(self.making_path("../FrontEnd/index.html"), "r", encoding="utf-8") as f:
                        content = f.read()
                    response_body = content
                    return f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""
                except FileNotFoundError:
                    return f"{version} 404 Not Found\r\n\r\nFile not found"
                
            elif self.db.get_full_url(path[1:]) != None:
                full_url = self.db.get_full_url(path[1:])
                print(f"{'-'*20} {full_url}")
                
                return f"""{version} 302 Found\r\nLocation: {full_url}\r\n\r\n"""
            else:
                filepath = path[1:]
                full_path = self.making_path(f"../FrontEnd/{filepath}")
                if os.path.exists(full_path):
                    content_type = self.get_content_type(full_path)
                    if content_type.startswith("image/"):
                        with open(full_path, "rb") as f:
                            content = f.read()
                        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content
                    else:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        return f"""HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}"""
                else:
                    
                    return "HTTP/1.1 404 Not Found\r\n\r\nFile not found"

        elif method == "POST":
            # Найти заголовки и тело
            headers_end = request.find("\r\n\r\n")
            headers = request[:headers_end]
            body = request[headers_end + 4:]

            # Проверить Content-Type
            if "Content-Type: application/json" in headers:
                try:
                    data = json.loads(body)
                    print("\n\n\n DATA = ", data, type(data), " \n\n")

                    user_id = int(data['id'])
                    original_url = data['url']
                    short_key = self.hash.hash(user_id, original_url)

                    response_data = {
                        "short_key": short_key
                    }
                    response_body = json.dumps(response_data)

                    self.db.add_short_url(user_id, original_url, short_key)

                    return f"""HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""
                except json.JSONDecodeError:
                    return "HTTP/1.1 400 Bad Request\r\n\r\nInvalid JSON"
            else:
                return "HTTP/1.1 400 Bad Request\r\n\r\nContent-Type must be application/json"

        else:
            return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"