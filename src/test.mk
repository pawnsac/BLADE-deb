.PHONY: all clean test-1 test-2

all:
	@echo  "Usage: make -f test-[1,2]"

clean:
	rm -rf target-program/* processing

test-1: 
	rm -f target-program/*
	cp ../test/test1.c target-program
	cp ../test/test_oracle_1.sh target-program
	python3 blade.py test1.c test_oracle_1.sh 3 3 

test-2: 
	rm -f target-program/*
	cp ../test/test2.c target-program
	cp ../test/test_oracle_2.sh target-program
	python3 blade.py test2.c test_oracle_2.sh 3 3 