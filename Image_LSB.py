from PIL import Image, ImageFilter
from base64 import b64encode
import secrets
import string
import sys, getopt
import os, codecs
import numpy as np
import random
import math


def otp_encrypt(plaintext_msg):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(alphabet) for i in range(len(plaintext_msg)))


    encrypted_msg = ''

    for i in range(len(plaintext_msg)):
        c_bit = ord(plaintext_msg[i]) ^ ord(key[i])
        encrypted_msg += chr(c_bit)

    return encrypted_msg, key

def otp_decrypt(otp_msg, key):
    decrypted_msg = ''

    for i in range(len(key)):
        c_bit = ord(otp_msg[i]) ^ ord(key[i])
        decrypted_msg += chr(c_bit)
    
    return decrypted_msg



def get_new_color(color, msg_bits, bit_index, total_bits):
    #encode LSB if the entire message has not been encoded
    if (bit_index < total_bits):
        color_bin = bin(color)
        new_color_bin = color_bin[:-1] + msg_bits[bit_index]
        bit_index += 1
        return int(new_color_bin, 2), bit_index
    else:
        return color, bit_index

def pad_zeros(input):
    if len(input) < 7:
        input = '0'*(7-len(input))+input
    return input

def encode(img):
    plaintext_msg = input('>Please type the message your wish to encode: ')
    otp_msg, key = otp_encrypt(plaintext_msg)

    msg_bits = ''.join(pad_zeros(format(ord(i), 'b')) for i in otp_msg)

    bit_index = 0
    total_bits = len(msg_bits)

    width, height = img.size


    if (total_bits > (width * height * 3)):
        max_msg_size = math.floor((width * height * 3) / 7)
        print("Message is too long to encode, Max message size for this image is:", max_msg_size, "characters")
        sys.exit(2)

    pixel_arr = img.load()

    stego_im = Image.new(img.mode, img.size)
    stego_pixels = stego_im.load()

    for i in range(width):
        for j in range(height):
            r,g,b = pixel_arr[i,j]

            new_r, bit_index = get_new_color(r, msg_bits, bit_index, total_bits)
            new_g, bit_index = get_new_color(g, msg_bits, bit_index, total_bits)
            new_b, bit_index = get_new_color(b, msg_bits, bit_index, total_bits)

            stego_pixels[i,j] = (new_r, new_g, new_b)
    
    print("Success! The encryption key is:", key)
    print("The encoded image has beed saved to steg.png")
    stego_im.save('steg.png')

def get_LSB(color):
    color_bin = bin(color)
    return color_bin[-1]

def decode(img):
    width, height = img.size
    pixel_arr = img.load()

    msg_bits = ''

    for i in range(width):
        for j in range(height):
            r,g,b = pixel_arr[i,j]
            msg_bits += get_LSB(r)
            msg_bits += get_LSB(g)
            msg_bits += get_LSB(b)

    #decoding data for binary string
    otp_str = ''
    for i in range(0, len(msg_bits), 7):
        split_bin_data = msg_bits[i:i + 7]
        split_dec = int(split_bin_data, 2)
        otp_str = otp_str + chr(split_dec)

    key = input(">Please enter the encryption key: ")
    decrypted_msg = otp_decrypt(otp_str, key)

    print("The decoded string is:", decrypted_msg)


def main(argv):
    input_image = ''
    output_file = ''
    if( len(sys.argv) != 2 ):
        print("USAGE: Image_LSB.py <input_image>")
        sys.exit(2)

    input_file = sys.argv[1]
    img = Image.open(input_file, 'r')

    while(True):
	    mode_num = input('>Which Mode? 1) encode 2) decode: ')
	    if(mode_num == '1'):
	        encode(img)
	        sys.exit()
	    elif(mode_num == '2'):
	        decode(img)
	        sys.exit()
	    else:
	        print("Invalid Mode Number")

if __name__=="__main__":
    main(sys.argv[1:])

