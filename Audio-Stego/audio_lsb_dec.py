import wave
import sys

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
    
def decode(filename, length):
    audio = wave.open(filename, 'rb')

    n_frames = audio.getnframes()
    text = []
    data = audio.readframes(n_frames)
    n_bytes = len(data)
    
    for j in range(n_bytes):        
        if data[j] % 2 == 0:
            text.append(0)
        else:
            text.append(1)
    
    print(frombits(text)[:length])

    audio.close()
    
def main():
    if len(sys.argv) != 3:
        print ("Bad syntax")
        print ("Correct usage: python3 dec.py [AUDIO_FILE] [NUM_BYTES]")
        return
    audio_file = sys.argv[1]
    num_bytes = int(sys.argv[2])
    decode(audio_file, num_bytes)    
  
if __name__ == '__main__':
    main()
      
    
    
    
    