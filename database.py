from constants import database_filename as filename
from logger import logger
from sqlite3 import connect
from subscription import Subscription


def get_database():
    return connect(filename)


def create_database():
    try:
        cur = get_database().cursor()
        command = 'CREATE TABLE IF NOT EXISTS subscriptions(subscription_number INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, industry TEXT DEFAULT "", source TEXT DEFAULT "", subcategory TEXT DEFAULT "", last_sent TEXT DEFAULT "")'
        cur.execute(command)
        log = "Opened database {filename}".format(filename=filename)
        logger.info(log)
    except Exception as e:
        log = "Failed to open database {filename}. Exception: {e}".format(
            filename=filename, e=e)
        logger.error(log)


def insert_email(email, industry="", source="", subcategory=""):
    try:
        con = get_database()
        cur = con.cursor()
        command = 'INSERT OR REPLACE INTO subscriptions(email,industry,source,subcategory) VALUES ("{email}","{industry}","{source}", "{subcategory}")'.format(
            email=email, industry=industry, source=source, subcategory=subcategory)
        cur.execute(command)
        con.commit()
        log = "Added new subscription for email {email} to database {filename}".format(
            email=email, filename=filename)
        logger.info(log)
    except Exception as e:
        log = "Failed to add new subscription for email {email} to database {filename}. Excpetion: {e}".format(
            email=email, filename=filename, e=e)
        logger.error(log)


def get_subscription(email):
    try:
        cur = get_database().cursor()
        command = 'SELECT subscription_number, email, industry, source, subcategory, last_sent FROM subscriptions WHERE email="{email}"'.format(
            email=email)
        value = cur.execute(command).fetchone()
        log = "Successfully retrieved subscription for email {email} from database {filename}".format(
            email=email, filename=filename)
        logger.info(log)
        return Subscription(value)
    except Exception as e:
        log = "Failed to retrieve subscription for email {email} from database {filename}".format(
            email=email, filename=filename)
        logger.error(log)
        return None


def get_subscriptions():
    try:
        cur = get_database().cursor()
        command = 'SELECT subscription_number, email, industry, source, subcategory, last_sent FROM subscriptions'
        values = cur.execute(command).fetchall()
        log = "Successfully retrieved all subscriptions from database {filename}".format(
            filename=filename)
        logger.info(log)
        subscriptions = [Subscription(n) for n in values]
        return subscriptions
    except Exception as e:
        log = "Failed to retrieve all subscriptions from database {filename}".format(
            filename=filename)
        logger.info(log)
        return None


def check_subscription_exists(subscription):
    try:
        subscription_number = subscription.subscription_number
        value = None
        cur = get_database().cursor()
        command = 'SELECT subscription_number FROM subscriptions WHERE subscription_number = {subscription_number}'.format(
            subscription_number=subscription_number)
        value = cur.execute(command).fetchone()
        log = "Successfully checked subscription_number {subscription_number} exists in database {filename}".format(
            subscription_number=subscription_number, filename=filename)
        logger.info(log)
        return True if value else False
    except Exception as e:
        log = "Failed to check if subscription_number {subscription_number} exists in database {filename}".format(
            subscription_number=subscription_number, filename=filename)
        logger.error(log)
        return None


def update_timestamp_for_subscription(subscription, current_timestamp):
    try:
        subscription_number = subscription.subscription_number
        cur = get_database().cursor()
        command = 'UPDATE subscriptions SET current_timestamp = {current_timestamp} WHERE subscription_number = {subscription_number}'.format(
            current_timestamp=current_timestamp, subscription_number=subscription_number)
        log = "Successfully updated timestamp for subscription_number {subscription_number} from database {filename}".format(
            subscription_number=subscription_number, filename=filename)
        logger.info(log)
    except Exception as e:
        log = "Failed to update timestamp for subscription_number {subscription_number} from database {filename}".format(
            subscription_number=subscription_number, filename=filename)
        logger.info(log)
        return None
