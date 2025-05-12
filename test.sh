#!/usr/bin/bash

prog=./seqalign.py
last_output=""

function assert {
		name=$1
		expected=$2
		actual=$last_output

		if [ "$expected" = "$actual" ]; then
				echo "✓: $name"
		else
				echo "✗"
				echo "Expected: $expected"
				echo "Actual: $actual"
		fi
}

function run {
		fname=$1
		target=$2

		last_output=$(cat $fname | $prog $target | awk 'NR==1{end=$3; cost=$5} NR==2{print $3, end, cost}')
}

run "tests/hello.txt" "hello"
assert "hello" "0 5 0" 

last_output=$(echo -n inputfiletesting | $prog "T est.inx" | awk 'NR==1{end=$3; cost=$5} NR==2{print $3, end, cost}')
assert "input_string" "8 17 13"

run "tests/that.txt" "that?...\"he"
assert "That?" "61 72 2"

#run "tests/anna.txt" "that?...” he" 
#assert "Anna1" " 78233 78245 1"
