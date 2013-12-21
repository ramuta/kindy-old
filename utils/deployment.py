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