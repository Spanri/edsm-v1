from docs.views import job0

REFRESH_INTERVAL = 10
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

# Смотрим, если время подписи истекло, указываем это и
# посылаем уведомление
@sched.scheduled_job('interval', seconds=REFRESH_INTERVAL)
def job():
    job0()

def scheduler_sample():
    print('sdsd')
    # subprocess.call('python manage.py scheduler', shell = True, close_fds = True)


sched.start()
