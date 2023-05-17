import random
import locale
from faker import Faker


def _currency():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(int(random.uniform(1, 100000)), grouping=True)


def _name():
    fake = Faker()
    return fake.name()


def _country():
    fake = Faker()
    return fake.country()


def load():
    return dict(country=_country(), name=_name(), amount=_currency())
