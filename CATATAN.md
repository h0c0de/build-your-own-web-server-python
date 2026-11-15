# Catatan Build — Web Server Python

Satu bagian = satu halaman. Ditulis sesudah uji nyata, bukan sesudah membaca.

## Bagian 1 — Server HTTP dasar (15 Nov 2026, terverifikasi)

**Yang dibangun:** `webserver1.py` (±25 baris) — server HTTP dari socket mentah di port 8888.

**Bukti jalan:** Python 3.12.3; `curl -i http://localhost:8888/hello` → `HTTP/1.1 200 OK` + `Hello, World!`; path sembarang pun dijawab sama. Sesudah uji server dimatikan dan port terverifikasi bebas lagi.

**Konsep inti:**
- Siklus hidup socket server cuma lima langkah: `socket()` → `setsockopt(SO_REUSEADDR)` → `bind()` → `listen()` → loop `accept()`. Semua server "sungguhan" (Nginx, Gunicorn) memulai dari pola yang sama.
- HTTP di atas TCP itu teks polos: request = baris `GET /path HTTP/1.1` + header; respons = baris status + baris kosong wajib + body. Telnet pun bisa jadi klien HTTP manual.
- `SO_REUSEADDR` = supaya server bisa langsung dinyalakan ulang di port yang sama tanpa menunggu sisa koneksi lama.

**Keterbatasan yang disengaja (jadi pertanyaan Bagian 2–3):**
- Server ini *mengabaikan* request sepenuhnya — path/method apa pun dijawab `Hello, World!`. Belum ada routing, belum ada aplikasi.
- Dia *iteratif*: satu request dilayani sampai tuntas sebelum `accept()` berikutnya. Klien kedua mengantre. → Bagian 3.
- Belum bisa menjalankan aplikasi framework apa pun. → Bagian 2 (WSGI).

**Kejutan dari uji nyata:**
- Log server kosong (0 byte) padahal server jelas melayani dua request: `print()` Python ter-buffer saat stdout dialihkan ke berkas, dan proses dimatikan sebelum sempat flush. Pelajaran praktis: untuk server yang log-nya dipantau, jalankan `python3 -u` atau `flush=True`.

## Bagian 2 — WSGI (15 Nov 2026, terverifikasi)

**Yang dibangun:** `webserver2.py` — kelas `WSGIServer` yang memuat aplikasi dari argumen `module:callable`, plus tiga aplikasi uji: `wsgiapp.py` (polos), `flaskapp.py`, `pyramidapp.py`. Framework dipasang di venv `lsbaws/` persis seperti tutorial (Flask 3.1.3 + Pyramid).

**Bukti jalan — server yang sama, nol perubahan kode, tiga aplikasi berbeda:**
- `wsgiapp:app` → `Hello world from a simple WSGI application!`
- `flaskapp:app` → `/hello` menjawab `Hello world from Flask!`; path tak dikenal menjawab **404 dari Flask sendiri** — bukti routing sudah pindah ke aplikasi (bandingkan Bagian 1: semua path dijawab sama oleh server).
- `pyramidapp:app` → `Hello world from Pyramid!`
- Header `Server: WSGIServer 0.2` muncul di semua respons = server kami yang mengantar, aplikasi yang menjawab.

**Konsep inti:**
- Kontrak WSGI cuma satu kalimat: aplikasi adalah callable `(environ, start_response)` yang mengembalikan iterable berisi bytes. Siapa pun yang memenuhi kontrak ini bisa dipasangkan dengan server mana pun yang memenuhinya — inilah yang membebaskan pilihan framework dari pilihan server (di dunia nyata: Gunicorn/uWSGI/Waitress × Django/Flask/Pyramid).
- Alur per request: server membaca & mem-parse request → merakit dict `environ` (method, path, server name/port, variabel `wsgi.*`) → memanggil aplikasi → aplikasi menetapkan status+header lewat `start_response` dan mengembalikan body → server merakit respons HTTP mentah dan mengirimnya.
- Pemisahan peran terlihat dari header: `Content-Type`/`Content-Length` datang dari aplikasi; `Date`/`Server` ditambahkan server.

