import subprocess


def run_test_case(input_cmd, cwd):
    try:
        process = subprocess.Popen(
            input_cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd
        )
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        return exit_code
    except Exception as e:
        return 1
