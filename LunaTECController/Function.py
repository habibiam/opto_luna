'''
Created on Jul 21, 2016

@author: Xianguang Yan

Description: This is were the string is created to send to the Driver

'''

import binascii

"""
Not Used in Anything as of Right Now
Description: number to hex converter this works for negative values as well
val = value
nbits = number of bits for 64 bit two's compliment
ex: input: tohex(-199703103, 64)
returns: fffffffff418c5c1L

Input: val = value, nbits = bits
Return: String in the specified bits

"""
def tohex(val, nbits):
    return str(hex((val + (1 << nbits)) % (1 << nbits)))[2:]

"""

Description: This is just a helper funciton that checks if you inputed 4 bytes into the right get_command function (not complete for checking)
    if it fails to recieve a correct 4 byte  command it will return 0000
Input: 4 byte string
Return: 4byte string or 0000

"""
def get_value(value_input):
    number = 0
    for count in value_input:
        number += 1
    if number == 4:
        return value_input
    else:
        return "0000"

"""
Description: Gets the check sum
Check Sum is Calculated as the following:
    convert all characters into ascii numbers
    add all the characters up
    shrink it to 2 bytes
    and then convert to hex
*Note it ignores the first byte as the formate expects an * as the startbit
Input: String with start bit
Output: 2 byte check sum in string
"""

def get_checksum(string_input):
    sum = 0
    curString = string_input[1:]
    for a in curString:
        sum += ord(a) 
    sum = sum % 256
    return str(hex(sum)[2:])

"""

Description: Gets the command string to input to the Driver
Format: *CCDDDDSS/r
CC = 2 Byte Command
DDDD = 4 Byte Value
SS = CheckSum

Input: command = 2 hex value in a string, value = 4 byte hex value in a string
example get_command("10", "0000")

Output: = the Format (see above)

"""
def get_command(command, value):
    stringInput = "*"
    stringInput += command #Command
    stringInput += get_value(value) #Gets value
    stringInput += get_checksum(stringInput) #Gets Checksum
    stringInput += "\x0d"
    print stringInput

    return stringInput

"""
Description: Unused
"""
def padHex(value):
    return value
    