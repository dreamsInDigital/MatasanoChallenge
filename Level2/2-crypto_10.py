#!/usr/bin/python
import string
from Crypto.Cipher import AES
import base64

"""
******************************************************************************************
Generates a list containing # of bytes for padding and appends to input
******************************************************************************************
"""
def padBlock( input, blockLength, byte ):   
    padding = [byte]*( blockLength - ( len ( input ) % blockLength ) ) 
    return input + string.join( padding, '' )

"""
******************************************************************************************

******************************************************************************************
"""
def removePad( inputStr ):
    i = len( inputStr ) - 1
    flag = False
    while ( flag == False ):
        if inputStr[i] != chr( ord( '\x04' ) ):
            flag = True
        else:
            i = i - 1
    return inputStr[0:i]


"""
*******************************************************************************************
Pads if text not a multiple of the block length, then calls recursive encryptBlock function.
*******************************************************************************************
"""
def encrypt( input, IV ):
    if ( len ( input ) % len ( IV ) ) != 0 :
        input = padBlock ( input, len( IV ), '\x04' ) 
    return encryptBlock( input, IV, 0 )
    

"""
*******************************************************************************************
Encrypts each block, and then sends the result to the next call for chain encryption
by recursion.
*******************************************************************************************
"""
def encryptBlock( input, block, ix ):
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
    encryptor = AES.new( 'YELLOW SUBMARINE', AES.MODE_ECB )
    result = encryptor.encrypt( result )

# recursive call, which returns the encrypted string past this point
    partialRes = encryptBlock( input, result, ix + 16 )  
            
# appends result from call, and returns the encrypted string to this point
    return result + partialRes  



"""
*******************************************************************************************
Calls recursive function decryptBlock, as well as removePad to clean up result.
*******************************************************************************************
"""
def decrypt( input, IV ):
# call to recursive decryption function, initializes start index at 0
    return removePad( decryptBlock( input, IV, 0 )  ) 



"""
*******************************************************************************************
Sends each encrypted block to the next call for chain decryption. Decrypts and joins
blocks through a series of recursive calls.
*******************************************************************************************
"""
def decryptBlock( input, block, ix ):
# test for base case - end of input string
    if ( ix == len ( input ) ):
        return ''

# slice subBlock from main string
    xorResult = list()
    subBlock = input[ix:ix+16]

# perform ECB decryption on this chunk
    decryptor = AES.new( 'YELLOW SUBMARINE', AES.MODE_ECB )
    result = decryptor.decrypt( subBlock )

# XOR of current block with prev block ciphertext ( or IV in case of first block )  
    for i in range ( 0, len( block ) ):
        xorResult.append( chr( ord( result[i] ) ^ ord( block[i] ) ) )
    xorResult = string.join( xorResult, '' )

# recursive call, which returns the decrypted string past this point
    partialRes = decryptBlock( input, subBlock, ix + 16 )   
           
# appends result from call, and returns the encrypted string to this point
    return xorResult + partialRes  



"""
*******************************************************************************************
Main - makes three test calls to the above implemented encrypt/decrypt functions.
*******************************************************************************************
"""
def main():
# testing encryption functions    
    input = 'No TV and no beer make Homer something something...'
    IV = string.join( ['\x00']*16, ''  )  
    result = encrypt ( input, IV )
    print base64.b64encode( result ) + '\n'
# testing paired encryption/decryption functions on the above encrypted string
    print decrypt( result, IV ) + '\n'
# testing decryption function on given input file
    with open( 'input10.txt' ) as f:
        ciphertext = f.read()
    print decrypt( base64.b64decode( ciphertext ), IV )


if __name__=='__main__':
    main()