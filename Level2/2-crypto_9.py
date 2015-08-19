#!/usr/bin/python
import string


"""
*********************************
General padding function that receives 3 arguments:
  input - the string to be padded
  blockLength - how long we want the padded string to be
  byte - the repeating byte to pad it with
*********************************
"""
def padBlock( input, blockLength, byte ):  
# generates a list containing the number of bytes needed for padding  
    padding = [byte]*( blockLength - ( len ( input ) % blockLength ) )
# appends the padding to our input string
    return input + string.join( padding, '' )

def main():
    padded = padBlock( 'HOMERSIMPSON', 20, '\x04' )
    print list ( padded )

if __name__=='__main__':
    main()