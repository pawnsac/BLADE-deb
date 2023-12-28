.PHONY: all clean test-1 test-2

all:
	@echo  "Usage: make -f test.mk test-[1,2]"

clean:
	rm -rf target-program/* processing

test-1:
	mkdir -p target-program 
	rm -f target-program/*
	cp ../test/test1.c target-program
	cp ../test/test_oracle_1.sh target-program
	python3 blade.py -p test1.c -t test_oracle_1.sh -u 3 -d 3 

test-2: 
	mkdir -p target-program
	rm -f target-program/*
	cp ../test/test2.c target-program
	cp ../test/test_oracle_2.sh target-program
	python3 blade.py -p test2.c -t test_oracle_2.sh -u 3 -d 3 