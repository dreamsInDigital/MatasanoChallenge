#!/usr/bin/python
import collections
import string

def cipher( ciphertext, key, line ):
    ciphertext = ciphertext.strip()
    cipherDecode = ciphertext.decode( "hex" ) 
    result = list()
  
    for i in range ( 0, len( cipherDecode ) ):
        result.append( chr( ord( cipherDecode[i] ) ^ key ) )

    cnt = collections.Counter( result )
    common_chrs = cnt['e']+cnt['a']+cnt['i']+cnt[' ']+cnt['t']

    if ( float(common_chrs)/float(len(result)) > 0.30 ):
        print string.join( result, "" )
        print "    Key = %d" % ( key )
        print "    Line # = %d" % ( line + 1 )
        print ""

def main(): 
    with open( 'input4.txt' ) as f:
        ciphertext = f.readlines()
        for i in range (0, len(ciphertext)):
            for k in range (32, 127):
                cipher( ciphertext[i], k, i )

if __name__=='__main__':
    main()