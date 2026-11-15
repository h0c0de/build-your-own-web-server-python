# Build Pertama BYOX — Web Server Python

Dipilih Vero 14 Nov 2026 ("Mulai dari Web Server Python"), dimulai 15 Nov 2026.
Sumber induk: fork https://github.com/h0c0de/build-your-own-x → kategori *Build your own Web Server*.

## Panduan yang diikuti

Ruslan Spivak — *Let's Build A Web Server* (3 bagian, terverifikasi 15 Nov 2026):

1. **Bagian 1 — Server HTTP dasar dari socket mentah**
   https://ruslanspivak.com/lsbaws-part1/
   Hasil: `webserver1.py` — listening socket, loop accept, balas `Hello, World!` ke semua request.
2. **Bagian 2 — WSGI**
   https://ruslanspivak.com/lsbaws-part2/
   Hasil: `webserver2.py` — server yang bisa menjalankan aplikasi Flask/Pyramid/Django tanpa diubah.
3. **Bagian 3 — Konkurensi**
   https://ruslanspivak.com/lsbaws-part3/
   Hasil: server konkuren (fork + penanganan SIGCHLD/zombie) — obat untuk server iteratif Bagian 1–2 yang hanya melayani satu request bergantian.

## Pagar selesai (disepakati dari saran 14 Nov)

Satu build dihitung selesai hanya bila:
- [ ] Kode tiap bagian jalan dan terbukti dengan uji nyata (curl), bukan sekadar tertulis.
- [ ] `CATATAN.md` terisi satu halaman per bagian: konsep inti + kejutan/kegagalan.
- [ ] Mini Redis Python TIDAK dibuka sebelum build ini selesai.

## Status

- [x] Bagian 1 — selesai & terverifikasi 15 Nov 2026 (lihat CATATAN.md)
- [x] Bagian 2 — WSGI, selesai & terverifikasi 15 Nov 2026 (lihat CATATAN.md)
- [x] Bagian 3 — Konkurensi, selesai & terverifikasi 15 Nov 2026 (lihat CATATAN.md)

**Build tuntas penuh 15 Nov 2026** — 3/3 bagian jalan dan terbukti dengan uji nyata, catatan lengkap, dan hasil diterbitkan sebagai repo publik: https://github.com/h0c0de/build-your-own-web-server-python (commit snapshot pertama `b515ce9`).

## Cara menjalankan Bagian 1

```sh
python3 webserver1.py          # Serving HTTP on port 8888 ...
curl -i http://localhost:8888/hello
```
