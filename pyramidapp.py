# pyramidapp.py — aplikasi Pyramid minimal (dari Bagian 2 tutorial).
# Diekspor sebagai "app" (hasil make_wsgi_app) supaya bisa dimuat:
# python3 webserver2.py pyramidapp:app

from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response(
        'Hello world from Pyramid!\n',
        content_type='text/plain',
    )


config = Configurator()
config.add_route('hello', '/hello')
config.add_view(hello_world, route_name='hello')
app = config.make_wsgi_app()
