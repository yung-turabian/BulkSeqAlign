#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Uses the Needleman-Wunsch algorithm as a starting point.

Henry Wandover
8/5/2025
Bard College
"""

import argparse
import sys
import time
import numpy as np

def print_matrix( m ):
    """
    Prints a matrix, for debugging purposes. 
    """
    print( '\n'.join([''.join(['{:4}'.format( item ) for item in row])
        for row in m]))
    print('')

class SequenceAlignment:
    """
    Perform a 'global' sequence alignment, as in we are comparing in its
    entirerty string `text` to string `target`. However, there is a variable
    `CHARGE_FOR_PRIOR_DELETIONS` that will curb any deletions before the
    start of the target string. That is in the only reference to a concept
    of a substring here.
    """
    
    # This table defines possible descrepencies
    penalties = {
            "exact": 0,
            "mismatch_char": 3,
            "mismatch_non-printable": 5,
            "deletion_in_text": 1,
            "deletion_in_target": 4
    }

    SKIPPED_CHAR = '_'
    """
    Don't charge for deletions before the sequence
    we are searching for. This means if we are looking
    at the first index of target, ingore the previous
    of long text.
    """
    CHARGE_FOR_PRIOR_DELETIONS = False

    # Kinda arbitrary
    COST_CEILING = 25

    def __init__( self, text, target ):
        self.sText = text
        self.sTarget = target
        self.iTextLen = len( text )
        self.iTargetLen = len( target )
        self.iTextGapPenalty = self.penalties["deletion_in_text"]
        self.iTargetGapPenalty = self.penalties["deletion_in_target"]

        self.matF = None # F matrix, or cost/scoring matrix

        self.sAlignment = None # The final alignment, vertical
        self.iCost = None
        self.iStartIndex = None

        self.bBestMatchFound = False

        self.compute_f_matrix()
        self.align()

    def __str__( self ):
        return f"Cost: {self.cost}\nAlignment:\n{self.sAlignment}"

    def print( self ):
        if self and self.bBestMatchFound:
            iEndIndex = self.iStartIndex + self.iTargetLen
            print(f"opt index {self.iStartIndex + self.iTargetLen} cost {self.iCost}")
            print(f"Start at {self.iStartIndex} in the long text")
            print("Alignment (target on right). Skipped chars are aligned to '_'.")
            print(self.sAlignment)
        else:
            print("No suitable alignment found")

    def penalty( self, cA, cB ):
        if cA == cB:
            return self.penalties["exact"]
        elif cA.isprintable() and cB.isprintable():
            return self.penalties["mismatch_char"]
        else:
            return self.penalties["mismatch_non-printable"]
        
    def compute_f_matrix( self ):
        """
        Adopted from the pseudocode provided on the Wikipedia page for Needleman
        as well as in Algorithms Illuminated.
        """
        self.matF = np.zeros( (self.iTextLen + 1, self.iTargetLen + 1), int )
        
        # Altered from the original Needleman, aligns from anywhere in sText,
        # doesn't penalize deletions before the match
        if self.CHARGE_FOR_PRIOR_DELETIONS:
            for i in range(self.iTextLen + 1):
                self.matF[i][0] = i * self.iTextGapPenalty
        else:
            for i in range(self.iTextLen + 1):
                self.matF[i][0] = 0

        for j in range( self.iTargetLen + 1 ):
            self.matF[0][j] = j * self.iTargetGapPenalty

        for i in range( 1, self.iTextLen + 1 ):
            for j in range( 1, self.iTargetLen + 1 ):
                iPenalty = self.penalty(self.sText[i - 1], self.sTarget[j - 1])
                match = self.matF[i - 1][j - 1] + iPenalty
                delete = self.matF[i - 1][j] + self.iTextGapPenalty
                insert = self.matF[i][j - 1] + self.iTargetGapPenalty
                self.matF[i][j] = min( match, delete, insert )

        self.iBestEndIndex = None

        aLastCol = self.matF[:, self.iTargetLen]
        self.iBestEndIndex = np.argmin( aLastCol )
        self.iCost = aLastCol[self.iBestEndIndex]

    def align( self ):
        sAlignmentText = ""
        sAlignmentTarget = ""
        i = self.iBestEndIndex
        j = self.iTargetLen 
        iCost = 0

        bMatchComplete = self.CHARGE_FOR_PRIOR_DELETIONS

        while j > 0: # Will halt when all of target has been matched, i.e. i = 0 
            iPenalty = self.penalty(self.sText[i - 1], self.sTarget[j - 1])
            if i > 0 and j > 0 and self.matF[i][j] == self.matF[i - 1][j - 1] + iPenalty:
                sAlignmentText = self.sText[i - 1] + sAlignmentText
                sAlignmentTarget = self.sTarget[j - 1] + sAlignmentTarget
                i -= 1
                j -= 1
            elif i > 0 and self.matF[i][j] == self.matF[i - 1][j] + self.iTextGapPenalty:
                sAlignmentText = self.sText[i - 1] + sAlignmentText
                sAlignmentTarget = self.SKIPPED_CHAR + sAlignmentTarget
                i -= 1
            else:
                sAlignmentText = self.SKIPPED_CHAR + sAlignmentText
                sAlignmentTarget = self.sTarget[j - 1] + sAlignmentTarget
                j -= 1

        sAlignment = "" 
        for c1, c2 in zip( sAlignmentText, sAlignmentTarget ):
            sAlignment += (c1 + c2 + '\n')
        
        if self.iCost < self.COST_CEILING:
            self.bBestMatchFound = True

        self.sAlignment = sAlignment
        self.iStartIndex = i

def main():
    parser = argparse.ArgumentParser(
            prog="BulkSeqAlign",
            description="A modified sequence alignment aglorithm for longer text inputs.",
            epilog='')
    parser.add_argument( 'target' )
    #parser.add_argument( "--somearg", help="some help", default="val" )
    args = parser.parse_args()


    sText = sys.stdin.read().strip('\n')
    sTarget = args.target

    seqBestMatch = SequenceAlignment( sText, sTarget )
    seqBestMatch.print()

    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except KeyboardInterrupt: pass
