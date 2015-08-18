#!/usr/bin/python
import string

# Breaks the string down into 16 byte blocks and checks for repeats
def blockCheck( ciphertext, lineNum ): 
    for i in range ( 0, len( ciphertext ) - 16, 16 ):
        if ( ciphertext[i:i+15] in ciphertext[i+15:] ):
            print "Line: %i" % ( lineNum )
            print "Repeat: %s" % ( ciphertext[i:i+15] )
            print ""   
             
def main():
    with open( 'input8.txt' ) as f:
        ciphertext = f.readlines()

# Calls blockCheck on each line of the input text
    for i in range ( 0, len( ciphertext ) ):
        blockCheck( ciphertext[i], i + 1 )
        

if __name__=='__main__':
      main()