from utils.deployment import is_local_env

LOCAL_ENV_BOOL = is_local_env()

if LOCAL_ENV_BOOL:
    from local import *
else:
    from prod import *

