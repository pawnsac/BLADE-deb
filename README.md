# Blade - Fast Source Code Debloating Framework

Blade uses clang under the hood to build a statement tree and performs deblaoting on c files. Based on the test oracle and the input file, it returns a minimal subset of the code.


## Instructions for Target Program

Your program must be present in the **src/target-program** folder. It must contain a target c file and a test oracle. Each oracle file (i-e oracle.sh) must be returning 0 on a successful run. The MAX_UPWARD_PROCESSESS and MAX_DOWNWARD_PROCESSESS denote the parallel processing allocations given to Blade's upward and downwards iterators.

Inside the *src* folder, run:

    python3 blade.py -p [target-program/target_file.c] -t [target-program/oracle_file] -u [MAX_UPWARD_PROCESSESS] -d [MAX_DOWNWARD_PROCESSESS]

## Test Programs

To run Blade on the two test programs attached, use the following commands
 inside the *src* folder:

    make -f test.mk test-1
    make -f test.mk test-2

## Requirements
Install the python requirements given in requirements.txt. 

Note: You need to configure the path of clang's object properly for python3. If you run into a similar error regarding the path, see the resolution given in this <a href="https://github.com/mapbox/cncc/issues/6">**link**</a> .
 

Additional linux requirements:

- clang-14
- clang-format
- astyle
## Prorotype Limits
- Works on single c file programs for now.
- Only C99 code tested so far.

## Disclaimer

#### Blade is a research prototype under MIT License

MIT License

Copyright (c) 2023 Blade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
