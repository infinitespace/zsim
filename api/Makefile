TARGET = zsimapi
CXXFLAGS = -g -O3 -flto -Wall -Wl,--no-as-needed -pedantic -std=c++11
LIBNAME = lib$(TARGET)

# Common deps
DEPS = Makefile zsim_api.h

lib: $(LIBNAME).so

all: lib test

test: test.cpp $(DEPS)
	$(CXX) $< -o $@ $(CXXFLAGS) -fPIC -DPIC -L. -pthread -l$(TARGET)

$(LIBNAME).so: $(TARGET).o
	$(CXX) -shared -o $@ $<

$(LIBNAME).a: $(TARGET).o
	$(AR) rcsv $@ $<

$(TARGET).o: zsim_api.cpp $(DEPS)
	$(CXX) $< -c -o $@ $(CXXFLAGS) -fPIC -DPIC

clean:
	$(RM) *~ *.o *.a *.so test

.PHONY: clean lib

