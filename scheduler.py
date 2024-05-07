from constants import seconds_in_a_day
from database import get_subscriptions
from logger import logger
from send_newsletter import check_subscription_and_send_newsletter
from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            ret = self.function(*self.args, **self.kwargs)
            if not ret: break

def start_schedule(subscription):
    try:
        RepeatTimer(seconds_in_a_day,check_subscription_and_send_newsletter,list(subscription)).start()
        logger.info("Schedule a timer for subscription {subscription}".format(subscription = subscription))
    except Exception as e:
        logger.error("Failed to timer a subscription. subscription {subscription} Exception: {e}".format(subscription = subscription, e = e))


def start_schedules():
    subscriptions = get_subscriptions()
    for subscription in subscriptions:
        start_schedule(subscription)
