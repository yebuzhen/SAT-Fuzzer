import os
import subprocess
import re
import string
import random
import argparse
from shutil import copyfile
from ub_generator import create_trash_input, create_dimacs_input

REGEXES = {
    0: re.compile('^.*runtime error:.+negation'), # INTMIN_NEGATED
    1: re.compile('^.*runtime error:.+null pointer'), # NULLPOINTER
    2: re.compile('^.*runtime error:.+shift'),  # SHIFT_ERROR
    3: re.compile('^.*runtime error:.+integer'), # INTEGER_OVERFLOW
    4: re.compile('.*runtime error:'), # OTHER_ERROE

    5: re.compile('^==.*AddressSanitizer: heap-use-after-free'), # USE_AFTER_FREE
    6: re.compile('^==.*AddressSanitizer: heap-buffer-overflow'), # HEAP_BUFFER_OVERFLOW
    7: re.compile('^==.*AddressSanitizer: stack-buffer-overflow'), # STACK_BUFFER_OVERFLOW
    8: re.compile('^==.*AddressSanitizer: global-buffer-overflow'), # GLOBAL_BUFFER_OVERFLOW
    9: re.compile('^==.*AddressSanitizer: stack-use-after-return'), # USE_AFTER_RETURN
    10: re.compile('^==.*AddressSanitizer: stack-use-after-scope'), # USE_AFTER_SCOPE
    11: re.compile('^==.*AddressSanitizer failed to'), # for overflowed integers
    12: re.compile('^==.*LeakSanitizer: detected memory leaks'), # MEMORY_LEAKS

    13: re.compile('^==.*UndefinedBehaviorSanitizer'), # UB_ERROR
}

NUM_ERRORS = 14
NUM_TS = 20
ubts_buffer = []
ub_counters = []

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_PATH",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("TPLTS_PATH", type=str,
        help="Path to a directory containing a non-empty set of well-fromed DIMACS-format files")
    return parser.parse_args()

def eval_case(error_log):
    print("Start evaluation")
    cur_status = [0] * NUM_ERRORS
    cur_counter = [0, 0] # extra "bit" 0 for duplication
    for line in error_log.decode('ascii').split('\n'):
        for index, regexp in REGEXES.items():
            if regexp.match(line):
                cur_status[index] = 1
                cur_counter[0] += 1

    if cur_status == [0] * NUM_ERRORS:
        print("No error info logged")
        return -1

    try:
        dup_indices = [i for i, x in enumerate(ubts_buffer) if x == cur_status]
        if len(ubts_buffer) < NUM_TS:
            ubts_buffer.append(cur_status)
            ub_counters.append(cur_counter)
            return len(ubts_buffer) - 1
        else:
            for i in dup_indices:
                if ub_counters[i][0] < cur_counter[0]:
                    ubts_buffer[i] = cur_status
                    if len(dup_indices) == 1:
                        cur_counter[1] = 1
                    ub_counters[i] = cur_counter
                    return i
                else:
                    return -1
    except ValueError as _:
        cur_counter[1] = 1
        if len(ubts_buffer) < NUM_TS:
            ubts_buffer.append(cur_status)
            ub_counters.append(cur_counter)
            return len(ubts_buffer) - 1
        else:
            for i in range(NUM_TS):
                if not ub_counters[i][1]:
                    ubts_buffer[i] = cur_status
                    ub_counters[i] = cur_counter
                    return i
                else:
                    continue
            print("Missing one unique case!")
            return -1

    return -1

def execute():
    args = ParseArgs()
    RUN_PATH = args.SUT_PATH + "/runsat.sh"
    INUPT_PATH = args.SUT_PATH + "/tmp.cnf"
    CASE_PATH = args.SUT_PATH + "/fuzzed-tests"
    ERR_PATH = args.SUT_PATH + "/fuzzed-tests-logs"
    OUTPUT_PATH = args.SUT_PATH + "/fuzzed-tests-outputs"

    if not os.path.exists(CASE_PATH):
        os.mkdir(CASE_PATH)
    if not os.path.exists(ERR_PATH):
        os.mkdir(ERR_PATH)
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    ctr = 0
    while True:
        print("\nIteration{}".format(ctr))
        if ctr < 7:
            create_trash_input(args.SUT_PATH, ctr)
        else:
            tplt_file = random.choice(os.listdir(args.TPLTS_PATH))
            print("Using {} as the base to mutate".format(tplt_file))
            create_dimacs_input(args.SUT_PATH, args.TPLTS_PATH+'/'+tplt_file)
        task = subprocess.Popen([RUN_PATH, INUPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  cwd=args.SUT_PATH)

        try:
            print("SUT is running")
            t_output, t_error = task.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            task.kill()
            print("SUT process killed")
            ctr += 1
            continue

        # os.system(args.SUT_PATH + "/runsat.sh " + args.SUT_PATH +
        #           "/tmp.cnf " + "> " + args.SUT_PATH + "/tmp.log 2>&1")

        flag = eval_case(t_error)
        if flag >= 0:
            print("Replacing Case ", flag)
            copyfile(INUPT_PATH, CASE_PATH+"/test_case{}".format(flag))
            try:
                with open(ERR_PATH+"/test_log{}".format(flag), 'w') as f:
                    f.writelines(t_error.decode('ascii'))
                with open(OUTPUT_PATH+"/test_output{}".format(flag), 'w') as f:
                    f.writelines(t_output.decode('ascii'))
            except UnicodeDecodeError as _:
                pass

        # os.system(args.SUT_PATH + "/runsat.sh " + args.SUT_PATH +
        #           "/tmp.cnf " + "> " + args.SUT_PATH + "/fuzzed-tests/test_log{} 2>&1".format(i))

        ctr += 1

if __name__ == "__main__":
    execute()
