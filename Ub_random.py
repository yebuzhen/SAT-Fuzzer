import subprocess
import string
import random
import argparse

def StringGenerator(length):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))
    return res

def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("SUT_path",  type=str,
        help="Path to binary containing the system under test.")
    parser.add_argument("inputs_path", type=str,
        help="Path to folder containing input DIMACS-format tests.")
    return parser.parse_args()

if __name__ == "__main__":
    args = ParseArgs()

    f = open("test.cnf", "w+")
    f.write(StringGenerator(10))
    f.close

    subprocess.run(["./runsat.sh", "test.cnf"])
