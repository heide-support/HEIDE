HELIB_SRC=../HElib/src
CC = g++
CFLAGS = -g -O2 -Wfatal-errors -Wshadow -Wall -I/usr/local/include -I$(HELIB_SRC)
LD = g++
LDLIBS = -L/usr/local/lib -lntl -lgmp -lm $(HELIB_SRC)/fhe.a
AR = ar
ARFLAGS = ruv


HEADER = BGV_HE.h
SRC = BGV_HE.cpp
OBJ = BGV_HE.o 
HELIB_OBJ = $(HELIB_SRC)/NumbTh.o $(HELIB_SRC)/timing.o $(HELIB_SRC)/bluestein.o $(HELIB_SRC)/PAlgebra.o  $(HELIB_SRC)/CModulus.o $(HELIB_SRC)/FHEContext.o $(HELIB_SRC)/IndexSet.o $(HELIB_SRC)/DoubleCRT.o $(HELIB_SRC)/FHE.o $(HELIB_SRC)/KeySwitching.o $(HELIB_SRC)/Ctxt.o $(HELIB_SRC)/EncryptedArray.o $(HELIB_SRC)/replicate.o $(HELIB_SRC)/hypercube.o $(HELIB_SRC)/matching.o $(HELIB_SRC)/powerful.o $(HELIB_SRC)/BenesNetwork.o $(HELIB_SRC)/permutations.o $(HELIB_SRC)/PermNetwork.o $(HELIB_SRC)/OptimizePermutations.o $(HELIB_SRC)/eqtesting.o $(HELIB_SRC)/polyEval.o $(HELIB_SRC)/extractDigits.o $(HELIB_SRC)/EvalMap.o $(HELIB_SRC)/OldEvalMap.o $(HELIB_SRC)/recryption.o $(HELIB_SRC)/debugging.o
TESTPROGS = validation_test bgv_he_timing_test helib_timing_test

TIMING_TESTS = add sub mul square cube neg eq rotate shift
NUM_TESTS = 5

all: bgv_he.a

check: $(TESTPROGS)
	@rm -r test_results
	@mkdir -p test_results
	@make valid_test
	@make bgv_he_time_test
	@make helib_time_test

valid_test:
	@./validation_test || (echo "Validation test failed. Stopping further execution."; exit 1)

bgv_he_time_test:
	@echo "RUNNING BGV_HE TIMING TESTS ..."	
	@num=1 ; while [ $${num} -le $(NUM_TESTS) ] ; do \
		for test in $(TIMING_TESTS) ; do \
			echo "running test $${test} $${num}" ; \
			time ./bgv_he_timing_test $${test} > test_results/bgv_he_$${test}_result_$${num} ; \
		done ; \
		num=`expr $${num} + 1` ; \
	done
	@echo "     TESTS COMPLETE. RESULTS IN ./test_results/"

helib_time_test:
	@echo "RUNNING HELIB TIMING TESTS ..."	
	@num=1 ; while [ $${num} -le $(NUM_TESTS) ] ; do \
		for test in $(TIMING_TESTS) ; do \
			echo "running test $${test} $${num}" ; \
			time ./helib_timing_test $${test} > test_results/helib_$${test}_result_$${num} ; \
		done ; \
		num=`expr $${num} + 1` ; \
	done
	@echo "     TESTS COMPLETE. RESULTS IN ./test_results/"

tests: $(TESTPROGS)

obj: $(OBJ)

%.o: %.cpp $(HEADER)
	$(CC) $(CFLAGS) -c $< $(LDLIBS)

bgv_he.a: $(OBJ)
	$(AR) $(ARFLAGS) bgv_he.a $(OBJ) $(HELIB_OBJ)

./%_test: %_test.cpp bgv_he.a
	$(CC) $(CFLAGS) -o $@ $< bgv_he.a $(LDLIBS)

clean:
	-rm -f *.o *_x *_x.exe *.a core.*
	-rm -rf *.dSYM
	-rm *~
	-rm bgv_he_timing_test
	-rm validation_test
	-rm helib_timing_test

info:
	: BGV_HE requires HElib
	: Compilation flags are 'CFLAGS=$(CFLAGS)'
	:
