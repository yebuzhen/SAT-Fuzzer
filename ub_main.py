import os
import string
import random
import argparse
from ub_generator import *

def RandomStringGenerator(length):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))
    return res

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("Inputs_path", type=str,
        help="Path to folder containing input DIMACS-format tests.")
    return parser.parse_args()

def execute():
    args = ParseArgs()
    NUM_TS = 20
    ubts_buffer = []
    os.makedirs(args.SUT_path+"/fuzzed-tests", exist_ok=True)

    for i in range(NUM_TS):
        print("iteration{}".format(i))
        modify_file(args.Inputs_path + "/bench_13462.smt2.cnf", args.SUT_path)
        os.system(args.SUT_path + "/runsat.sh " + args.SUT_path +
                  "/tmp.cnf " + "> " + args.SUT_path + "/fuzzed-tests/test_log{} 2>&1".format(i))

if __name__ == "__main__":
    execute()
