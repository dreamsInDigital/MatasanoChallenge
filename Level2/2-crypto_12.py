#!/usr/bin/python
import string
import random
import base64
from Crypto.Cipher import AES

key = '742evergreenterr'

"""
*******************************************************************************************
Checks for repeated 16 byte blocks to determine whether ECB encryption is used
(somewhat unreliable for short strings).
*******************************************************************************************
"""
def detect( ciphertxt ):
    for i in range ( 0, len( ciphertext ) - 16, 16 ):
        if ( ciphertext[i:i+15] in ciphertext[i+15:] ):
            print "ECB Encryption - Repeat: %s" % ( ciphertext[i:i+15] )

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
Encrypts with ECB under a fixed key.
*******************************************************************************************
"""
def ecbEncrypt( input, toDecrypt ):
    encryptor = AES.new( key, AES.MODE_ECB )
    return encryptor.encrypt( padBlock( input + toDecrypt ))

"""
*******************************************************************************************
Creates a library (list) of encrypted strings for each variation of the one byte short block.
Ex. AAAAAAAAAAAAAAAB, AAAAAAAAAAAAAAAC, etc.
*******************************************************************************************
"""
def genLibrary( inputStr ):
    resultBlocks = list()
    input = ['A']*16
    for i in range ( 32, 127 ):   
        input[15] = chr( i )
        resultBlocks.append( ecbEncrypt( string.join( input, '' ), inputStr ))
    return resultBlocks             

"""
*******************************************************************************************
Main - reads a base64 encoded sequence from a file. Encrypts the file, then uses byte-at-
a-time ECB decryption to determine the contents of the encrypted sequence.
*******************************************************************************************
"""
def main():
    with open( 'input12.txt' ) as f:
        ciphertext = f.read()
    decoded = base64.b64decode( ciphertext )

#*********  AUTOMATED SOLUTION
    library = genLibrary( decoded )
# Loops through each character of the decoded text appending it to the one byte short sequence
# Compares the block generated after ECB encryption to our library, adds the result to our
# decrypted string.
    input = ['A']*15
    decryptedString = ''
    for j in range ( 0, len( decoded ) ):
        encryptedBlock = ecbEncrypt( string.join( input, '' ), decoded[j:] )
        for k in range ( 0, len(library) ):
            if encryptedBlock[0:16] in library[k]:
                decryptedString = decryptedString + chr( k + 32 )
    print decryptedString

#******** ORIGINAL ORACLE FUNCTION - used to determine block length and detect ECB
    print "\nEnter a string to encrypt, or 'quit' to exit: \n"
    inputStr = raw_input("=> ")
    while ( inputStr != "quit" ):
        encrypted = base64.b64encode( ecbEncrypt( inputStr, decoded ) )
        print encrypted
        detect( encrypted ) 
        inputStr = raw_input("\n=> ")


if __name__=='__main__':
    main()