# Todo

+ Need to calculate cost as the final part of sequence alignment part, then of course must implement the dynamic programming element of parsing text.

+ Should print as:
```
$ cat anna_karenina.txt | python seqalign.py "that?..." he"
opt index 79883 cost 2
Start 79870 in the long text
Alignment (target on right). Skipped chars are aligned to '_'.
t t
h h
a a
t t
? ?
. .
. .
. .
" "
   
s _
h h
e e
```
