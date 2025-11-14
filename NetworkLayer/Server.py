import socket

def handle_request(request):
    # Разбиваем на строки
    lines = request.splitlines()
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    # Первая строка: метод, путь, версия
    request_line = lines[0]
    method, path, version = request_line.split()

    if method == "GET":
        if path == "/index":
            try:
                with open("C:\program_alex_v\Pet_Projects\Link-Shortener\FrontEnd\index.html", "r", encoding="utf-8") as f:
                    content = f.read()
                response_body = content
                response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found 22"
        elif path == "/hello":
            response_body = f"Hello, world!"
            response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""
        elif path == "/style.css":
            with open("C:\program_alex_v\Pet_Projects\Link-Shortener\FrontEnd\style.css", "r", encoding="utf-8") as f:
                content = f.read()
            response_body = content
            response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""


    elif method == "POST":
        if path == "/echo":
            # Тело запроса после пустой строки
            body_start = request.find("\r\n\r\n") + 4
            body = request[body_start:]
            response_body = f"Received: {body}"
        else:
            response_body = "Not Found1"
        response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"""

    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

    return response

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request:\n{request}")

        response = handle_request(request)
        client_socket.send(response.encode())

        client_socket.close()

if __name__ == "__main__":
    start_server('localhost', 80)