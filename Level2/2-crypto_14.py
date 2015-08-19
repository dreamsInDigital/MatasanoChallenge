#!/usr/bin/python
import string
import random
import base64
from Crypto.Cipher import AES

# Can change key to any randomly generated 16-byte key - will have no impact
# Key generated using the randKey() function from exercise #11
key = '\xba\x57\xf9\x5b\x1a\x20\x71\x67\x62\xdb\x58\x4a\x90\xa0\x75\x72'

"""
*******************************************************************************************
Checks for repeated 16 byte blocks to determine whether ECB encryption is used
(somewhat unreliable for short strings).
*******************************************************************************************
"""
def detect( ciphertext ):
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
Randomly generates a string of 1-15 bytes for padding. 
*******************************************************************************************
"""
def genPadding():
    length = random.randint( 1, 15 )
    pad = [0]*length
    for i in range ( 0, length ):
        pad[i] = chr( random.randint( 0, 255 ) )  
    return string.join( pad, "" )

"""
*******************************************************************************************
Sends strings of 'A', 'AA', 'AAA' etc. until the first 16-byte blocks match (giving us the
length of the unknownprefix). Returns a string of As we can append to the prefix to 
complete the first block.
*******************************************************************************************
"""
def padLength( decoded, randPrefix ):
    padPrefix = ['A']
    encryptedString = ecbEncrypt( randPrefix + string.join( padPrefix, '' ), decoded )
    prior = ''
    while ( encryptedString[0:16] != prior[0:16] ):
        padPrefix.append( 'A' )
        prior = encryptedString
        encryptedString = ecbEncrypt( randPrefix + string.join( padPrefix, '' ), decoded )
    return string.join( padPrefix, '' )[:-1]  

"""
*******************************************************************************************
Creates a library (list) of encrypted strings for each variation of the one byte short block.
Ex. AAAAAAAAAAAAAAAB, AAAAAAAAAAAAAAAC, etc. This library varies in the second block only,
due to the prefix block.
*******************************************************************************************
"""
def genLibrary( inputStr, prefix ):
    resultBlocks = list()
    for i in range ( 32, 127 ):   
        inputPrefix = prefix + string.join( ['A']*15, '') + chr( i )
        resultBlocks.append( ecbEncrypt( inputPrefix, inputStr ))
    return resultBlocks             

"""
*******************************************************************************************
Automated function - calls padPrefix() to determine how many bytes are needed to complete
the first block. Then uses standard byte-at-a-time ECB decryption on the second block.
*******************************************************************************************
"""
def automate( randPrefix, decoded ):
    padPrefix = padLength( decoded, randPrefix )
    library = genLibrary( decoded, randPrefix + padPrefix )

# Loops through each character of the decoded text appending it to the one byte short sequence
# Compares the block generated (second block of encrypted text) after ECB encryption to our 
# library, adds the result to our decrypted string.
    decryptedString = ''
    for j in range ( 0, len( decoded ) ):       
        encryptedBlock = ecbEncrypt( randPrefix + padPrefix + string.join( ['A']*15, '' ), decoded[j:] )  
        for k in range ( 0, len( library ) ):
            if encryptedBlock[16:32] in library[k]:
                decryptedString = decryptedString + chr( k + 32 )
    print decryptedString

"""
*******************************************************************************************
Oracle function - reads a user input, and prepends the random prefix. Encrypts and prints
the result.
*******************************************************************************************
"""
def oracle( randPrefix, decoded ):
    print "\nEnter a string to encrypt, or 'quit' to exit: \n"
    inputStr = raw_input("=> ")
    while ( inputStr != "quit" ):
        encrypted = base64.b64encode( ecbEncrypt( randPrefix + inputStr, decoded ) )
        print encrypted
        detect( encrypted ) 
        inputStr = raw_input("\n=> ")

"""
*******************************************************************************************
Main - reads a base64 encoded sequence from a file. Randomly generates a 1-15 byte prefix 
for encryption. Calls both the automated solution and the oracle function for manually 
testing the functionality.
*******************************************************************************************
"""
def main():
    with open( 'input12.txt' ) as f:
        ciphertext = f.read()
    decoded = base64.b64decode( ciphertext )
    randPrefix = genPadding()
    automate( randPrefix, decoded )
    oracle( randPrefix, decoded )

if __name__=='__main__':
    main()