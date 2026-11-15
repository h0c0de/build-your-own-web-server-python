# webserver3c.py — Bagian 3, langkah 1: server KONKUREN berbasis fork.
# Mengikuti Ruslan Spivak, "Let's Build A Web Server. Part 3."
#
# Parent hanya accept() lalu fork: child yang melayani request (dan yang
# tidur — di sini 5 detik, tutorial 60), parent langsung kembali accept().
# Kedua sisi menutup salinan descriptor yang tidak mereka pakai: kernel
# menutup socket sungguhan hanya saat reference count-nya mencapai 0.
#
# Kelemahan versi ini (dibahas tutorial sesudahnya): child yang selesai
# menjadi ZOMBIE karena tidak ada yang memanennya — diperbaiki di 3g.

import os
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5
TIDUR_DETIK = 5  # tutorial: 60


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print('Child PID: {pid}. Parent PID {ppid}'.format(
        pid=os.getpid(), ppid=os.getppid()))
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    time.sleep(TIDUR_DETIK)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))
    while True:
        client_connection, client_address = listen_socket.accept()
        pid = os.fork()
        if pid == 0:  # child
            listen_socket.close()  # tutup salinan child
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)  # child selesai di sini
        else:  # parent
            client_connection.close()  # tutup salinan parent, lanjut accept()


if __name__ == '__main__':
    serve_forever()
