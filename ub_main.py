import os
import subprocess
import re
import string
import random
import argparse
from shutil import copyfile
from ub_generator import create_input

REGEXES = {
    0: re.compile('^.*runtime error:.+negation'), # INTMIN_NEGATED
    1: re.compile('^.*runtime error:.+null pointer'), # NULLPOINTER
    2: re.compile('^.*runtime error:.+shift'),  # SHIFT_ERROR
    3: re.compile('^.*runtime error:.+signed integer'), # SIGNED_INTEGER_OVERFLOW
    4: re.compile('.*runtime error:'), # OTHER_ERROE

    5: re.compile('^==.*AddressSanitizer: heap-use-after-free'), # USE_AFTER_FREE
    6: re.compile('^==.*AddressSanitizer: heap-buffer-overflow'), # HEAP_BUFFER_OVERFLOW
    7: re.compile('^==.*AddressSanitizer: stack-buffer-overflow'), # STACK_BUFFER_OVERFLOW
    8: re.compile('^==.*AddressSanitizer: global-buffer-overflow'), # GLOBAL_BUFFER_OVERFLOW
    9: re.compile('^==.*AddressSanitizer: stack-use-after-return'), # USE_AFTER_RETURN
    10: re.compile('^==.*AddressSanitizer: stack-use-after-scope'), # USE_AFTER_SCOPE
    11: re.compile('^==.*AddressSanitizer: initialization-order-fiasco'), # INITIALIZATION_ORDER_BUGS
    12: re.compile('^==.*LeakSanitizer: detected memory leaks'), # MEMORY_LEAKS

    13: re.compile('^==.*UndefinedBehaviorSanitizer'), # UB_ERROR
}

NUM_ERRORS = 14
NUM_TS = 20
ubts_buffer = []
ub_counters = []

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("Inputs_path", type=str,
        help="Path to folder containing input DIMACS-format tests.")
    return parser.parse_args()

def eval_case(error_log):
    cur_status = [0] * NUM_ERRORS
    cur_counter = [0, 0] # extra "bit" 0 for duplication
    for line in error_log.decode('ascii').split('\n'):
        for index, regexp in REGEXES.items():
            if regexp.match(line):
                cur_status[index] = 1
                cur_counter[0] += 1

    try:
        dup_index = ubts_buffer.index(cur_status)
        if len(ubts_buffer) < NUM_TS:
            ubts_buffer.append(cur_status)
            ub_counters.append(cur_counter)
            return len(ubts_buffer) - 1
        else:
            if ub_counters[dup_index][0] < cur_counter[0]:
                ubts_buffer[dup_index] = cur_status
                ub_counters[dup_index] = cur_counter
                return dup_index
            else:
                return -1
    except ValueError as _:
        cur_counter[1] = 1
        if len(ubts_buffer) < NUM_TS:
            ubts_buffer.append(cur_status)
            ub_counters.append(cur_counter)
            return len(ubts_buffer) - 1
        else:
            for case_i in ub_counters:
                if not case_i[1]:
                    ubts_buffer[case_i] = cur_status
                    ub_counters[case_i] = cur_counter
                    return case_i
                else:
                    continue
            print("Missing one unique case!")
            return -1

    return -1

def execute():
    args = ParseArgs()
    RUN_PATH = args.SUT_path + "/runsat.sh"
    INUPT_PATH = args.SUT_path + "/tmp.cnf"
    CASE_PATH = args.SUT_path + "/fuzzed-tests"
    ERR_PATH = args.SUT_path + "/fuzzed-tests-logs"
    OUTPUT_PATH = args.SUT_path + "/fuzzed-tests-outputs"

    if not os.path.exists(CASE_PATH):
        os.mkdir(CASE_PATH)
    if not os.path.exists(ERR_PATH):
        os.mkdir(ERR_PATH)
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    for i in range(100):
        print("Iteration{}".format(i))
        create_input(args.Inputs_path + "/bench_13462.smt2.cnf", args.SUT_path)
        task = subprocess.Popen([RUN_PATH, INUPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  cwd=args.SUT_path)

        try:
            t_output, t_error = task.communicate(timeout=20)
        except subprocess.TimeoutExpired:
            task.kill()
            t_output, t_error = task.communicate()

        # os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
        #           "/tmp.cnf " + "> " + args.SUT_path + "/tmp.log 2>&1")

        flag = eval_case(t_error)
        if flag:
            print("Replacing Case ", flag)
            copyfile(INUPT_PATH, CASE_PATH+"/test_case{}".format(flag))
            with open(ERR_PATH+"/test_log{}".format(flag), 'w') as f:
                f.writelines(t_error.decode('ascii'))
            with open(OUTPUT_PATH+"/test_output{}".format(flag), 'w') as f:
                f.writelines(t_output.decode('ascii'))

        # os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
        #           "/tmp.cnf " + "> " + args.SUT_path + "/fuzzed-tests/test_log{} 2>&1".format(i))

if __name__ == "__main__":
    execute()
