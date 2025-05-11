#!/usr/bin/sh

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

run "test.txt" "hello"
assert "hello" "0 5 0" 

#cat anna.txt | ./seqalign.py "that?...\" he"
