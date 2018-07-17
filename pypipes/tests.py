import sys
import random
import string

from pypipes.task_client import TaskClient
from pypipes.tests_env import *


def _generate(max_size):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, max_size)))


def _reduce(value, keep='vowels'):
    vowels = ['a', 'e', 'i', 'o', 'u', ]
    if keep == 'vowels':
        result = [v for v in value if v in vowels]
    else:
        result = [v for v in value if v not in vowels]

    return value, ''.join(result)


def _count(data):
    value, vowels = data

    return value, len(vowels)


client = TaskClient(domain='word-counter', aws_key=AWS_KEY, aws_secret=AWS_SECRET, aws_region=AWS_REGION)

client.register_tasks([
    {'method': _generate, 'workers': 32, 'interval': 0},
    {'method': _reduce, 'workers': 32},
    {'method': _count, 'workers': 16}
])


def generate():
    for res in client.run(0, args=(10, ), iterate=True):
        print(res)


def reduce():
    for res in client.run(1, iterate=True):
        print('%s -> %s' % res)


def count():
    for result in client.run(2, iterate=True):
        print('%s -> %d' % result)


try:
    if sys.argv[1] == 'generate':
        generate()
    elif sys.argv[1] == 'reduce':
        reduce()
    elif sys.argv[1] == 'count':
        count()
    else:
        raise ValueError('Invalid argument: must be one of generate, reduce or count')
except IndexError:
    raise ValueError('Script argument is required')