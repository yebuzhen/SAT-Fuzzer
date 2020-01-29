# mutate the first line
import random
from pathlib2 import Path

# Read and edit a file
def modify_file(filename):
    num_lines = sum(1 for line in open(filename))

    with open(filename, 'r') as file:
        data = file.readlines()

        for i in range(10):
            line = random.randint(1, len(data))
            data[line] = genrate_mutation(data[line])
    
    with open(filename, 'w') as file:
        file.writelines(data)



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


def generate_mutation(line):
    return ''