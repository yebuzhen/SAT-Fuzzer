import os
import subprocess
import re
import string
import random
import argparse
from shutil import copyfile
from ub_generator import create_input

REGEXES = {
    "INTMIN_NEGATED": re.compile('^.*runtime error:.+negation'),
    "NULLPOINTER": re.compile('^.*runtime error:.+null pointer'),
    "SHIFT_ERROR": re.compile('^.*runtime error:.+shift'),
    "SIGNED_INTEGER_OVERFLOW": re.compile('^.*runtime error:.+signed integer'),
    "OTHER_ERROE": re.compile('.*runtime error:'),

    "USE_AFTER_FREE": re.compile('^==.*AddressSanitizer: heap-use-after-free'),
    "HEAP_BUFFER_OVERFLOW": re.compile('^==.*AddressSanitizer: heap-buffer-overflow'),
    "STACK_BUFFER_OVERFLOW": re.compile('^==.*AddressSanitizer: stack-buffer-overflow'),
    "GLOBAL_BUFFER_OVERFLOW": re.compile('^==.*AddressSanitizer: global-buffer-overflow'),
    "USE_AFTER_RETURN": re.compile('^==.*AddressSanitizer: stack-use-after-return'),
    "USE_AFTER_SCOPE": re.compile('^==.*AddressSanitizer: stack-use-after-scope'),
    "INITIALIZATION_ORDER_BUGS": re.compile('^==.*AddressSanitizer: initialization-order-fiasco'),
    "MEMORY_LEAKS": re.compile('^==.*LeakSanitizer: detected memory leaks'),

    "UB_ERROR": re.compile('^==.*UndefinedBehaviorSanitizer'),
}

NUM_TS = 20
ubts_buffer = []

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("Inputs_path", type=str,
        help="Path to folder containing input DIMACS-format tests.")
    return parser.parse_args()

def eval_case(logfile):
    with open(logfile, 'r') as f:
        pass

def execute():
    args = ParseArgs()
    RUN_PATH = args.SUT_path + "/runsat.sh"
    INUPT_PATH = args.SUT_path + "/tmp.cnf"
    OUTPUT_PATH = args.SUT_path + "/fuzzed-tests"

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    for i in range(20):
        print("Iteration{}".format(i))
        create_input(args.Inputs_path + "/bench_13462.smt2.cnf", args.SUT_path)
        task = subprocess.Popen([RUN_PATH, INUPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  cwd=args.SUT_path)

        try:
            t_output, t_error = task.communicate(timeout=100)
        except subprocess.TimeoutExpired:
            task.kill()
            t_output, t_error = task.communicate()

        with open(OUTPUT_PATH+"/test_log{}".format(1), 'w') as file:
            file.writelines(t_error.decode('ascii ').split('\n'))
        # os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
        #           "/tmp.cnf " + "> " + args.SUT_path + "/tmp.log 2>&1")
        if eval_case(args.SUT_path + "/tmp.log"):
            # copyfile
            pass
        # os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
        #           "/tmp.cnf " + "> " + args.SUT_path + "/fuzzed-tests/test_log{} 2>&1".format(i))

if __name__ == "__main__":
    execute()
