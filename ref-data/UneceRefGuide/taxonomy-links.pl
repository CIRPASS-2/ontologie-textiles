#!perl -wn
1..m{Details of code lists</a></h1>} and next;
m{(Details of identifiers|Overview identifier schemes)</h1>} and last;
print "$1\n" while m{(http[^"]+)}g;

