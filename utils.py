from pprint import PrettyPrinter
from datetime import datetime, timedelta
import math
import dateutil.parser
pp = PrettyPrinter(indent=4)


def pr(*args):
    pp.pprint(*args)


def ceil(number):
    return math.ceil(number*100)/100


def prior_week_end():
    return datetime.utcnow() - timedelta(days=((datetime.now().isoweekday()) % 7) + 7)


def prior_week_start():
    return datetime.utcnow() - timedelta(weeks=1, days=(datetime.now().isoweekday()))


def get_date(time_entry) -> str:
    te_date = dateutil.parser.parse(time_entry.get('timeInterval').get('start'))
    return te_date.strftime('%Y-%m-%d')


def get_start_end(te) -> tuple:
    start = dateutil.parser.parse(te.get('timeInterval').get('start'))
    if te.get('timeInterval').get('end'):
        end = dateutil.parser.parse(te.get('timeInterval').get('end'))
    else:
        py = pytz.timezone('Canada/Eastern')
        end = datetime.now()
        end = py.localize(end)

    return start, end
