#!/usr/bin/python
import base64
import string

def main( ciphertext ):
    cipherb64 = base64.b64encode(ciphertext.decode("hex"))
    print cipherb64

if __name__=='__main__':
    ciphertext = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

    main( ciphertext )