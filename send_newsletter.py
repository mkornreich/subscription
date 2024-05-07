from constants import seconds_in_a_week
from database import check_subscription_number
from logger import logger
from time import time

def check_subscription_and_send_newsletter(subscription_number, email, industry, source, subcategory, last_seen):
    if not check_subscription_number(subscription_number):
        logger.info("Subscription number {subscription_number} not in the database. Ending timer for subscription".format(subscription_number = subscription_number))
        return False
    current_timestamp = int(time())
    week_ago_timestamp = current_timestamp - seconds_in_a_week
    week_ago_timestamp_str = str(week_ago_timestamp)
    if last_seen <= week_ago_timestamp_str:
        logger.info("Newsletter for email {email} was sent less than a week ago".format(email = email))
        return True
    send_newsletter(email,industry,source,subcategory)
    update_timestamp_for_subscription(subscription_number, str(current_timestamp))
    logger.info("Newsletter sent to email {email}".format(email = email))
    return True

def send_newsletter(email, industry="", source="", subcategory=""):
    # Not implemented
    # Calls the other process that sends the newsletters
    pass
