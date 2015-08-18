#!/usr/bin/python
import base64
import string
import collections

def cipher( ciphertext, key ):
    ciphertext = ciphertext.decode( "hex" ) 
    result = list()
  
    for i in range ( 0, len( ciphertext ) ):
        result.append( chr( ord( ciphertext[i] ) ^ key ) )

# Counts common characters and checks result strings for frequency
    cnt = collections.Counter( result )
    common_chrs = cnt['e']+cnt['a']+cnt['i']+cnt[' ']+cnt['t']

    if ( float(common_chrs)/float(len(result)) > 0.25 ):
	print string.join( result, "" )
    	print "Key = "+chr(key)

def main(): 
    ciphertext = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    for i in range( 65, 122 ):
        cipher( ciphertext, i )

if __name__=='__main__':
    main()