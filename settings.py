import sys
import logging
import logging.config
import os

DOCKER_OPS_LOGS_FILE='/ops_logs/docker_ops.log'

WRAPPERS = {
    'run': os.getenv('RUN_WRAPPER', 'sandbox;log_driver').split(';'),
    'wait': os.getenv('WAIT_WRAPPER', '').split(';')
}

DOCKER_LOG_SETTINGS = {
    'driver': os.getenv('DOCKER_LOG_DRIVER', 'fluentd'),
    'host': os.getenv('FLUENTD_ADDRESS', 'localhost:24224')
}

LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)-15s %(name)s [%(levelname)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': '/var/log/luna.log',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5
        }
    },
    'loggers': {
        'luna': {
            'level': 'DEBUG',
            'propagate': 1
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
}

# FORMAT = '%(levelname)-6s %(asctime)-15s %(name)s: %(message)s'
# logging.basicConfig()
logging.config.dictConfig(LOGGING)

IPTABLE_CHAIN_NAME = 'ALAUDA_LINK'
JAKIRO = {
    'API_ENDPOINT': 'http://api.int.alauda.io',
    'INNER_API_ENDPOINT': 'http://innerapi.int.alauda.club:8080',
    'USER': 'sys_admin',
    'PASSWORD': '07Apples'
}
DOCKER_API_VERSION = '1.17'
LINA_ENDPOINT = "lina.int.alauda.club:8080"
DNS = ['8.8.8.8', '4.4.4.4']
