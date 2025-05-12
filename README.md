# Sequence Alignment Aglorithm For Long Text Inputs

# About

Makes use of the Needleman-Wunsch algorithm, which typically is useful for so called global sequences; however, in this case it has been modified to not be prejudice at where the target substring actually begins. Rather than expecting the sting to begin at F\[0\]\[0\] in the computed cost matrix, it can start anywhere. This helps in eliminating a bunch of junk that we don't care for in our search.

This algorithm is not highly optimized, and there are most likely faster implementations of such a search making use of Smith-Waterman. That being said, it can find a target string in a long input, such as [Anna Karenina](./tests/anna.txt), in about 30 seconds.

Still has a worst-case performance of O (m • n)

## Usage
```bash
$ cat tests/anna.txt | ./seqalign.py "that?...” he"
```
