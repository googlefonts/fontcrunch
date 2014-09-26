%module quadopt
%include "std_string.i"
%feature ("kwargs");

%{
#include "quadopt.h"
%}

%include "quadopt.h"
