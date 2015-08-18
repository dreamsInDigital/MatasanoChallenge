#!/usr/bin/python
import string
import base64


def bin( x ):
    if ( x == 0 ):
        return '0'
    else:
        return (  bin(x/2)+str(x%2) ).lstrip('0') or '0'


def hamming( x, y ):
# convert strings to binary
    bin_x = ''.join(['%08d'%int(bin(ord(i))) for i in x])
    bin_y = ''.join(['%08d'%int(bin(ord(i))) for i in y])
  
    count = 0 

    # counts number of differing bits
    for i in range ( 0, len( bin_y ) ):
        if ( bin_x[i] != bin_y[i] ):
            count = count + 1
    return count


def main():
    with open( 'input6.txt' ) as f:
        ciphertext = f.readlines()

# Cycles through the possible key lengths
    for i in range ( 2, 41 ): 
        sum = 0    

# For each key length, generate a comparison on each line of text
        for k in range ( 0, len( ciphertext) ):
            cipherSubstring = base64.b64decode( ciphertext[k] )
            subsub1 = cipherSubstring[0:i]
            subsub2 = cipherSubstring[i:i*2]
            ham1 = float( hamming ( subsub1, subsub2 ) )/len( subsub2 )
            sum = sum + ham1

# Average out the comparisons from each line of text        
        average = float(sum)/len( ciphertext )

# Print keys under a certain threshold for hamming distance
        if ( average < 3.1 ):
            print "Key = %i " % (i)
            print "Average Hamming Dist = %03f " % (average)
            print ""


if __name__=='__main__':
    main()