**Catatan jujur:**
- Header `Date` di kode tutorial *hardcoded* `Mon, 15 Jul 2019` — terlihat apa adanya di semua respons uji. Di server produksi tanggal ini wajib diambil dari jam sistem.
- Django TIDAK diuji: contohnya di tutorial membutuhkan proyek Django utuh (`django-admin startproject`) dan tutorialnya sendiri menyarankan clone repo pendamping. Tiga bukti di atas sudah menunjukkan kontraknya bekerja lintas framework.
- `start_response` di sini melewatkan callable `write()` yang diwajibkan spesifikasi — penyederhanaan sadar dari tutorial, tercatat supaya tidak dikira kelalaian.
- Server ini tetap iteratif (satu request tuntas dulu, baru berikutnya) → Bagian 3.

## Bagian 3 — Konkurensi (15 Nov 2026, terverifikasi dengan pengukuran)

**Yang dibangun:** `webserver3b.py` (iteratif + tidur, titik masalah), `webserver3c.py` (konkuren fork, versi antara), `webserver3g.py` (final: fork + handler SIGCHLD). Tidur di versi uji 5 detik; tutorial memakai 60 — logika identik, angka dipilih supaya terukur.

**Bukti jalan — dua curl serentak, server yang tidur 5 detik sesudah menjawab:**
- Iteratif (3b): curl selesai dalam **5,00 dtk dan 10,00 dtk** — yang kedua mengantre satu siklus penuh.
- Konkuren (3c): tiga curl serentak selesai **semuanya ±5,00 dtk** — dilayani child yang berbeda-beda.
- Final (3g, tanpa tidur): **20 request paralel, 20/20 dijawab** `Hello, World!`, dan daftar proses bersih.

**Konsep inti:**
- `fork()` dipanggil sekali tapi kembali dua kali: di parent membawa PID child, di child membawa 0. Parent server konkuren hanya accept → fork → accept lagi; child yang bekerja.
- Descriptor socket digandakan oleh fork dan dihitung kernel dengan *reference count*: socket sungguhan tertutup hanya saat hitungan mencapai 0 — karena itu parent dan child wajib masing-masing menutup salinan yang tidak mereka pakai (versi tutorial 3d menunjukkan akibatnya bila tidak: klien menggantung karena FIN tak pernah terkirim, dan descriptor bocor sampai habis).
- **Zombie itu nyata dan terlihat:** sesudah uji 3c, `ps` menunjukkan 3 child berstatus `Z` — proses mati yang belum dipanen parent-nya. Obatnya di 3g: handler SIGCHLD `grim_reaper` memanen dengan `waitpid(-1, WNOHANG)` **dalam loop**, karena sinyal tidak mengantre — satu sinyal bisa mewakili banyak kematian sekaligus. Sesudah uji 3g: **0 zombie**.
- accept() bisa terinterupsi sinyal (EINTR) dan harus diulang, bukan dianggap error. Catatan modern: Python 3 (PEP 475) umumnya sudah mengulang syscall terinterupsi secara otomatis; cabang EINTR di kode dipertahankan sesuai tutorial.

**Kejutan dari uji nyata:**
- Antrean iteratif terukur persis seperti teori (5 vs 10 detik) — dan koneksi kedua sebenarnya sudah *terhubung* oleh kernel (backlog `listen`), hanya tidak dilayani. "Terhubung" ≠ "dilayani".
- Zombie bukan konsep buku: tiga baris `Z` di `ps` muncul dari server yang baru saja kami jalankan sendiri.

**Status build:** 3/3 bagian selesai dan terverifikasi; catatan lengkap. Sisa pagar administratif: hasil ini masih folder lokal — belum jadi repo GitHub tersendiri.
