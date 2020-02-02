# mutate the first line
import random
import string
import sys

SPECIAL_INPUT = ["p cnf 1 1\na! 0\n",
                 "p cnf 1 1\n394890123456789\n",
                 "p cnf 10 10\n1 2 -4\n",
                 "p cnf 1 1\n1 2 3 4 5 6 0\n1 2 3 4 5 6 -7\n"]


def random_string_generator(length):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return res


# no need filename (same as create_input, you can delete it)
def create_trash_input(sut_path, index):
    data = SPECIAL_INPUT[index]
    with open(sut_path + "/tmp.cnf", 'w') as file:
        file.writelines(data)


# Read and edit a file
def create_input(sut_path):
    # with open(filename, 'r') as file:
    #     data = file.readlines()
    #     mark = random.randint(2, 3)
    #     if mark == 0:
    #         data[0] = first_line_mutation(data[0])
    #     elif mark == 1:
    #         for _ in range(10):
    #             line = random.randint(1, len(data))
    #             data[line] = random_line_mutation(data[line])
    #     else:
    #     data = generate_random_number_cnf()

    data = generate_random_number_cnf()
    with open(sut_path + "/tmp.cnf", 'w') as file:
        file.writelines(data)


# mutate data line
def random_line_mutation(line):
    print("Mutating a random line")
    digits = line.split(' ')
    mark = random.randint(0, 1)
    for i in range(len(digits)):
        if mark == 0:
            digits[i] += '000000000000000000'
        elif mark == 1:
            digits[i] += 'a'
    return combine(digits)


# mutate first line
def first_line_mutation(line):
    print("Mutating the first line")
    digits = line.split(' ')
    mark = random.randint(1, 4)
    if mark == 1:
        digits[1] = 'z'
    elif mark == 2:
        digits[2] = sys.maxsize
    elif mark == 3:
        digits[3] = sys.maxsize
    elif mark == 4:
        res = random_string_generator(random.randint(0, 100))
        return res
    return combine(digits)


# combine str list to str
def combine(digits):
    line = ''
    for digit in digits:
        line += str(digit) + ' '
    return line[0: len(line) - 1]


# generate cnf txt with valid format but random number between 5 - 950
def generate_random_number_cnf():
    print("Generating random cnf file")
    variable = random.randint(20, 50)
    clause = random.randint(40, 100)
    txt = ['p cnf ' + str(variable) + " " + str(clause) + '\n']
    percent = random.uniform(0.1, 0.9)
    for i in range(1, clause):
        line = ''
        for _ in range(1, random.randint(1, variable)):
            mark = random.randint(0, 1)
            if mark == 1:
                line += '-'
            line += str(random.randint(1, int(variable * percent)))
            line += ' '
        line += '0\n'
        txt.append(line)
    return txt


# currently unused
def generate_invalid_cnf():
    txt = ['p cnf 2 3']
    for i in range(3):
        line = random_string_generator(random.randint(5, 10))
        line += ' 0'
        txt.append(line)
    return txt
