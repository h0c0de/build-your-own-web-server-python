# flaskapp.py — aplikasi Flask minimal (dari Bagian 2 tutorial).
# Yang diekspor sebagai WSGI callable adalah flask_app.wsgi_app,
# dibungkus nama "app" supaya bisa dimuat: python3 webserver2.py flaskapp:app

from flask import Flask
from flask import Response

flask_app = Flask('flaskapp')


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain',
    )


app = flask_app.wsgi_app
