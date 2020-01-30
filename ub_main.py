import os
import re
import string
import random
import argparse
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

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("Inputs_path", type=str,
        help="Path to folder containing input DIMACS-format tests.")
    return parser.parse_args()

def eval_case():
    pass

def execute():
    args = ParseArgs()
    NUM_TS = 20
    ubts_buffer = []

    if not os.path.exists(args.SUT_path+"/fuzzed-tests"):
        os.mkdir(args.SUT_path+"/fuzzed-tests")

    for i in range(NUM_TS):
        print("iteration{}".format(i))
        create_input(args.Inputs_path + "/bench_13462.smt2.cnf", args.SUT_path)
        os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
                  "/tmp.cnf " + "> " + args.SUT_path + "/tmp.log 2>&1")
        # os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
        #           "/tmp.cnf " + "> " + args.SUT_path + "/fuzzed-tests/test_log{} 2>&1".format(i))

if __name__ == "__main__":
    execute()
