from clockify import report
from redmine import get_time_entries
from utils import pr

entries = get_time_entries('lyxn-portal-build')
pr(entries)
# print(report())