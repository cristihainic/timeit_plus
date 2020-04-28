import smtplib
import time
import logging
from functools import wraps

from email_templates import warning_template

logging.basicConfig(level=logging.INFO)
default_logger = logging.getLogger(__name__)


def send_tplus_mail(email_config, msg, logger):
    required_keys = ['host', 'port', 'username', 'password', 'from', 'to']

    try:
        assert all(k in email_config for k in required_keys)
    except (AssertionError, TypeError):
        logger.error('tplus email_config improperly configured. Check that it\'s a dict and that all keys are present.')

    recipients = email_config['to']
    if isinstance(recipients, list):
        recipients = ', '.join(recipients)

    email_msg = warning_template.format(recipients, email_config['from'], msg)

    with smtplib.SMTP(email_config['host'], email_config['port']) as smtp_server:
        smtp_server.login(email_config['username'], email_config['password'])
        smtp_server.sendmail(email_config['from'], email_config['to'], email_msg)

    logger.info(f'Warning emails sent to: {email_config["to"]}')


def tplus(max_time=None, email_config=None, logger=default_logger):
    """
    Decorator. Emits logging and (optionally) email warnings if the execution time of a function in seconds exceeds
    the expectation passed as the `max_time` argument. If not, execution time is logged as info.

    :param max_time: int or float specifying maximum number of seconds the function execution is intended to take
    :param email_config: a dict containing these mandatory keys and example values:
    - 'host': 'smtp.gmail.com'
    - 'port': 587
    - 'username': 'user'
    - 'password': 'somepass'
    - 'from': 'tplus@example.com'
    - 'to': ['someone@example.com', 'someone.else@exmaple.com']
    :param logger: a Python `logging.Logger()` instance. A default is provided for convenience
    """
    def timeit_plus(func):
        @wraps(func)
        def time_check(*args, **kwargs):
            before = time.time()
            func_result = func(*args, **kwargs)
            result = time.time() - before
            if max_time and result > max_time:
                msg = (f'`{func.__name__}` took longer than maximum execution time specified ({max_time} seconds). '
                       f'Actual time: {result} seconds.')
                logger.warning(msg)
                if email_config:
                    send_tplus_mail(email_config, msg, logger)
            else:
                logger.info(f'`{func.__name__}` took {result} seconds.')
            return func_result
        return time_check
    return timeit_plus
