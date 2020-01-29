# mutate the first line
import random
import shutil
import string


def ub_frist_line_mutation(filename):
    from_file = open(filename)
    line = from_file.readline()

    # make any changes to line here
    line = ''
    while True:
        choice = random.randint(0, 9)
        if len(line) >= 20:
            break
        else:
            line += str(choice)

    line += "\n"
    to_file = open(filename, mode="w")
    to_file.write(line)
    shutil.copyfileobj(from_file, to_file)



ub_frist_line_mutation("smaple.cnf");



# generate valid cnf input

def generate_valid_cnf():
    cnf = ''

    return cnf


# generate invalid cnf input
def generate_invalid_cnf():
    cnf = ''
    return cnf