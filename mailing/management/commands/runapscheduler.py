import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution

from mailing.models import Mailing, Log, Message, Client

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)


def change_status():
    for mailing in Mailing.objects.all():
        if timezone.now() < mailing.start_time:
            print(f"0 {timezone.now()} --- {mailing.start_time}")
            mailing.status = "C"
        elif mailing.start_time <= timezone.now() <= mailing.end_time:
            print(f"1 {timezone.now()} --- {mailing.start_time}")
            mailing.status = "S"
        else:
            print(f"2 {timezone.now()} --- {mailing.start_time}")
            mailing.status = "F"
            scheduler.shutdown()
        mailing.save()


def start_or_not_mailing():
    mailing_correct = Mailing.objects.filter(status="S")
    print(mailing_correct)
    if mailing_correct:
        for mailing in mailing_correct:
            # logs = Log.objects.filter(mailing=mailing)
            # if not logs.exists():
            add_job(mailing)


def send_mailing(mailing):
    # Log.objects.create(response="Sent", mailing=mailing)

    # title = mailing.message.message_title
    # body = mailing.message.message_body
    # from_email = settings.EMAIL_HOST_USER
    # to_emails = [client.email for client in mailing.clients.all()]
    # send_mail(title, body, from_email, to_emails)

    messages = Message.objects.all()
    clients = Client.objects.all()
    # print(f"{len(messages)} {len(clients)}")
    if messages and clients:
        send_mail(
            subject=messages[0].message_title,
            message=messages[0].message_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in clients],
        )


def add_job(mailing):
    if mailing.period == "D":
        # cron_period = CronTrigger(day="*/1")
        cron_period = CronTrigger(second="*/30")
    elif mailing.period == "W":
        # cron_period = CronTrigger(week="*/1")
        cron_period = CronTrigger(second="*/30")
    else:
        # cron_period = CronTrigger(month="*/1")
        cron_period = CronTrigger(second="*/30")

    scheduler.add_job(send_mailing,
                      trigger=cron_period,
                      id=f"{mailing.pk}",
                      max_instances=1,
                      args=[mailing],
                      replace_existing=True)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs Apscheduler"

    def handle(self, *args, **options):
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(change_status,
                          trigger=CronTrigger(second='*/30'),
                          id='change_status',
                          max_instances=1,
                          replace_existing=True)
        logger.info("Added job 'change_status'.")

        scheduler.add_job(start_or_not_mailing,
                          trigger=CronTrigger(second='*/30'),
                          id='start_or_not_mailing',
                          max_instances=1,
                          replace_existing=True)
        logger.info("Added job 'start_or_not_mailing'.")

        scheduler.add_job(delete_old_job_executions,
                          trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
                          id="delete_old_job_executions",
                          max_instances=1,
                          replace_existing=True)
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
