import argparse
import random
import os

UNCHANGE = 'SAT->SAT\nUNSAT->UNSAT\n'
UNSAT_UNKNOWN = 'SAT->SAT\nUNSAT->UNKNOWN\n'
SAT_UNKNOWN = 'SAT->UNKNOWN\nUNSAT->UNSAT\n'


# data is list of strings (each represents a line in cnf files)
# return [(data, expect_file_content), (), ...]
def generate_follow_up_tests_and_expectation_files(no_of_var, data):
    result = []
    for i in range(0, 7):
        new_data = swap_between_clauses(data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGE))
    for i in range(7, 14):
        new_data = swap_internal_clauses(data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGE))
    for i in range(14, 21):
        new_data = add_clause(no_of_var, data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(21, 28):
        new_data = swap_between_clauses(swap_internal_clauses(data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGE))
    for i in range(28, 35):
        new_data = add_clause(no_of_var, swap_between_clauses(data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(35, 42):
        new_data = add_clause(no_of_var, swap_internal_clauses(data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(42, 50):
        new_data = add_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))

    return result


def add_line_separator(data):
    for i in range(len(data)):
        data[i] += '\n'
    return data


def swap_between_clauses(old_data):
    data = old_data.copy()
    random.shuffle(data)
    return data


def swap_internal_clauses(old_data):
    data = old_data.copy()
    for i in range(0, len(data)):
        data[i] = data[i][0: len(data[i]) - 1]
        split_line = data[i].split()
        length = len(split_line)
        if split_line[length - 1] == '0':
            split_line = split_line[0: length - 1]
            random.shuffle(split_line)
            split_line.append('0')
        else:
            random.shuffle(split_line)
        data[i] = combine(split_line) + '\n'
    return data


def combine(split_line):
    line = ''
    for split_num in split_line:
        line += split_num + ' '
    return line[0: len(line) - 1]


def add_clause(no_of_vars, old_data):
    data = old_data.copy()
    no_of_new_clauses = random.randint(1, 100)

    # Number of clauses
    for i in range(no_of_new_clauses):
        line = ''
        # Number of vars in a line
        for _ in range(random.randint(1, 100)):
            if random.randint(0, 1) == 1:
                line += '-'
            # Choose one var
            line = line + str(random.randint(1, no_of_vars)) + ' '
        line += '0\n'
        data.append(line)

    return data


# def delete_clause(old_data):
#     data = old_data.copy()
#     no_of_clauses = len(data)
#     times = random.randint(0, no_of_clauses - 1)
#
#     for _ in range(times):
#         del data[random.randint(0, len(data) - 1)]
#
#     return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs_path",  type=str)
    parser.add_argument("outputs_path", type=str)
    return parser.parse_args()


def execute():
    args = parse_args()

    input_directory = os.fsdecode(args.inputs_path)

    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)
        if filename.endswith(".cnf"):
            print(filename)
            with open(input_directory + '/' + filename, 'r') as target_file:
                basename = filename[:-4]
                data = target_file.readlines()
                strings = data[0].split(' ')
                no_of_var = int(strings[2])
                del data[0]
                result = generate_follow_up_tests_and_expectation_files(no_of_var, data)
                for i in range(50):
                    x, y = result[i]
                    with open(args.outputs_path + '/' + str(basename + '_' + "{0:0=2d}".format(i) + '.cnf'),
                              'w') as output_cnf:
                        output_cnf.writelines(x)
                    with open(args.outputs_path + '/' + str(basename + '_' + "{0:0=2d}".format(i) + '.txt'),
                              'w') as output_txt:
                        output_txt.writelines(y)


if __name__ == "__main__":
    execute()
