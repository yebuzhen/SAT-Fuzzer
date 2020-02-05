import argparse
import random
import os
from pathlib import Path

UNCHANGED = 'SAT->SAT\nUNSAT->UNSAT\n'
# UN_SAT_UNKNOWN = 'SAT->SAT\nUNSAT->UNKNOWN\n'
SAT_UNKNOWN = 'SAT->UNKNOWN\nUNSAT->UNSAT\n'
ALL_UN_SAT = 'SAT->UNSAT\nUNSAT->UNSAT\n'


# data is list of strings (each represents a line in cnf files)
# return [(data, expect_file_content), (), ...]
def generate_follow_up_tests_and_expectation_files(no_of_var, data):
    result = []
    for i in range(0, 6):
        new_data = swap_between_clauses(data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGED))
    for i in range(6, 12):
        new_data = swap_internal_clauses(data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGED))
    for i in range(12, 18):
        new_data = add_clause(no_of_var, data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(18, 19):
        new_data = add_trivial_sat_clause(no_of_var, data)
        new_data.insert(0, 'p cnf ' + str(no_of_var + 1) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGED))
    for i in range(19, 20):
        new_data = add_trivial_un_sat_clause(no_of_var, data)
        new_data.insert(0, 'p cnf ' + str(no_of_var + 1) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, ALL_UN_SAT))
    for i in range(20, 26):
        new_data = swap_between_clauses(swap_internal_clauses(data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGED))
    for i in range(26, 32):
        new_data = swap_between_clauses(add_clause(no_of_var, data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(32, 38):
        new_data = swap_internal_clauses(add_clause(no_of_var, data))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(38, 44):
        new_data = add_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(44, 47):
        new_data = add_trivial_sat_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, SAT_UNKNOWN))
    for i in range(47, 50):
        new_data = add_trivial_un_sat_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
        new_data.insert(0, 'p cnf ' + str(no_of_var + 1) + ' ' + str(len(new_data)) + '\n')
        result.append((new_data, UNCHANGED))
    return result


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


def add_trivial_sat_clause(no_of_vars, old_data):
    data = old_data.copy()
    new_no_of_vars = no_of_vars + 1
    data.append(str(new_no_of_vars) + ' 0\n')
    return data


def add_trivial_un_sat_clause(no_of_vars, old_data):
    data = old_data.copy()
    new_no_of_vars = no_of_vars + 1
    data.append(str(new_no_of_vars) + ' 0\n')
    data.append('-' + str(new_no_of_vars) + ' 0\n')
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str)
    parser.add_argument("inputs_path", type=str)
    return parser.parse_args()


def execute():
    args = parse_args()

    input_directory = os.fsdecode(args.inputs_path)
    Path(args.inputs_path + '/follow-up-tests').mkdir(parents=True, exist_ok=True)

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
                    cnf, txt = result[i]
                    with open(args.inputs_path + '/follow-up-tests/' + str(basename + '_' + "{0:0=2d}".format(i) + '.cnf'),
                              'w') as output_cnf:
                        output_cnf.writelines(cnf)
                    with open(args.inputs_path + '/follow-up-tests/' + str(basename + '_' + "{0:0=2d}".format(i) + '.txt'),
                              'w') as output_txt:
                        output_txt.writelines(txt)


if __name__ == "__main__":
    execute()
