'''
Created on Jul 21, 2016

@author: Xianguang Yan

'''

import binascii

def tohex(val, nbits):
    return str(hex((val + (1 << nbits)) % (1 << nbits)))[2:]

def get_value(value_input):
    number = 0
    for count in value_input:
        number += 1
    if number == 4:
        return value_input
    else:
        return "0000"

def get_checksum(string_input):
    sum = 0
    curString = string_input[1:]
    for a in curString:
        sum += ord(a) 
    sum = sum % 256
    return str(hex(sum)[2:])

def get_command(command, value):
    stringInput = "*"
    stringInput += command #Command
    stringInput += get_value(value) #Gets value
    stringInput += get_checksum(stringInput) #Gets Checksum
    stringInput += "\x0d"
    print stringInput

    return stringInput

def padHex(value):
    return value
    