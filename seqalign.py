#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""

Uses the Needleman-Wunsch algorithm as a starting point.

Rather than memoization, we use a 'bottom-up iterative approach' through dynamic programming. Each sub-alignment is computed only once.

Cost table:
exact match, printable or not - 0
mismatch of character for a different printable character - 3
mismatch of a printable character for a non-printable character - 5
deletion in text from long document - 1
deletion in target string - 4

Henry Wandover
8/5/2025
Bard College
"""

import argparse
import sys
import time

SKIPPED_CHAR = '_'

"""
Prints a matrix, for debugging purposes. Also it is horrible and does not do any
sort of alignment of lables or elements.
"""
def print_matrix( m ):
    for i, row in enumerate(m):
        print (" ".join(map(str, row)) )
    print('')


class SequenceAlignment:
    penalties = {
            "exact": 0,
            "mismatch_char": 3,
            "mismatch_non-printable": 5,
            "deletion_in_text": 1,
            "deletion_in_target": 4
    }

    A = ""
    B = ""
    nA = 0
    nB = 0
    dA = 0
    dB = 0

    S = []
    F = []

    alignment = ""
    cost = sys.maxsize

    def __init__( self, A, B ):
        self.A = A
        self.B = B
        self.nA = len( A )
        self.nB = len( B )
        self.dA = self.penalties["deletion_in_text"]
        self.dB = self.penalties["deletion_in_target"]

        self.compute_similarity_matrix()
        #print_matrix( self.S )

        self.compute_f_matrix()
        #print_matrix( self.F )

        self.seq_alignment()


    def __str__( self ):
        return f"{self.alignment}"

    def regen( self, newA ):
        self.A = newA
        self.nA = len( newA )

        self.compute_similarity_matrix()

        self.compute_f_matrix()

        self.seq_alignment()

    """
    `A` should be the long document.
    """
    def compute_similarity_matrix( self ):
        self.S = [[0 for _ in range( self.nB )] for _ in range( self.nA )]

        for i in range( self.nA ):
            for j in range( self.nB ):
                penalty = -1 # Something went wrong if this selected

                cA = self.A[i]
                cB = self.B[j]

                if cA == cB: # Exact
                    penalty = self.penalties["exact"]
                elif (not cA.isprintable() or not cB.isprintable()) and cA != cB:
                    penalty = self.penalties["mismatch_non-printable"]
                elif cA.isprintable() and cB.isprintable() and cA != cB:
                    penalty = self.penalties["mismatch_char"]

               
                self.S[i][j] = penalty

    """
    """
    def compute_f_matrix( self ):
        self.F = [[0 for _ in range( self.nB + 1 )] for _ in range( self.nA + 1 )]

        for i in range( self.nA + 1 ):
            self.F[i][0] = self.dA * i

        for j in range( self.nB + 1 ):
            self.F[0][j] = self.dB * j

        for i in range( 1, self.nA + 1 ):
            for j in range( 1, self.nB + 1 ):
               
                match = self.F[i - 1][j - 1] + self.S[i - 1][j - 1]
                delete = self.F[i - 1][j] + self.dA
                insert = self.F[i][j - 1] + self.dB
                self.F[i][j] = min( match, delete, insert ) 


    def seq_alignment( self ):
        alignmentA = ""
        alignmentB = ""
        i = self.nA
        j = self.nB 
        cost = 0

        # We don't care about multiple instances if they have same cost
        while i > 0 or j > 0 and cost < self.cost: 
            if self.F[i][j] == self.F[i - 1][j - 1] + self.S[i - 1][j - 1]:
                alignmentA = self.A[i - 1] + alignmentA
                alignmentB = self.B[j - 1] + alignmentB
                cost += self.S[i - 1][j - 1] # Accounts for matches and mismatches
                i -= 1
                j -= 1
            elif i > 0 and self.F[i][j] == self.F[i - 1][j] + self.dA:
                alignmentA = self.A[i - 1] + alignmentA
                alignmentB = SKIPPED_CHAR + alignmentB
                if i != 1:
                    cost += self.dA
                i -= 1
            else:
                alignmentA = SKIPPED_CHAR + alignmentA
                alignmentB = self.B[j - 1] + alignmentB
                cost += self.dB
                j -= 1


        if cost < self.cost:
            alignmentStr = "" 
            for c1, c2 in zip( alignmentA, alignmentB ):
                alignmentStr += (c1 + c2 + '\n')

            self.alignment = alignmentStr
            self.cost = cost
        else:
            return


def print_header( alignment ):
    print( f"opt index ? cost {alignment.cost}" )
    print( "Start at ? in the long text" )
    print( "Alignment (target on right). Skipped chars are aligned to '_'." )
    print( alignment )

def main():
    parser = argparse.ArgumentParser(
            prog="BulkSeqAlign",
            description="A modified sequence alignment aglorithm for longer text inputs.",
            epilog='Sup Sven')
    parser.add_argument('string_name')
    parser.add_argument("--somearg", help="some help", default="val")

    args = parser.parse_args()


    
    line = sys.stdin.readline()
    seq = SequenceAlignment( line, args.string_name )

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        seq.regen( line )

        #time.sleep(3)

    print_header( seq )

    """
    for word in sys.stdin.read().split():
        if word not in dpTable:
            dpTable[word] = 1
   
    condensed = list(dpTable)

    for word in condensed:
        if word == args.string_name:
            print(word)
    """
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except KeyboardInterrupt: pass
