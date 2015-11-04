import sys


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
            'filename': '/var/log/mathilde/lina.log',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5
        }
    },
    'loggers': {
        'peewee': {
            'level': 'INFO',
            'propagate': 1
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
