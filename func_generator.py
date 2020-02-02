import random

UNCHANGE = 'SAT->SAT\nUNSAT->UNSAT\n'
UNSAT_UNKNOWN = 'SAT->SAT\nUNSAT->UNKNOWN\n'
SAT_UNKNOWN = 'SAT->UNKNOWN\nUNSAT->UNSAT\n'


# data is list of strings (each represents a line in cnf files)
# return [(data, no_of_var, no_of_clauses, expect_file_content), (), ...]
def generate_follow_up_tests_and_expectation_files(no_of_var, data):
    result = []
    for i in range(0, 3):
        new_data = swap_between_clauses(data)
        result.append((new_data, no_of_var, len(new_data), UNCHANGE))
    for i in range(4, 7):
        new_data = swap_internal_clauses(data)
        result.append((new_data, no_of_var, len(new_data), UNCHANGE))
    for i in range(8, 11):
        new_data = add_clause(no_of_var, data)
        result.append((new_data, no_of_var, len(new_data), SAT_UNKNOWN))
    for i in range(12, 15):
        new_data = delete_clause(data)
        result.append((new_data, no_of_var, len(new_data), UNSAT_UNKNOWN))
    for i in range(16, 19):
        new_data = swap_between_clauses(swap_internal_clauses(data))
        result.append((new_data, no_of_var, len(new_data), UNCHANGE))
    for i in range(20, 23):
        new_data = add_clause(no_of_var, swap_between_clauses(data))
        result.append((new_data, no_of_var, len(new_data), SAT_UNKNOWN))
    for i in range(24, 27):
        new_data = delete_clause(swap_between_clauses(data))
        result.append((new_data, no_of_var, len(new_data), UNSAT_UNKNOWN))
    for i in range(28, 31):
        new_data = add_clause(no_of_var, swap_internal_clauses(data))
        result.append((new_data, no_of_var, len(new_data), SAT_UNKNOWN))
    for i in range(32, 35):
        new_data = delete_clause(swap_internal_clauses(data))
        result.append((new_data, no_of_var, len(new_data), UNSAT_UNKNOWN))
    for i in range(36, 42):
        new_data = add_clause(no_of_var, swap_internal_clauses(swap_between_clauses(data)))
        result.append((new_data, no_of_var, len(new_data), SAT_UNKNOWN))
    for i in range(43, 49):
        new_data = delete_clause(swap_internal_clauses(swap_between_clauses(data)))
        result.append((new_data, no_of_var, len(new_data), UNSAT_UNKNOWN))


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


