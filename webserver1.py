# webserver1.py — Bagian 1: server HTTP paling dasar dari socket mentah.
# Mengikuti Ruslan Spivak, "Let's Build A Web Server. Part 1."
# https://ruslanspivak.com/lsbaws-part1/
#
# Sengaja dibuat sekecil ini: server ini MENGABAIKAN isi request sepenuhnya
# dan selalu menjawab "Hello, World!". Tujuannya memahami siklus hidup
# socket server: socket -> setsockopt -> bind -> listen -> accept loop.

import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    client_connection.close()
