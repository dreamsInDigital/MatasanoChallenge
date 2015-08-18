#!/usr/bin/python
import base64
import string

def main( ciphertext, key ):
    ciphertext = ciphertext.decode ( "hex" )
    key = key.decode ( "hex" )
    result = list()
  
    for i in range ( 0, len( ciphertext ) ):
        result.append( chr( ord( ciphertext[i] ) ^ ord( key[i] ) ) )

    print string.join( result, "" ).encode( "hex" ) 

if __name__=='__main__':
    ciphertext = '1c0111001f010100061a024b53535009181c'
    key = '686974207468652062756c6c277320657965'

    main( ciphertext, key )