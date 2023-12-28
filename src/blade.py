## Importing Modules
import clang.cindex
import time
import argparse
import sys
import os
from make_dir_duplicates import copy_dir, rm_dir, copy_target_program, get_file_name
from context_builder import parse_container
from reduction import Reduction
from process import run_test_case
from writer import write


def cmd_line_invocation():
    # Code to fetch the command line arguments
    desc_text = """The following are the arguments needed for blade's debloating."""
    parser = argparse.ArgumentParser(description=desc_text)
    parser.add_argument(
        "-p",
        "--path-to-file",
        type=str,
        required=True,
        help="Input path to C program.",
    )
    parser.add_argument(
        "-t",
        "--path-to-test-oracle",
        type=str,
        required=True,
        help="Input path to test oracle.",
    )
    parser.add_argument(
        "-u",
        "--max_precesses_upwards",
        type=int,
        required=False,
        default=10,
        help="Input the number of upward processes that denote the upward debloating iterators.",
    )
    parser.add_argument(
        "-d",
        "--max_precesses_downwards",
        type=int,
        required=False,
        default=10,
        help="Input the number of downward processes that denote the downward debloating iterators.",
    )
    args = parser.parse_args()
    return args

# Driver code below

def main():

    # parsing command line args
    args = cmd_line_invocation()
    c_program_path = args.path_to_file
    test_oracle_path = args.path_to_test_oracle
    u_processes = args.max_precesses_upwards
    d_processes = args.max_precesses_downwards

    ## checking if programs paths paths exists and getting the base name
    c_program = get_file_name(c_program_path)
    test_oracle_file = get_file_name(test_oracle_path)


    # setting executable permission for the test oracle
    os.system(f'chmod +x {test_oracle_path}')
    # preprocess cfile for statement tree builder
    os.system(f'bash preprocess_cfile.sh {c_program_path}')

    # checking if initial oracle file in the target-program dir
    # returns 0 (successful run)
    if not (run_test_case(f'bash {test_oracle_file}', 'target-program') == 0 ):
        print("Oracle test script execution failed.")
        sys.exit(1)

    print(f"Input C program: {c_program} |", f"Oracle test file: {test_oracle_file}")

    # processing dirs for debloating process
    rm_dir()
    copy_target_program()
    copy_dir(u_processes, d_processes)

    # parsing the C file to build the statement tree
    index = clang.cindex.Index.create()
    translation_unit = index.parse(c_program_path)
    file = open(c_program_path, "r+").read().split("\n")
    test_file = sys.argv[2]
    last_fit = file.copy()
    time_final = time.time()
    print(f"Building Statement tree of {c_program}")
    token_map = parse_container(translation_unit.cursor)
    print("Done")
    deb_run = 1

    # Debloating process driver code
    while True:
        print("Reduction Starting")
        reduction = Reduction(last_fit, test_oracle_file,
                              c_program, u_processes, d_processes)
        reduction.start_progress(len(last_fit))
        print(f"[Debloating Iteration: {deb_run}]\n")
        reduction.reduction(token_map)
        last_fit = reduction.last_fit
        index = clang.cindex.Index.create()
        outfile = c_program + ".blade.c"
        write(last_fit, outfile)
        clang_format_command = f"clang-format -i {outfile}"
        os.system(clang_format_command)
        reduction.clear_screen()
        deb_run += 1
        break
        # limited to 1 interation for now.
        # to-do: think about adding an option to extend to multiple iterations.

    time_final = time.time() - time_final
    time_final = round(time_final, 2)
    print(f"Debloated file saved as: {outfile}")
    print(f"Time taken: {time_final}s")


if __name__ == "__main__":
    main()
