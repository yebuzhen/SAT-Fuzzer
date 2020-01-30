import random


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


print(swap_internal_clauses(['1 2 3 0', '4 5 6']))
print(swap_between_clauses(['1 2 3 0', '4 5 6']))


def add_clause():
    print()


def add_clause(no_of_vars, data):
    no_of_clauses = len(data)
    no_of_new_clauses = random.randint(1, no_of_clauses)

    for i in range(0, no_of_new_clauses):
        line = ''
        for _ in range(0, random.randint(1, no_of_vars)):
            if random.randint(0,1) == 1:
                line += '-'
            line = line + str(random.randint(1, no_of_vars)) + ' '
        line += '0'
        data.append(line)
    
    return data


def delete_clause(data):
    no_of_clauses = len(data)

    for _ in range(0, no_of_clauses):
        del data[random.randint(0, len(data) - 1)]

    return data