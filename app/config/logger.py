from logging import config, getLogger, WARNING


def configure(logging_level: str, graylog_host: str, graylog_port: int) -> None:
    logging_config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s: %(message)s',
                'datefmt': '%m/%d/%Y %I:%M:%S %p'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': logging_level
            },
            'graylog': {
                'class': 'graypy.GELFUDPHandler',
                'host': graylog_host,
                'port': graylog_port,
                'level': logging_level
            }
        },
        'root': {
            'handlers': ['console', 'graylog'],
            'level': logging_level
        }
    }

    config.dictConfig(logging_config)
    getLogger('waitress').setLevel(WARNING)
