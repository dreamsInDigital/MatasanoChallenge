#!/usr/bin/python
import string

"""
******************************************************************************************
Starts at the end of the string and checks for valid padding. If valid padding found,
will strip off those characters and return a clean string. If invalid padding is found,
and exception is thrown.
******************************************************************************************
"""
def removePad( inputStr ):
    i = len( inputStr ) - 1
    flag = False
    while ( flag == False ):
        if ord( inputStr[i] ) !=  ord( '\x04' ) :
# Value x08 could be adjusted to detect different types of bad padding - left as x08 
# in this case so as not to strip carriage returns, tabs, etc.
            if ord( inputStr[i] ) < ord( '\x08' ):  
                raise Exception( 'Invalid Padding on %s' % (inputStr) )
            else:
                flag = True
        else:
            i = i - 1
    return inputStr[0:i+1]


"""
******************************************************************************************
Main - three test cases used on removePad function
******************************************************************************************
"""
def main():
    try:
        print removePad( 'ICE ICE BABY\x04\x04\x04\x04' )
        print removePad( 'ICE ICE BABY\x05\x05\x05\x05' )
    except Exception as e:
        print list( e )
        


if __name__=='__main__':
    main()