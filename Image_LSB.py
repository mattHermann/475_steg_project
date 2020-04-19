from PIL import Image, ImageFilter
import sys, getopt
import numpy as np




def encode(img):
	plaintext_msg = input('>Please type the message your wish to enocde: ')

	msg_bytes = ''.join(format(ord(i), 'b') for i in plaintext_msg) 
	print(msg_bytes)

	byte_index = 0
	total_bytes = len(msg_bytes)

	width, height = img.size

	stego_im = Image.new(img.mode, img.size)
	stego_pixels = stego_im.load()
	pixel_arr = img.load()

	for i in range(width):
		for j in range(height):
			if (byte_index < total_bytes):
				print(pixel_arr[i,j])
				byte_index += 1
				

			else:
				stego_pixels[i,j] = pixel_arr[i,j]
	
	stego_im.save('test.jpg')

	print("encode")

def decode(img):
	pix_val = list(img.getdata())

	#decoding data for binary string
	decoded_str = ''
	for i in range(0, len(msg_bytes), 7): 
		split_bin_data = msg_bytes[i:i + 7] 
		split_dec = int(split_bin_data, 2) 
		decoded_str = decoded_str + chr(split_dec)  


	print("decode")


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