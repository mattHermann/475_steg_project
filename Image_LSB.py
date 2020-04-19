from PIL import Image, ImageFilter
import sys, getopt
import numpy as np
import math


def get_new_color(color, msg_bytes, bit_index, total_bits):
	#encode LSB if the entire message has not been encoded
	if (bit_index < total_bits):
		color_bin = bin(color)
		new_color_bin = color_bin[:-1] + msg_bytes[bit_index]
		bit_index += 1
		return int(new_color_bin, 2), bit_index
	else:
		return color, bit_index

def encode(img):
	plaintext_msg = input('>Please type the message your wish to enocde: ')

	msg_bytes = ''.join(format(ord(i), 'b') for i in plaintext_msg) 
	print(msg_bytes)

	bit_index = 0
	total_bits = len(msg_bytes)

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

			new_r, bit_index = get_new_color(r, msg_bytes, bit_index, total_bits)
			new_g, bit_index = get_new_color(g, msg_bytes, bit_index, total_bits)
			new_b, bit_index = get_new_color(b, msg_bytes, bit_index, total_bits)

			stego_pixels[i,j] = (new_r, new_g, new_b)
	
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

	print(msg_bits[:10])

	#decoding data for binary string
	decoded_str = ''
	for i in range(0, len(msg_bits), 7): 
		split_bin_data = msg_bits[i:i + 7] 
		split_dec = int(split_bin_data, 2) 
		decoded_str = decoded_str + chr(split_dec)  


	print("The decoded string is:", decoded_str[:10])


def main(argv):
	input_image = ''
	output_file = ''
	if( len(sys.argv) != 2 ):
		print("USAGE: Image_LSB.py <input_image>")
		sys.exit(2)

	input_file = sys.argv[1]
	img = Image.open(input_file, 'r')

	mode_num = input('>Which Mode? 1) encode 2) decode: ') 
	if(mode_num == '1'):
		encode(img)
	elif(mode_num == '2'):
		decode(img)
	else:
		print("Invalid Mode Number")
		sys.exit(2)

if __name__=="__main__":
    main(sys.argv[1:])