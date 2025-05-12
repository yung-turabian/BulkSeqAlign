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

"""
Prints a matrix, for debugging purposes. Also it is horrible and does not do any
sort of alignment of lables or elements.
"""
def print_matrix( m ):
    print( '\n'.join([''.join(['{:4}'.format( item ) for item in row])
        for row in m]))
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
    cost = -1

    start_index = 0
    end_index = 0

    def __init__( self, text, target ):
        self.sText = text
        self.sTarget = target
        self.iTextLen = len( text )
        self.iTargetLen = len( target )
        self.iTextGapPenalty = self.penalties["deletion_in_text"]
        self.iTargetGapPenalty = self.penalties["deletion_in_target"]

        self.compute_f_matrix()
        self.compute_similarity_matrix()
        #self.seq_alignment()


    def __str__( self ):
        return f"{self.alignment}"
    
    def compute_similarity_matrix( self ):
        """
        `A` should be the long document.
        """
        self.S = [[0 for _ in range( self.iTargetLen )] for _ in range( self.iTextLen )]

        for i in range( self.iTextLen ):
            for j in range( self.iTargetLen ):

                cA = self.sText[i]
                cB = self.sTarget[j]

                if cA == cB: # Exact
                    penalty = self.penalties["exact"]
                elif cA.isprintable() and cB.isprintable() and cA != cB:
                    penalty = self.penalties["mismatch_char"]
                else:
                    penalty = self.penalties["mismatch_non-printable"]

                self.S[i][j] = penalty


    def compute_f_matrix( self ):
        self.F = [[0 for _ in range( self.iTextLen + 1 )] for _ in range( self.iTargetLen + 1 )]

        for i in range( self.iTextLen ):
            self.F[i][0] = i * self.iTextGapPenalty

        for j in range( self.iTargetLen ):
            self.F[0][j] = j * self.iTargetGapPenalty

        for i in range( 1, self.iTextLen ):
            for j in range( 1, self.iTargetLen ):
                
                match = self.F[i - 1][j - 1] 
                delete = self.F[i - 1][j] + self.iTextGapPenalty
                insert = self.F[i][j - 1] + self.iTargetGapPenalty
                self.F[i][j] = min( match, delete, insert )
                
        self.cost = self.F[self.iTextLen - 1][self.iTargetLen - 1] # Solution to largest subproblem


    def seq_alignment( self ):
        alignmentA = ""
        alignmentB = ""
        i = self.iTextLen
        j = self.iTargetLen 
        
        min_cost = self.cost
        cost = 0


        # We don't care about multiple instances if they have same cost
        while ( i > 0 or j > 0 ) and cost < min_cost: 
            if i > 0 and j > 0 and self.F[i][j] == self.F[i - 1][j - 1] + self.S[i - 1][j - 1]:
                alignmentA = self.A[i - 1] + alignmentA
                alignmentB = self.B[j - 1] + alignmentB
                cost += self.S[i - 1][j - 1] # Accounts for matches and mismatches
                i -= 1
                j -= 1

                self.start_index = i + 1
            elif i > 0 and self.F[i][j] == self.F[i - 1][j] + self.dA:
                # Don't charge for deletions before the sequence
                # we are searching for. This means if we are looking
                # at the first index of target, ingore the previous
                # of long text.
                if self.A[i] == self.A[0]:
                    if self.B[j] == self.A[i]:
                        alignmentA = self.A[i] + alignmentA
                        alignmentB = SKIPPED_CHAR + alignmentB
                        cost += self.dA

                i -= 1
            else:
                alignmentA = SKIPPED_CHAR + alignmentA
                alignmentB = self.B[j] + alignmentB
                cost += self.dB
                j -= 1

        if cost < min_cost:
            alignmentStr = "" 
            for c1, c2 in zip( alignmentA, alignmentB ):
                alignmentStr += (c1 + c2 + '\n')

            self.alignment = alignmentStr
            self.cost = cost
            self.end_index = self.start_index + len( alignmentA ) - 1
        else:
            return
    

def print_header( alignment ):
    print( f"opt index {alignment.end_index} cost {alignment.cost}" )
    print( f"Start at {alignment.start_index} in the long text" )
    print( "Alignment (target on right). Skipped chars are aligned to '_'." )
    print( alignment )

def main():
    parser = argparse.ArgumentParser(
            prog="BulkSeqAlign",
            description="A modified sequence alignment aglorithm for longer text inputs.",
            epilog='')
    parser.add_argument( 'target' )
    parser.add_argument( "--somearg", help="some help", default="val" )

    args = parser.parse_args()
    
    line = sys.stdin.readline()
    seq = SequenceAlignment( line, args.target )
    #print_header( seq )

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        # Found the first instance
        if seq.cost == 0:
            break

        print_header( seq )
        print_matrix( seq.F )
        seq.regen( line )



    print_header( seq )
    print_matrix( seq.S )
    print_matrix( seq.F )

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
