    def compute_similarity_matrix( self ):
        """
        `text` should be the long document.
        """
        self.S = [[0 for _ in range( self.iTargetLen )] 
                     for _ in range( self.iTextLen )]

        for i in range( self.iTextLen ):
            for j in range( self.iTargetLen ):
                cA = self.sText[i]
                cB = self.sTarget[j]
                if cA == cB:
                    penalty = self.penalties["exact"]
                elif cA.isprintable() and cB.isprintable() and cA != cB:
                    penalty = self.penalties["mismatch_char"]
                else:
                    penalty = self.penalties["mismatch_non-printable"]
                self.S[i][j] = penalty




def print_matrix( m ):
    """
    Prints a matrix, for debugging purposes. 
    """
    print( '\n'.join([''.join(['{:4}'.format( item ) for item in row])
        for row in m]))
    print('')

