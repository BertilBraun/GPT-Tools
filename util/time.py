
import datetime


def get_time():
    return datetime.datetime.now().strftime('%H-%M-%S')


def get_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_day():
    return datetime.datetime.now().strftime('%A')
