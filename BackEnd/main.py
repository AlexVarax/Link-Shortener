# Точка входа для запуска HTTP-сервера сокращения URL

from Server import Server

server = Server('localhost', 8080)
server.start()