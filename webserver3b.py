# webserver3b.py — Bagian 3, titik masalah: server ITERATIF yang tidur.
# Mengikuti Ruslan Spivak, "Let's Build A Web Server. Part 3."
# https://ruslanspivak.com/lsbaws-part3/
#
# Sama seperti server Bagian 1, tapi sesudah mengirim respons ia tidur.
# Di tutorial tidurnya 60 detik; di sini 5 detik supaya uji antreannya
# terukur cepat — logikanya identik: selama tidur, accept() berikutnya
# tidak berjalan, jadi klien kedua mengantre di backlog kernel.

import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5
TIDUR_DETIK = 5  # tutorial: 60


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    time.sleep(TIDUR_DETIK)  # blokir proses: tidak ada accept() selama ini


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        client_connection.close()


if __name__ == '__main__':
    serve_forever()
