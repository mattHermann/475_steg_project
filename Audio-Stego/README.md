# LSB Stegonography for .WAV Files (EECS 475)

This repo includes audio_lsb_enc.py which is used in order to encode data into a .WAV file and audio_lsb_dec.py 
which is used to recover the data from the .WAV file. For convenience, some demo files were included. The file waiting_for_grades.wav 
is an untouched audio file while output.wav has a secret message embedded within it.

## Encoding Process:
The encoding process is as simple as running audio_lsb_enc.py on the file you are tring to encode. 
### Usage:
```console
$python3 lsb_enc.py [AUDIO_FILE] [OUTPUT_FILE] [HIDDEN_DATA]
```

## Decoding Process:
The decoding process is similarly simple, just run audio_lsb_dec.py on the file that has the hidden message with
the number of bytes to read out. 
## Usage:

```console
$python3 dec.py [AUDIO_FILE] [NUM_BYTES]
```
