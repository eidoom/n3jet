CXX?=g++
CXXFLAGS=-g -std=c++11 -Wall -Wextra -Wpedantic
DEFS=-DDEBUG 

.PHONY: clean all

all: ex_3g2A single_test

# Example of using the NN
ex_3g2A: ex_3g2A.o model_fns.o
	$(CXX) -o $@ $^ $(LDFLAGS) $(LIBS)

single_test: single_test.o model_fns.o
	$(CXX) -o $@ $^ $(LDFLAGS) $(LIBS)

model_fns.o: model_fns.cpp model_fns.h
	$(CXX) $(CXXFLAGS) -o $@ -c $< $(CPPFLAGS) $(DEFS)

ex_3g2A.o: ex_3g2A.cpp
	$(CXX) $(CXXFLAGS) -o $@ -c $< $(CPPFLAGS) $(DEFS)

single_test.o: single_test.cpp
	$(CXX) $(CXXFLAGS) -o $@ -c $< $(CPPFLAGS) $(DEFS)

clean:
	-rm -f *.o __pycache__ ex_3g2A single_test
