#!/bin/bash

DEB_TARGET=test1.c
RED_BIN=deb-1
LOG=log.tx

rm -rf $RED_BIN temp* $LOG

clang -w $DEB_TARGET -o $RED_BIN || exit 1
{ timeout -k 0.3 0.3 ./$RED_BIN >& temp1 ; } || exit 1
echo -n "HELLO WORLD" >& temp2
diff temp2 temp1  || exit 1

rm -rf $RED_BIN temp* $LOG

exit 0