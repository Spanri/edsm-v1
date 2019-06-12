from apscheduler.schedulers.background import BackgroundScheduler
import os
# import sys
import django
# sys.path.append('django_auth')
# #from django_project import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_auth.settings')
django.setup()

from users.models import Notif, User
# from apscheduler.scheduler import Scheduler
sched = BackgroundScheduler()


@sched.scheduled_job('interval', seconds=10)
def job():
    print('sss')
    # Ищем нотифы, где статус 2 (то есть те, которые надл подписать)
    notif = Notif.objects.filter(status=2)
    # Находим людей, которым нужно отправлять уведомление
    users = User.objects.filter(is_get_notif_expired_email=True)
    # Проверяем, может в них время date_expire истекло.
    # Если время истекло, то посылаем уведомления
    for i, n in enumerate(notif):
        if n.date_expire and n.date_expire < timezone.now() and n.is_notif_expire == False:
            if (n.user.profile.first_name != "" and n.user.profile.patronymic != ""):
                full_name = n.user.profile.second_name + " " + \
                    n.user.profile.first_name[0] + \
                    "." + n.user.profile.patronymic[0] + "."
            else:
                full_name = n.user.profile.second_name
            for i, u in enumerate(users):
                print(u.email)
                send_mail(
                    'Уведомление от СЭД МТУСИ',
                    'Уведомляем, что пользователь ' + full_name + ' (' + n.user.email +
                    ') просрочил срок подписи документа "' + n.doc.title + '".',
                    'edmsmtuci@gmail.com',
                    [u.email, ],
                    fail_silently=False,
                )
            n.is_notif_expire = True
            n.save()

# sched.configure(options_from_ini_file)
sched.start()





