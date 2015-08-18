#!/usr/bin/python
import string
import base64
from Crypto.Cipher import AES

def main():
    with open( 'input7.txt' ) as f:
        ciphertext = f.readlines()
    cipherString = string.join( ciphertext, "" )
    decodedString = base64.b64decode( cipherString )

    decryptor = AES.new( 'YELLOW SUBMARINE', AES.MODE_ECB )
    decryptedString = decryptor.decrypt( decodedString )

# Strips padding off the end for clean printing
    print decryptedString[0:-4]    

if __name__=='__main__':
      main()