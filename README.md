# Blade - Fast Source Code Debloating Framework

Blade uses clang under the hood to build a statement tree and performs deblaoting on c files. Based on the test oracle and the input file, it returns a minimal subset of the code.


## Instructions for Target Program

Your program must be present in the **src/target-program** folder. It must contain a target c file and a test oracle. Each oracle file (i-e oracle.sh) must be returning 0 on a successful run. The MAX_UPWARD_PROCESSESS and MAX_DOWNWARD_PROCESSESS denote the parallel processing allocations given to Blade's upward and downwards iterators.

Inside the *src* folder, run:

    python3 blade.py [target_file.c] [oracle_file] [MAX_UPWARD_PROCESSESS] [MAX_DOWNWARD_PROCESSESS]

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

#### Blade is a research prototype under GNU General Public License 3.0

Copyright © 2023 Blade

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License 3.0 for more details.

You should have received a copy of the GNU General Public License 3.0
along with this program. If not, see
<https://www.gnu.org/licenses/gpl-3.0.html>.
