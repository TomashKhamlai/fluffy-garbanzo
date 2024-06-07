from app.config import settings

if settings.environment == 'development':
    import app.config.environments.development as env
elif settings.environment == 'testing':
    import app.config.environments.testing as env
elif settings.environment == 'production':
    # import app.config.environments.production as env
    pass
else:
    raise RuntimeError('Environment not set or incorrect')


server = env.server or settings.server
host = getattr(env, 'host', settings.host)
port = getattr(env, 'port', settings.port)
graylog_host = getattr(env, 'graylog_host', settings.graylog_host)
graylog_port = getattr(env, 'graylog_port', settings.graylog_port)
debug = env.debug
reloader = env.reloader
db_name = env.db_name
db_echo = env.db_echo
logging_level = env.logging_level
