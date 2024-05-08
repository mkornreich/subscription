from constants import seconds_in_a_day
from database import get_subscriptions
from logger import logger
from send_newsletter import check_subscription_and_send_newsletter
from subscription import Subscription
from threading import Timer


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            ret = self.function(*self.args, **self.kwargs)
            if not ret:
                break


def start_schedule(subscription: Subscription) -> None:
    try:
        RepeatTimer(seconds_in_a_day, check_subscription_and_send_newsletter, [
                    subscription]).start()
        logger.info("Successfully scheduled a timer for subscription_number {subscription_number}".format(
            subscription_number=subscription.subscription_number))
    except Exception as e:
        logger.error("Failed to schedule a timer for subscription_number {subscription_number} Exception: {e}".format(
            subscription_number=subscription.subscription_number, e=e))


def start_schedules() -> None:
    subscriptions = get_subscriptions()
    for subscription in subscriptions:
        start_schedule(subscription)
