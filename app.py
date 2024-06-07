import os

from bottle import Bottle, TEMPLATE_PATH

from app.config.routes import setup_routing


class App:
    def __init__(
        self,
        server='auto',
        host='0.0.0.0',
        port=8080,
        db_name='',
        db_echo=False,
        reloader=False,
        debug=False,
        template_path='app/views/'
    ):
        self.server_type = server
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db_echo = db_echo
        self.reloader = reloader
        self.debug = debug
        self.template_path = template_path
        self.bottleInstance = Bottle()
        self.template_path = os.path.normpath(self.template_path)

        if self.template_path not in TEMPLATE_PATH:
            TEMPLATE_PATH.append(self.template_path)

    def add_routes(self):
        setup_routing(self.bottleInstance)

    def run(self):
        self.bottleInstance.run(
            server=self.server_type,
            host=self.host,
            port=self.port,
            reloader=self.reloader,
            debug=self.debug
        )
