#!/usr/bin/python
import string
import random
import base64
import collections
from Crypto.Cipher import AES
import re
import json

userId = 0

"""
*******************************************************************************************
Takes an email address and user role and creates an encoded json by calling encodeObject()
*******************************************************************************************
"""
def profile_for( email, userRole ):
    # calls function which eliminates '&' and '=' in the email input
    email = cleanInput( email )
    userRole = cleanInput( userRole )

    objStr = '{"email":"'+email+'","uid":"%i","role":"' % (userId) +userRole+'"}' 
    return encodeObj( json.loads( objStr, object_pairs_hook=collections.OrderedDict ) )

"""
*******************************************************************************************
Cleans a string input, removing all occurences of '&' and '=' 
*******************************************************************************************
"""
def cleanInput( inputStr ):
    return re.sub( '[&=]', '', inputStr )

"""
*******************************************************************************************
Creates a json object from an input string of 'foo=bar&baz=qux&zap=zazzle' format
*******************************************************************************************
"""
def createObj( inputStr ):
    params = re.sub( '[&]', ' ', inputStr ).split()
    objStr = '{'
    for i in range ( 0 , len( params ) ):
        if i > 0: objStr = objStr + ','
        objStr = objStr + '"' + params[i][:params[i].find( '=' )] + '"' 
        objStr = objStr + ':"' + params[i][params[i].find( '=' )+1:] + '"' 
    return json.loads( objStr + '}' )
 
"""
*******************************************************************************************
Takes a json object and coverts to string of 'foo=bar&baz=qux&zap=zazzle' format
*******************************************************************************************
"""  
def encodeObj( obj ):
    objStr = json.dumps( obj )
    objStr = re.sub( '[{}"]', '', objStr )
    objStr = re.sub( '[:]', '=', objStr )
    objStr = re.sub( '[,]', '&', objStr )
    return re.sub( '[ ]', '', objStr )

"""
*******************************************************************************************
Randomly generates a 16 byte key. 
*******************************************************************************************
"""
def randKey():
    global randomKey
    keyList = [0]*16
    for i in range ( 0 , 16 ):
        keyList[i] = chr( random.randint( 0, 255 ) )
    randomKey = string.join( keyList, "" )

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
Encrypts with ECB under the randomly generated key.
*******************************************************************************************
"""
def ecbEncrypt( input ):
    paddedInput = padBlock( input )
    encryptor = AES.new( randomKey, AES.MODE_ECB )
    return encryptor.encrypt( paddedInput )

def ecbDecrypt( input ):
    decryptor = AES.new(randomKey, AES.MODE_ECB )
    decrypted = decryptor.decrypt( input )
    result = ''
    for i in range ( 0, len( decrypted ) ):
        if ( decrypted[i] != '\x04' ):
            result = result + decrypted[i]
    return result

def main():
    j = createObj( 'foo=bar&baz=qux&zap=zazzle' )
    print json.dumps( j, indent=2, separators=(',', ' : ')) 
    print encodeObj( j )
    print profile_for( 'fake@fake.com', 'user' )

    randKey()

    print "Enter an email address, or 'quit' to exit: \n"
    inputStr = raw_input("Email Address => ")
    while ( inputStr != 'quit' ):
        encrypted = base64.b64encode( ecbEncrypt(inputStr) )
        print encrypted
        print ""
        inputStr = raw_input("Enter string to decrypt => ")
        inputStr = inputStr.rstrip()
        print ecbDecrypt( base64.b64decode( inputStr ) )
        print ""
        inputStr = raw_input("Email Address => ")


if __name__=='__main__':
    main()