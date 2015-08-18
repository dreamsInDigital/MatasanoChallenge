#!/usr/bin/python
import base64
import collections
import string

def cipher( ciphertext, key ): 
    count = 0
    result = list()
    for i in range ( 0, len( ciphertext ) ):
        result.append( chr( ord( ciphertext[i] ) ^ key ) )
        if ( ord( result[i] ) >= 32 and ord( result[i] ) <= 126 ):
            count = count + 1   

    cnt = collections.Counter( result )
    common_chrs = cnt['e']+cnt['a']+cnt['i']+cnt[' ']+cnt['t']+cnt['n']+cnt['n']+cnt['r']+cnt['o']

# If 95% of the characters are printable and 25% are common, it prints the result and histogram

    if ( float(count)/float(len(result)) > 0.95 and float(common_chrs)/float(len(result)) > 0.25  ):
        print "KEY = %d" % ( key )
        print "Count = %d" % ( count )
        print "space =",
        print '*'*cnt[' ']
        print "e =",
        print "*"*cnt['e']
        print "t =",
        print "*"*cnt['t']
        print "a =",
        print "*"*cnt['a']
        print "o =",
        print "*"*cnt['o']
        print "i =",
        print "*"*cnt['i']
        print "n =",
        print "*"*cnt['n']
        print "r =",
        print "*"*cnt['r']
        print string.join( result, "" )
        print ""


def main(): 
    with open( 'input6.txt' ) as f:
        ciphertext = f.readlines()
   
    cipherString = string.join( ciphertext, "" )    
    cipherDecode = base64.b64decode( cipherString )

# Change these values based on which position you are currently solving 
    keyLength = 29   
    l = 0
    
    for k in range ( 0, keyLength ):
        print '-'*25,"POSITION ", l,'-'*25, '\n'
        firstBlock = list()
        i = l
        j = l + keyLength
        while ( j < len( cipherDecode ) ):
            substring = cipherDecode[i:j]
            firstBlock.append( substring[0] )
            i = i + 29
            j = j + 29
        for key in range( 32, 127 ):
            cipher( firstBlock, key )
        l = l + 1

if __name__=='__main__':
    main()