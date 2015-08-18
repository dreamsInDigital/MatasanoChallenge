#!/usr/bin/python
import base64
import string

def cipher( ciphertext, key ): 
    result = list()
    for i in range ( 0, len( ciphertext ) ):
        result.append( chr( ord( ciphertext[i] ) ^ ord(key[i%len(key)]) ) )
    return result
             
def main():
    with open( 'input6.txt' ) as f:
        ciphertext = f.readlines()
    cipherString = string.join( ciphertext, "" )
    decodedString = base64.b64decode( cipherString )
    
    result = cipher ( decodedString,"Terminator X: Bring the noise" )
    print string.join( result, "" )

if __name__=='__main__':
    main()