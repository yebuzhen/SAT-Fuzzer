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
    for i in range(0, 1):
        new_data = swap_between_clauses(data)
        new_data.insert(0, 'p cnf ' + str(no_of_var) + ' ' + str(len(new_data)))
        result.append((new_data, UNCHANGE))
    # for i in range(4, 7):
    #     new_data = swap_internal_clauses(data)
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNCHANGE))
    # for i in range(8, 11):
    #     new_data = add_clause(no_of_var, data)
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, SAT_UNKNOWN))
    # for i in range(12, 15):
    #     new_data = delete_clause(data)
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNSAT_UNKNOWN))
    # for i in range(16, 19):
    #     new_data = swap_between_clauses(swap_internal_clauses(data))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNCHANGE))
    # for i in range(20, 23):
    #     new_data = add_clause(no_of_var, swap_between_clauses(data))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, SAT_UNKNOWN))
    # for i in range(24, 27):
    #     new_data = delete_clause(swap_between_clauses(data))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNSAT_UNKNOWN))
    # for i in range(28, 31):
    #     new_data = add_clause(no_of_var, swap_internal_clauses(data))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, SAT_UNKNOWN))
    # for i in range(32, 35):
    #     new_data = delete_clause(swap_internal_clauses(data))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNSAT_UNKNOWN))
    # for i in range(36, 42):
    #     new_data = add_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, SAT_UNKNOWN))
    # for i in range(43, 49):
    #     new_data = delete_clause(swap_internal_clauses(swap_between_clauses(data)))
    #     final_data = ['p cnf ' + str(no_of_var) + ' ' + str(len(new_data)), new_data]
    #     result.append((final_data, UNSAT_UNKNOWN))

    return result


def add_line_separator(data):
    for i in range(len(data)):
        data[i] += '\n'
    return data


def swap_between_clauses(data):
    random.shuffle(data)
    return data


def swap_internal_clauses(data):
    for i in range(0, len(data)):
        split_line = data[i].split()
        length = len(split_line)
        if split_line[length - 1] == '0':
            split_line = split_line[0: length - 1]
            random.shuffle(split_line)
            split_line.append('0')
        else:
            random.shuffle(split_line)
        data[i] = combine(split_line)
    return data


def combine(split_line):
    line = ''
    for split_num in split_line:
        line += split_num + ' '
    return line[0 : len(line) - 1]


def add_clause(no_of_vars, data):
    no_of_clauses = len(data)
    no_of_new_clauses = random.randint(1, no_of_clauses)

    # Number of clauses
    for i in range(0, no_of_new_clauses):
        line = ''
        # Number of vars in a line
        for _ in range(0, random.randint(1, no_of_vars)):
            if random.randint(0, 1) == 1:
                line += '-'
            # Choose one var
            line = line + str(random.randint(1, no_of_vars)) + ' '
        line += '0'
        data.append(line)

    return data


def delete_clause(data):
    no_of_clauses = len(data)

    for _ in range(0, no_of_clauses):
        del data[random.randint(0, len(data) - 1)]

    return data


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
                for i in range(1):
                    with open(args.outputs_path + '/' + str(basename + '_' + "{0:0=2d}".format(i) + '.cnf'),
                              'w') as output_cnf:
                        x, y = result[i]
                        output_cnf.writelines(x)
                    with open(args.outputs_path + '/' + str(basename + '_' + "{0:0=2d}".format(i) + '.txt'),
                              'w') as output_txt:
                        output_txt.writelines(y)


if __name__ == "__main__":
    execute()
