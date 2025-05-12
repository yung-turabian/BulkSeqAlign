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
assert "hello" "44 48 0" 

last_output=$(echo -n inputfiletesting | $prog "T est.inx" | awk 'NR==1{end=$3; cost=$5} NR==2{print $3, end, cost}')
assert "input_string" "8 16 13"


target="that?...\" he"
run "tests/anna.txt" $target 
assert "Anna1" "0 0 0"
