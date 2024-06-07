import os

# environment (production, development, test)
environment = os.getenv('ENVIRONMENT', 'development')  # Default to 'development' if ENVIRONMENT is not set

# server backend (cherrypy, gunicorn, waitress, tornado, wsgiref, ...)
# if set to '', a default server backend will be used
server = ''

# define host
host = 'localhost'

# define port
port = 8000

# GreyLog settings
graylog_host = 'localhost'
graylog_port = 12201
