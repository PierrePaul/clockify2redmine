GOOGLE_USER = ''
GOOGLE_PASSWORD = ''
REDMINE_USER = ''
REDMINE_PASSWORD = ''
REDMINE_URL = ''

CLOCKIFY_TOKEN = ''
CLOCKIFY_WID = ''
CLOCKIFY_UID = ''

try:
    from config_local import GOOGLE_USER, GOOGLE_PASSWORD
    from config_local import REDMINE_URL, REDMINE_PASSWORD, REDMINE_USER
    from config_local import CLOCKIFY_TOKEN, CLOCKIFY_UID, CLOCKIFY_WID
except ModuleNotFoundError:
    pass
