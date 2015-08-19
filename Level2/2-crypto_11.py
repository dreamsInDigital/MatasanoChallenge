#!/usr/bin/python
import string
import random
import base64
from Crypto.Cipher import AES

"""
*******************************************************************************************
Checks for repeated 16 byte blocks to determine whether ECB encryption is used. If no 
repeats detected, returns a result of CBC (somewhat unreliable for short strings).
*******************************************************************************************
"""
def detect( ciphertext ):
    count = 0
    for i in range ( 0, len( ciphertext ) - 16, 16 ):
        if ( ciphertext[i:i+15] in ciphertext[i+15:] ):
            return 'ECB'
    return 'CBC'

"""
*******************************************************************************************
Checks whether the length of a string is a multiple of 16, will pad with the byte 'x04'
if necessary.
*******************************************************************************************
"""
def padBlock( input ):  
    if ( len( input ) % 16 != 0 ): 
        padding = ['\x04']*( 16 - ( len ( input ) % 16 ) ) 
        return input + string.join( padding, '' )
    else: return input

"""
*******************************************************************************************
Encrypts with ECB under a randomly generated key.
*******************************************************************************************
"""
def ecbEncrypt( input ):
    encryptor = AES.new( randKey(), AES.MODE_ECB )
    return encryptor.encrypt( input )

"""
*******************************************************************************************
Calls the recursive function cbcEncryptBlock, providing a randKey() result as the key
and IV.
*******************************************************************************************
"""
def cbcEncrypt( input ):
    IV = randKey()
    key = randKey()
    return cbcEncryptBlock( input, IV, 0, key )

"""
*******************************************************************************************
Encrypts each block, and then sends the result to the next call for chain encryption
by recursion.
*******************************************************************************************
"""
def cbcEncryptBlock( input, block, ix, key ):
# test for base case - end of input string
    if ix == len ( input ):
        return ''

# do xor on next chunk of input with provided block
    result = list()
    subBlock = input[ix:ix+16]
    for i in range ( 0, len( subBlock ) ):
        result.append( chr( ord( subBlock[i] ) ^ ord( block[i] ) ) )
    result = string.join( result, '' )

# perform ECB encryption on this chunk
    encryptor = AES.new( key, AES.MODE_ECB )
    result = encryptor.encrypt( result )

# recursive call, which returns the encrypted string past this point
    partialRes = cbcEncryptBlock( input, result, ix + 16, key )  
            
# appends result from call, and returns the encrypted string to this point
    return result + partialRes  

"""
*******************************************************************************************
Makes two calls to genPadding(), to add a 5-10 byte pad on each end of the input.
*******************************************************************************************
"""
def addPadding( input ):
    return genPadding() + input + genPadding()

"""
*******************************************************************************************
Randomly generates a padding string to be appended to the input.
*******************************************************************************************
"""
def genPadding():
    length = random.randint( 5, 10 )
    pad = [0]*length
    for i in range ( 0, length ):
        pad[i] = chr( random.randint( 0, 255 ) )  
    return string.join( pad, "" )
   
"""
*******************************************************************************************
Randomly chooses whether to encrypt with ECB or CBC.
*******************************************************************************************
"""
def chooseMethod( input ):
    choice = random.randint( 1, 2 )
    if ( choice == 1 ):
        result = ecbEncrypt( padBlock( addPadding( input ) ) )
    if ( choice == 2 ):
        result = cbcEncrypt( padBlock( addPadding( input ) ) )
    return result

"""
*******************************************************************************************
Randomly generates a 16 byte key. 
*******************************************************************************************
"""
def randKey():
    keyList = [0]*16
    for i in range ( 0 , 16 ):
        keyList[i] = chr( random.randint( 0, 255 ) )
    return string.join( keyList, "" )

"""
*******************************************************************************************
Main - prompts user for input, then encrypts it with either ECB or CBC. Calls the detect()
function on the output to determine which type was used.
*******************************************************************************************
"""
def main():
    print "Enter a string to encrypt, or 'quit' to exit: \n"
    inputStr = raw_input("=> ")
    while ( inputStr != 'quit' ):
        encrypted = base64.b64encode( chooseMethod( inputStr ) )
        print encrypted
        print ""
        print "Detected as: %s" % detect( encrypted )
        print ""
        inputStr = raw_input("=> ")


if __name__=='__main__':
    main()