import sys
from subprocess import PIPE, run
import subprocess
import os
import pprint

def get_targets(make_cmd,CC):
    target_files=[]
    trace_cmd='--trace'
    clean='clean'
    full_cmd=make_cmd+' '+trace_cmd
    os.system(f'{make_cmd} {clean}')
    trace_output = run(full_cmd.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
    trace_output=trace_output.stdout.split('\n')
    for cmd in trace_output:
        if cmd.startswith(CC):
            targets=cmd.split()
            for target in targets:
                if target.endswith('.c'):
                    target_files.append(os.getcwd()+'/'+target)
                    break
    return target_files
