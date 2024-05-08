from constants import seconds_in_a_week
from database import check_subscription_exists, get_timestamp_for_subscription, update_timestamp_for_subscription
from logger import logger
from subscription import Subscription
from time import time


def check_subscription_and_send_newsletter(subscription: Subscription) -> bool:
    if not check_subscription_exists(subscription):
        logger.info("Subscription number {subscription_number} is not in the database. Ending timer for subscription".format(
            subscription_number=subscription.subscription_number))
        return False
    current_timestamp = int(time())
    week_ago_timestamp = current_timestamp - seconds_in_a_week
    week_ago_timestamp_str = str(week_ago_timestamp)
    last_sent = get_timestamp_for_subscription(subscription)
    if last_sent and last_sent >= week_ago_timestamp_str:
        logger.info(
            "Newsletter for email {email} was sent less than a week ago".format(email=subscription.email))
        return True
    send_newsletter(subscription)
    update_timestamp_for_subscription(
        subscription, str(current_timestamp))
    logger.info("Newsletter sent to email {email}".format(
        email=subscription.email))
    return True


def send_newsletter(subscription: Subscription):
    # Not implemented
    # Calls the other process that sends the newsletters
    pass
