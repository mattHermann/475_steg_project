import wave
import sys

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result
    
def encode(filename, outfile, metadata):
    code = tobits(metadata)
    
    audio = wave.open(filename, 'rb')
    
    n_frames = audio.getnframes()
    output = []
    data = audio.readframes(n_frames)
    n_bytes = len(data)
    
    for x in range(n_bytes):
        output.append(0)
    
    for j in range(n_bytes):
        if len(code) > j:
            if code[j] == 1:
                if data[j] % 2 == 0:
                    new_byte = data[j] + 1
                else:
                    new_byte = data[j]
                output[j] = new_byte
                
            else:
                if data[j] % 2 == 1:
                    new_byte = data[j] - 1
                else:
                    new_byte = data[j]
                output[j] = new_byte
        else:
            output[j] = data[j]
        
    out = wave.open(outfile, 'wb')
    out.setframerate(audio.getframerate())
    out.setnchannels(audio.getnchannels())
    out.setsampwidth(audio.getsampwidth())

    out.writeframes(bytes(output))
    
    out.close()
    audio.close()
    
def main():
    if len(sys.argv) != 4:
        print ("Bad syntax")
        print ("Correct usage: python3 lsb_enc.py [AUDIO_FILE] [OUTPUT_FILE] [HIDDEN_DATA]")
        return

    audio_file = sys.argv[1]
    output_name = sys.argv[2]
    text = sys.argv[3]
    
    encode(audio_file, output_name, text)    
  
if __name__ == '__main__':
    main()
      
    
    
    
    