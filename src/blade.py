from context_builder import parse_container, reset_global_storage
from reduction import Reduction
from writer import write
import clang.cindex
import time
from pprint import pprint
import sys
import os
from make_dir_duplicates import copy_dir, rm_dir, copy_target_program
from get_targets import get_targets

try:
    file_name = sys.argv[1]
    test_command = sys.argv[2]
    n_max = sys.argv[3]
    back_max = sys.argv[4]
except:
    print(
        "Usage: python3 blade [input_file.c] [oracle] [MAX_PROCESSES_UPWARDS] [MAX_PROCESSES_DOWNARDS]"
    )
    sys.exit(1)


def main(file_name, test_command, n_max, back_max):

    f_n = os.path.join("target-program", file_name)
    test_oracle_file=os.path.join("target-program", test_command)
    os.system(f'chmod +x {test_oracle_file}') ## setting executable permission for the test oracle

    rm_dir()
    copy_target_program()
    copy_dir(n_max, back_max)

    index = clang.cindex.Index.create()
    translation_unit = index.parse(f_n)
    file = open(f_n, "r+").read().split("\n")
    test_file = sys.argv[2]
    last_fit = file.copy()
    time_final = time.time()
    print(f"Building Statement tree of {file_name}")
    token_map = parse_container(translation_unit.cursor)
    print("Done")
    deb_run = 1
    while True:
        print("Reduction Starting")
        reduction = Reduction(last_fit, test_command, file_name, n_max, back_max)
        reduction.start_progress(len(last_fit))
        print(f"[Debloating Iteration: {deb_run}]\n")
        reduction.reduction(token_map)
        last_fit = reduction.last_fit
        index = clang.cindex.Index.create()
        outfile = file_name + ".blade.c"
        write(last_fit, outfile)
        clang_format_command = f"clang-format -i {outfile}"
        os.system(clang_format_command)
        reduction.clear_screen()
        deb_run += 1
        break
        ## limited to 1 interation for now.
        ## to-do: think about adding an option to extend to multiple iterations.

    time_final = time.time() - time_final
    time_final = round(time_final,2)
    print(f"Debloated file saved as: {outfile}")
    print(f"Time taken: {time_final}s")


if __name__ == "__main__":
    main(file_name, test_command, n_max, back_max)
