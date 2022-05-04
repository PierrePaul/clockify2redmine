GOOGLE_USER = ''
GOOGLE_PASSWORD = ''
REDMINE_TOKEN = ''
REDMINE_URL = ''
REDMINE_UID = ''

CLOCKIFY_TOKEN = ''
CLOCKIFY_WID = ''
CLOCKIFY_UID = ''



try:
    from config_local import *
except ModuleNotFoundError:
    pass
