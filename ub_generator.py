# mutate the first line
import random
import string
import sys

NORM_HEADER = "p cnf 10 10\n"
OVERFLOW_HEADER = "p cnf " + str(sys.maxsize+1) + ' ' + str(sys.maxsize+1) + '\n'
RANDOM_HEADER = string.printable
SPECIAL_INPUT = ["",
                 "p cnf\n",
                 OVERFLOW_HEADER,
                 RANDOM_HEADER,
                 NORM_HEADER,
                 NORM_HEADER + string.punctuation + '\n',
                 NORM_HEADER + string.printable + '\n']


# def random_string_generator(length):
#     res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
#     return res


# no need filename (same as create_input, you can delete it)
def create_trash_input(sut_path, index):
    print("Throwing rubbish")
    cnf = SPECIAL_INPUT[index]
    with open(sut_path + "/tmp.cnf", 'w') as file:
        file.writelines(cnf)


# Read and edit a file
def create_dimacs_input(sut_path, template):
    with open(template, 'r') as t:
        cnf = t.readlines()
        which_p = random.randint(0, 9)
        if which_p < 1:
            cnf[0] = first_line_mutation(cnf[0])
        elif which_p < 7:
            line_i = random.randint(1, len(cnf)-1)
            cnf[line_i] = random_line_mutation(
                cnf[line_i], line_i, int(cnf[0].split(' ')[2]))
        else:
            cnf = generate_random_number_cnf()
    with open(sut_path + "/tmp.cnf", 'w') as file:
        file.writelines(cnf)


# mutate a random line
def random_line_mutation(line, which, bdry):
    print("Mutating line {}".format(which+1))
    digits = line.split(' ')
    if random.randint(0, 1) == 0:
        for i in range(len(digits)):
            if i != len(digits)-1:
                which = random.randint(0, 2)
                if which == 2:
                    digits[i] = str(sys.maxsize+1)
                elif which == 1:
                    digits[i] = str(bdry+1)
                else:
                    digits[i] = string.punctuation[random.randint(0, len(string.punctuation)-1)]
    elif random.randint(0, 1) == 0:
        digits[len(digits)-1] = ''
    else:
        digits[len(digits)-1] = string.punctuation
    return combine(digits)


# mutate the first line
def first_line_mutation(line):
    print("Mutating the first line")
    digits = line.split(' ')
    if random.randint(2,3) == 2:
        if random.randint(0,1) == 1:
            digits[2] = str(int(digits[2])+1)
        else:
            digits[2] = str(int(digits[2])-1)
    else:
        if random.randint(0, 1) == 1:
            digits[3] = str(int(digits[3])+1)
        else:
            digits[3] = str(int(digits[3])-1)
    return combine(digits)


# combine str list to a line
def combine(digits):
    line = ''
    for i in range(len(digits)):
        if i == len(digits) - 1:
            if not len(digits[i]):
                line += '\n'
            elif digits[i][len(digits[i])-1] != '\n':
                line += str(digits[i]) + '\n'
            else:
                line += str(digits[i])
        else:
            line += str(digits[i]) + ' '

    return line


# generate cnf txt with valid format but random number between 5 - 950
def generate_random_number_cnf():
    print("Generating random cnf file")
    variable = random.randint(20, 50)
    clause = random.randint(40, 100)
    txt = ['p cnf ' + str(variable) + " " + str(clause) + '\n']
    percent = random.uniform(0.1, 0.9)
    for _ in range(1, clause):
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


# for testing
# if __name__ == "__main__":
#     with open("./sample.cnf", 'r') as file:
#         cnf = file.readlines()
#         print(cnf[0].split(' ')[2])
#         # cnf[0] = first_line_mutation(cnf[0])
#         # cnf[11] = random_line_mutation(cnf[11], 11, 50)
#
#     with open("./tmp.cnf", 'w') as file:
#         file.writelines(cnf)
