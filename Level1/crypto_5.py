#!/usr/bin/python
import string

def main( text, key ):
    result = list()
  
    for i in range ( 0, len( text ) ):
        result.append( chr( ord( text[i] ) ^ ord( key[i%len( key )] ) ) )

    print string.join( result, "" ).encode( "hex" ) 

if __name__=='__main__':
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    key = 'ICE'

    main( text, key )