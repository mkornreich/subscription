from constants import database_filename as filename
from logger import logger
from sqlite3 import connect, Connection
from subscription import Subscription


def get_database() -> Connection:
    return connect(filename)


def create_database() -> None:
    try:
        con = get_database()
        cur = con.cursor()
        command = 'CREATE TABLE IF NOT EXISTS subscriptions(subscription_number INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, industry TEXT DEFAULT "", source TEXT DEFAULT "", subcategory TEXT DEFAULT "", last_sent TEXT DEFAULT "")'
        cur.execute(command)
        con.commit()
        log = "Opened database {filename}".format(filename=filename)
        logger.info(log)
    except Exception as e:
        log = "Failed to open database {filename}. Exception: {e}".format(
            filename=filename, e=e)
        logger.error(log)


def insert_email(email: str, industry="", source="", subcategory="") -> None:
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
        log = "Failed to add new subscription for email {email} to database {filename}. Exception: {e}".format(
            email=email, filename=filename, e=e)
        logger.error(log)


def get_subscription(email: str) -> Subscription:
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
        log = "Failed to retrieve subscription for email {email} from database {filename}. Exception: {e}".format(
            email=email, filename=filename, e = e)
        logger.error(log)
        return None


def get_subscriptions() -> list[Subscription]:
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
        log = "Failed to retrieve all subscriptions from database {filename}. Exception: {e}".format(
            filename=filename, e = e)
        logger.info(log)
        return None


def check_subscription_exists(subscription: Subscription) -> bool:
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
        log = "Failed to check if subscription_number {subscription_number} exists in database {filename}. Exception: {e}".format(
            subscription_number=subscription_number, filename=filename, e = e)
        logger.error(log)
        return None


def update_timestamp_for_subscription(subscription: Subscription, current_timestamp: str) -> None:
    try:
        subscription_number = subscription.subscription_number
        con = get_database()
        cur = con.cursor()
        command = 'UPDATE subscriptions SET last_sent = {current_timestamp} WHERE subscription_number = {subscription_number}'.format(
            current_timestamp=current_timestamp, subscription_number=subscription_number)
        cur.execute(command)
        con.commit()
        log = "Successfully updated timestamp for subscription_number {subscription_number} from database {filename}".format(
            subscription_number=subscription_number, filename=filename)
        logger.info(log)
    except Exception as e:
        log = "Failed to update timestamp for subscription_number {subscription_number} from database {filename}. Exception: {e}".format(
            subscription_number=subscription_number, filename=filename, e = e)
        logger.info(log)


def get_timestamp_for_subscription(subscription: Subscription) -> str:
    try:
        subscription_number = subscription.subscription_number
        cur = get_database().cursor()
        command = 'SELECT last_sent FROM subscriptions WHERE subscription_number = {subscription_number}'.format(
            subscription_number=subscription.subscription_number)
        last_sent = cur.execute(command).fetchone()[0]
        log = "Successfully retrieved last_sent for subscription_number {subscription_number} from database {filename}".format(
            subscription_number=subscription.subscription_number, filename=filename)
        logger.info(log)
        return last_sent
    except Exception as e:
        log = "Failed to retrieve last_sent for subscription_number {subscription_number} from database {filename}. Exception: {e}".format(
            subscription_number=subscription.subscription_number, filename=filename, e = e)
        return None
