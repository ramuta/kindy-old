from utils.deployment import get_dj_env

DJ_ENV = get_dj_env()

if DJ_ENV == 'local':
    from local import *
elif DJ_ENV == 'prod':
    from prod import *
elif DJ_ENV == 'dev':
    from dev import *