# mutate the first line
import random
import sys


# Read and edit a file
def modify_file(filename, sut_path):
    num_lines = sum(1 for line in open(filename))

    with open(filename, 'r') as file:
        data = file.readlines()
        mark = random.randint(0, 3)
        if mark == 0:
            data[0] = first_line_mutation(data[0])
        elif mark == 1:
            for i in range(10):
                line = random.randint(1, len(data))
                data[line] = generate_mutation(data[line])
        else:
            data = generate_random_number_cnf()

    with open(sut_path + "/tmp.cnf", 'w') as file:
        file.writelines(data)


# mutate data line
def generate_mutation(line):
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
    mark = random.randint(1, 3)
    if mark == 1:
        digits[1] = 'z'
    elif mark == 2:
        digits[2] = sys.maxsize
    elif mark == 3:
        digits[3] = sys.maxsize
    return combine(digits)


# combine str list to str
def combine(digits):
    line = ''
    for digit in digits:
        line += str(digit) + ' '
    return line[0: len(line) - 1]


# generate cnf txt with valid format but random number between 5 - 950
def generate_random_number_cnf():
    txt = ['p cnf 1000 10000']
    for m in range(1, 10000):
        line = ''
        for n in range(1, 5):
            mark = random.randint(0, 1)
            if mark == 1:
                line += '-'
            line += str(random.randint(5, 950))
            line += ' '
        line += '0'
        txt.append(line)
    return txt
