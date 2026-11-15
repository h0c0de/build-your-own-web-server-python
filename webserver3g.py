# webserver3g.py — Bagian 3, versi FINAL: konkuren + panen zombie.
# Mengikuti Ruslan Spivak, "Let's Build A Web Server. Part 3."
#
# Dua perbaikan dari 3c:
# 1. Handler SIGCHLD "grim_reaper": setiap child yang mati memicu sinyal;
#    handler memanen dengan waitpid(-1, WNOHANG) dalam LOOP — karena
#    sinyal tidak mengantre, satu sinyal bisa mewakili banyak child mati;
#    loop memastikan semuanya terpanen, tidak ada zombie tertinggal.
# 2. accept() yang terinterupsi sinyal (EINTR) diulang, bukan crash.
#    (Di Python 3 modern, PEP 475, syscall yang terinterupsi umumnya
#    sudah diulang otomatis oleh interpreter; cabang ini dipertahankan
#    sesuai tutorial dan tidak berbahaya.)

import errno
import os
import signal
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1024


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # tunggu child mana pun
                os.WNOHANG   # jangan memblokir
            )
        except OSError:
            return
        if pid == 0:  # tidak ada zombie lagi
            return


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    signal.signal(signal.SIGCHLD, grim_reaper)
    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:  # accept terinterupsi sinyal: ulangi
                continue
            else:
                raise
        pid = os.fork()
        if pid == 0:  # child
            listen_socket.close()  # tutup salinan child
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:  # parent
            client_connection.close()  # tutup salinan parent, lanjut accept()


if __name__ == '__main__':
    serve_forever()
