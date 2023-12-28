import os
import shutil
import sys
from pathlib import Path

def is_valid_path(path):
    if not Path(path).exists():
        print(f"Input path: '{path}' not valid")
        sys.exit(1)
    return path

def copy_target_program():
    src_dir = 'target-program'
    dest_dir = 'processing/1'
    dest_dir_downwards = 'processing/_1'

    try:
        target_dir_len=len(os.listdir(src_dir))
        if target_dir_len<2: ## must include test oracle and a c file
            print("No target program found")
            sys.exit(1)
    except:
        print("No target program found")
        sys.exit(1)
    shutil.copytree(src_dir, dest_dir)
    shutil.copytree(src_dir, dest_dir_downwards)

def copy_dir(n, b):
    for i in range(int(n) - 1):
        os.system(f"cp processing/1 processing/{i+2} -r")
    for i in range(int(b) - 1):
        os.system(f"cp processing/1 processing/_{i+2} -r")


def rm_dir():
    os.system(f"rm -rf processing")
    # for i in range(200):
    #     os.system(f"rm -rf processing/{i+2}")
    #     os.system(f"rm -rf processing/_{i+2}")
