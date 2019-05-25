import random
import string

correct_string = 'this is string for test'
correct_id = 'thisid42'


def random_string(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))