from constants import seconds_in_a_week
from database import check_subscription_exists, update_timestamp_for_subscription
from logger import logger
from time import time


def check_subscription_and_send_newsletter(subscription):
    if not check_subscription_exists(subscription):
        logger.info("Subscription number {subscription_number} not in the database. Ending timer for subscription".format(
            subscription_number=subscription.subscription_number))
        return False
    current_timestamp = int(time())
    week_ago_timestamp = current_timestamp - seconds_in_a_week
    week_ago_timestamp_str = str(week_ago_timestamp)
    last_sent = subscription.last_sent
    if last_sent and int(last_sent) <= week_ago_timestamp_str:
        logger.info(
            "Newsletter for email {email} was sent less than a week ago".format(email=subscription.email))
        return True
    send_newsletter(subscription)
    update_timestamp_for_subscription(
        subscription, str(current_timestamp))
    logger.info("Newsletter sent to email {email}".format(
        email=subscription.email))
    return True


def send_newsletter(subscription):
    # Not implemented
    # Calls the other process that sends the newsletters
    pass
