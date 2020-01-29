# mutate the first line
import random
from pathlib2 import Path



# generate valid cnf input

def generate_valid_cnf():
    cnf = ''

    return cnf


# generate invalid cnf input
def generate_invalid_cnf():
    cnf = ''
    return cnf


def ub_number_mutation(filename):
    path = Path(filename)
    text = path.read_text()
    text = text.replace('1', '2')
    path.write_text(text)


def genrate_mutation(line):
    return ''