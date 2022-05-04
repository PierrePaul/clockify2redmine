from clockify import report
from redmine import get_time_entries, init_redmine, redmine_format
from utils import pr, prior_week_end
from datetime import datetime, timedelta

if __name__ == '__main__':
    init_redmine()

    date_start = prior_week_end()
    date_end = datetime.utcnow()

    clockify_entries = report(iso_start=date_start.isoformat() + 'Z', iso_end=date_end.isoformat() + 'Z')

    # Redmine doesnt return time entries on the date, only > date_start and < date_end
    date_start = date_start - timedelta(hours=24)
    date_end = date_end + timedelta(hours=24)

    redmine_entries = get_time_entries(date_start.strftime('%Y-%m-%d'), date_end.strftime('%Y-%m-%d'))
    redmine_entries = redmine_format(redmine_entries)

    pr(redmine_entries)
    pr(clockify_entries)
    pr('----------')
    for project_id, entries in clockify_entries.items():
        for date_, task in entries.items():
            for task_id, total in task.items():
                pr(redmine_entries[project_id][date_])
                if project_id in redmine_entries \
                        and date_ in redmine_entries[project_id] \
                        and task_id in redmine_entries[project_id][date_]:
                    diff = total - redmine_entries[project_id][date_][task_id]
                    if diff > 0:
                        print('need to create redmine task')
                        # create_entry(issue_id=task_id, spent_on=date_, hours=missing_hours)
                    elif diff < 0:
                        print('time overlogged in redmine')
                    else:
                        print(f'time in sync for {date_} {task_id}')
