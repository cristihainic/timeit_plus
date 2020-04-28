import time

from timeit_plus import tplus

smtp_config = {
    'host': 'smtp.mailtrap.io',
    'port': 2525,
    'username': '',  # fill this in
    'password': '',  # fill this in
    'from': 'tplus@test.com',
    'to': ['whoever@test.com', 'andthensome@example.com']
}


@tplus(max_time=0.5, email_config=smtp_config)
def f():
    time.sleep(3)
    return 1 + 1


print(f())
