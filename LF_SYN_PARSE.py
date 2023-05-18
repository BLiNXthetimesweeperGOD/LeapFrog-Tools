import struct
import os
from tkinter import filedialog as fd
import random
from statistics import median
#A script that aims to parse LeapFrog's "SYN" sequences. Currently only designed with the Leapster in mind.

files = fd.askopenfilenames()
try:
    os.mkdir(os.getcwd()+"/OUTPUT/")
except:
    "Path already exists."
for FILE in files:
    f = open(FILE, "r+b")
    FNAM = FILE.split("/")
    FNAM = FNAM[len(FNAM)-1]
    track = 0
    header = f.read(2)
    trackCount = struct.unpack('<H', f.read(2))[0]
    print(f"Track count: {trackCount}")
    loops = 0
    errored = False
    for i in range(trackCount):
        startOffset = struct.unpack('<H', f.read(2))[0]
        unknown = struct.unpack('<H', f.read(2))[0]
        nextInfo = f.tell()
        f.seek(startOffset)
        volume = 1
        instrument = 0
        corrected = False
        if errored == True:
            break
        print("____________________________________________________\nStart of track",i)
        byte = 0
        looppoint = 0
        ID = 0
        while byte != 0xFF:
            if byte != 0xFF:
                try:
                    byte = f.read(1)
                    byte = byte[0]
                except:
                    print("Errored out on track",i,"at offset",f.tell())
                    errored = True
                    break
            corrected = False
            if byte in range(0, 0x7F):
                try:
                    delay = f.read(1)[0]
                    if delay == 0:
                        f.seek(-1,1)
                        byte = f.read(1)[0]
                        delay = f.read(1)[0]
                        if delay == 0xFF:
                            byte = 0xFF
                        corrected = True
                    if delay != 255:
                        print("Pitch:",hex(byte),"\nDelay:",hex(delay))   
                    if delay == 255:#We hit the end of the track unexpectedly. Shouldn't happen, but it probably does in at least a few of them.
                        byte = 255
                except: #Something went horribly wrong while going through the track data.
                    break
            if byte == 0x81: #"CuePt". How it's handled is currently unknown.
                ""
                print("CuePt:",hex(byte))
            if byte == 0x82: #"CuePt". How it's handled is currently unknown.
                ""
                print("CuePt:",hex(byte))
            if byte == 0x83: #"CuePt". How it's handled is currently unknown.
                ""
                print("CuePt:",hex(byte))
            if byte == 0x84: #"CuePt". How it's handled is currently unknown.
                ""
                print("CuePt:",hex(byte))
            if byte == 0x85: #"CuePt". How it's handled is currently unknown.
                "{BadCuePtUser:%d}" #From the BIOS at the part of the code that handles this command
                print("CuePt:",hex(byte))
            if byte == 0x88: #"SynCmd". Set volume
                byte = f.read(1)[0]
                if byte in range(0x80, 0xFF): #Handles variable width values. Instruments can have IDs that are pretty large, so they added a check for this in the BIOS.
                    f.seek(-1, 1)
                    volume = struct.unpack("<H", f.read(2))[0]
                    corrected = True
                if corrected == False:
                    volume = byte
                print("Set volume:",hex(volume))
            corrected = False
            if byte == 0x89: #"SynCmd". Set instrument.
                byte = f.read(1)[0]
                if byte in range(0x80, 0xFF): #Handles variable width values. Instruments can have IDs that are pretty large, so they added a check for this in the BIOS.
                    f.seek(-1, 1)
                    instrument = struct.unpack("<H", f.read(2))[0]
                    corrected = True
                if corrected == False:
                    instrument = byte
                print("Set instrument:",hex(instrument))
            corrected = False
            if byte == 0x8A: #"SynCmd". Bends the pitch of the notes. No idea how to use it myself, but it's used a lot in tracks that do this.
                byte = hex(f.read(2)[0])
                print("Pitch bend:",hex(byte))
            if byte == 0x8E: #"SynCmd". Set loop count
                byte = hex(f.read(1)[0]) #Never gets set above 0x7F
                loops = byte
                print("Loop count:",byte)
            if byte == 0x8F: #"SynCmd". Set loop point
                byte = hex(f.read(1)[0])
                print("Loop back to start or previous marker after track ends")
            if byte == 0xFF: #End of track. Go to the next one.
                print("End of track")
                #Next byte should always be 00. 0xFF00 is the full command.
            corrected = False
        f.seek(nextInfo)
