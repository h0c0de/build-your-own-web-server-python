# Build Your Own Web Server — Python

Membangun web server dari nol dengan Python murni: dari socket mentah, ke
server WSGI yang bisa menjalankan aplikasi Flask/Pyramid, sampai server
konkuren berbasis `fork` dengan penanganan zombie.

Build pertama dari fork [build-your-own-x](https://github.com/h0c0de/build-your-own-x),
mengikuti seri **_Let's Build A Web Server_** oleh Ruslan Spivak:

- [Part 1](https://ruslanspivak.com/lsbaws-part1/) — server HTTP dasar dari socket
- [Part 2](https://ruslanspivak.com/lsbaws-part2/) — WSGI
- [Part 3](https://ruslanspivak.com/lsbaws-part3/) — konkurensi

## Isi

| Berkas | Bagian | Isi |
|---|---|---|
| `webserver1.py` | 1 | Server HTTP paling dasar: socket → bind → listen → accept, selalu menjawab `Hello, World!` |
| `webserver2.py` | 2 | Server WSGI: memuat aplikasi lewat argumen `module:callable` |
| `wsgiapp.py` | 2 | Aplikasi WSGI polos tanpa framework |
| `flaskapp.py` | 2 | Aplikasi Flask minimal (`/hello`) |
| `pyramidapp.py` | 2 | Aplikasi Pyramid minimal (`/hello`) |
| `webserver3b.py` | 3 | Server iteratif yang tidur — titik masalah antrean |
| `webserver3c.py` | 3 | Server konkuren berbasis `fork` (versi antara) |
| `webserver3g.py` | 3 | Versi final: fork + handler SIGCHLD `grim_reaper` (panen zombie) |
| `RENCANA.md` | — | Rencana build, pagar selesai, status |
| `CATATAN.md` | — | Catatan belajar satu halaman per bagian, dari hasil uji nyata |

## Menjalankan

Butuh Python 3.7+; Bagian 2 butuh Flask/Pyramid (di tutorial dipasang dalam venv):

```sh
python3 -m venv lsbaws && ./lsbaws/bin/pip install flask pyramid

python3 webserver1.py                              # Bagian 1, port 8888
./lsbaws/bin/python webserver2.py flaskapp:app     # Bagian 2 + Flask
./lsbaws/bin/python webserver2.py pyramidapp:app   # Bagian 2 + Pyramid
python3 webserver3g.py                             # Bagian 3, server konkuren final

curl http://localhost:8888/hello
```

## Status verifikasi (15 Nov 2026)

Ketiga bagian selesai dan terbukti dengan uji nyata — bukan sekadar tertulis:

- Bagian 1: `curl` menerima `HTTP/1.1 200 OK` + `Hello, World!` di path apa pun.
- Bagian 2: satu server yang sama melayani aplikasi polos, Flask, dan Pyramid
  tanpa diubah; path tak dikenal dijawab 404 oleh aplikasi (routing milik aplikasi).
- Bagian 3 (server tidur 5 detik): iteratif menyelesaikan 2 request serentak
  dalam 5,00 & 10,00 detik (mengantre); konkuren menyelesaikan 3 request
  serentak dalam ±5,00 detik; versi final menjawab 20/20 request paralel
  dengan 0 proses zombie (versi antaranya meninggalkan 3 zombie — terlihat di `ps`).

Detail pengukuran dan konsep per bagian ada di `CATATAN.md`.
