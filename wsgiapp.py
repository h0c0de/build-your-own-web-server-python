# wsgiapp.py — aplikasi WSGI polos tanpa framework (dari Bagian 2 tutorial).
# Membuktikan kontrak WSGI dari sisi aplikasi: terima (environ,
# start_response), panggil start_response sekali, kembalikan iterable bytes.


def app(environ, start_response):
    """A barebones WSGI application.

    This is a starting point for your own Web framework :)
    """
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello world from a simple WSGI application!\n']
