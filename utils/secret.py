'''
Everything that's secret. IMPORTANT: Add this file to .gitignore!
'''

SECRET_KEY = 'rlx@p)7o*z!sf=cm26aded5^h&5pgfglqq)%c+)mdk2os#$e%1'
EMAIL_PASSWORD = 'k1ndy123'


def get_secret_key():
    return SECRET_KEY


def get_email_password():
    return EMAIL_PASSWORD