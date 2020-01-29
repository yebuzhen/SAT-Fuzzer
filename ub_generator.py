# mutate the first line
import random
import sys

# Read and edit a file
def modify_file(filename, sut_path):
    num_lines = sum(1 for line in open(filename))

    with open(filename, 'r') as file:
        data = file.readlines()
        mark = random.randint(0, 2)
        if mark == 0:
            data[0] = first_line_mutation(data[0])
        else:
            for i in range(10):
                line = random.randint(1, len(data))
                data[line] = generate_mutation(data[line])

    with open(sut_path+"/tmp.cnf", 'w') as file:
        file.writelines(data)

def generate_mutation(line):
    print("Mutating a random line")
    digits = line.split(' ')
    mark = random.randint(0, 2)
    for i in range(len(digits)):
        if mark == 0:
            digits[i] += '000000000000000000'
        elif mark == 1:
            digits[i] += 'a'
    return combine(digits)


def first_line_mutation(line):
    print("Mutating the first line")
    digits = line.split(' ')
    mark = random.randint(0, 4)
    if mark == 0:
        digits[0] = 'z'
    elif mark == 1:
        digits[1] = 'z'
    elif mark == 2:
        digits[2] = sys.maxsize
    elif mark == 3:
        digits[3] = sys.maxsize
    return combine(digits)


def combine(digits):
    line = ''
    for digit in digits:
        line += str(digit) + ' '
    return line[0 : len(line) - 1]