import importlib.util
import sys
from logging import info
from signal import signal, SIGINT, SIGTERM

from app.config import environment, settings
from app.config.logger import configure as configure_logger

# Define the path to the app.py file
app_file_path = './app.py'

# Load the app.py module dynamically
spec = importlib.util.spec_from_file_location('App', app_file_path)
app_module = importlib.util.module_from_spec(spec)
sys.modules['App'] = app_module
spec.loader.exec_module(app_module)


def handle_signal(sig, frame):
    info(f'Got signal: {sig}. Shutting down gracefully...')
    sys.exit(0)


def print_startup_message(host: str, port: int):
    local_ip = 'localhost'
    print(f'Listening on http://{local_ip}:{port}/ (for local access)')
    print(f'Serving on all hosts http://{host}:{port}/')
    print('Hit Ctrl-C to quit.\n')


def main():
    server = environment.server
    db_name = environment.db_name

    # Configure the logger before doing anything else
    configure_logger(
        environment.logging_level,
        environment.graylog_host,
        environment.graylog_port
    )

    # Log application settings
    info(
        '\nApplication settings:\n'
        'server = %s\n'
        'host = %s\n'
        'port = %s\n'
        'db_name = %s\n'
        'db_echo = %s\n'
        'reloader = %s\n'
        'debug = %s\n',
        server,
        settings.host,
        settings.port,
        db_name,
        environment.db_echo,
        environment.reloader,
        environment.debug
    )

    application = app_module.App(
        server=server,
        host=settings.host,
        port=settings.port,
        db_name=db_name,
        db_echo=environment.db_echo,
        reloader=environment.reloader,
        debug=environment.debug
    )

    application.add_database_connection()
    application.add_routes()
    print_startup_message(application.host, application.port)
    application.run()


if __name__ == '__main__':
    signal(SIGINT, handle_signal)
    signal(SIGTERM, handle_signal)
    main()
