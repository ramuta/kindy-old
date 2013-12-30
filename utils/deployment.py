'''
    preverimo ali app tece lokalno ali na heroku
    na Heroku smo nastavili: heroku config:add DJANGO_LOCAL_DEV=0
'''
import os


def is_local_env():
    try:
        LOCAL_ENV = os.environ["DJANGO_LOCAL_DEV"]
        if LOCAL_ENV == 0 or LOCAL_ENV == '0':
            return False
        else:
            return True
    except KeyError:
        return True


def get_dj_env():
    try:
        GET_ENV = os.environ["DJANGO_ENV"]
        if GET_ENV == 1:
            return 'prod'
        elif GET_ENV == 2:
            return 'dev'
        else:
            return 'local'
    except KeyError:
        return 'local'