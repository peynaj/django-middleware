import datetime
from django.utils import timezone

max_try_count = 3
expire_sec = 10*60

wrong_try = {}

def incr_wrong_try_count(username):
    k = 'wrong_try_{un}'.format(un=username)
    if k not in wrong_try or wrong_try[k]['expire'] < timezone.now():
        wrong_try[k] = dict(
            count=1,
            expire=timezone.now()+datetime.timedelta(seconds=expire_sec)
        )
    else:
        wrong_try[k]['count'] += 1
    return wrong_try[k]['count'], wrong_try[k].get('expire')

def get_wrong_try_data(username):
    k = 'wrong_try_{un}'.format(un=username)
    if k in wrong_try:
        data = wrong_try[k]
        if data['expire'] < timezone.now():
            wrong_try.pop(k)
            return 0, None
        else:
            return data.get('count', 0), data.get('expire')
    return 0, None
