import struct
import os
from tkinter import filedialog
from tkinter import * #import filedialog as fd
#Pointer types
TIN = ["UNKNOWN0", #"TIN" stands for "Title INfo". ID 0
       "UNKNOWN1", #ID 1
       "UNKNOWN2_Some sort of game ID 1?",#ID 2
       "UNKNOWN3_Some sort of game ID 2?",#ID 3
       "Approved content check string 1",#ID 4
       "Approved content check string 2",#ID 5
       "Approved content check string 3",#ID 6
       "Game version",#ID 7
       "Copyright LeapFrog text",#ID 8
       "UNKNOWN9",#ID 9
       "Product number",#ID 10
       "Game name",#ID 11
       "Compiler version",#ID 12
       "Machine used to compile with username",#ID 13
       "Username",#ID 14
       "Build date",#ID 15
       "Unknown encoded data",#ID 16
       "UNKNOWN17",#ID 17
       "UNKNOWN18",#ID 18
       "UNKNOWN19"]#ID 19
LTP = ["UNKNOWN0","UNKNOWN1","UNKNOWN2","Title info","UNKNOWN4","UNKNOWN5","File pointer lists","UNKNOWN7","UNKNOWN8","UNKNOWN9","UNKNOWN10","UNKNOWN11","UNKNOWN12","UNKNOWN13","UNKNOWN14","UNKNOWN15","UNKNOWN16","UNKNOWN17","UNKNOWN18"]
LNM = ["UNKNOWN0",#0
       "UNKNOWN1",#1
       "UNKNOWN2",#2
       "UNKNOWN3",#3
       "LFC",#4
       "RAW",#5
       "SYN",#6
       "SWF/DATA",#7
       "UNKNOWN8",#8
       "SWF/DATA",#9
       "UNKNOWN10",#10
       "UNKNOWN11",#11
       "UNKNOWN12",#12
       "UNKNOWN13",#13
       "UNKNOWN14",#14
       "UNKNOWN15",#15
       "UNKNOWN16",#16
       "UNKNOWN17",#17
       "UNKNOWN18",#18
       "UNKNOWN19",#19
       "UNKNOWN20"]#20
LFHD = []
PTRS = []
CELP = []
MUSP = []
DATP = []
SWFP = []
DATS = []
MID = 0
SND = 0
CEL = 0
SWF = 0
TOTLFM = 0
FIL = 0
GAMT = 0
CHEK = 0
MUS = 32768
SWF = 2147483648
SHFT = 0
SDCD = 0x3C800000
BIOS = 0x40000000
CART = 0x80000000
root = Tk()
#button = root.Button("test", **option)
root.F = filedialog.askopenfilenames(title = "Select file",filetypes = (("Leapster ROMs","*.bin"),("all files","*.*")))
GNM = ""
OUTPUTMUS1 = False
for F in root.F:
    LFHD = []
    PTRS = []
    CELP = []
    MUSP = []
    DATP = []
    SWFP = []
    DATS = []
    NOREPEATS = [] #Used to prevent repeated file extractions because games tend to reference the same data more than once.
    MID = 0
    SND = 0
    CEL = 0
    SWF = 0
    FIL = 0
    GAMT = 0
    LAST = 0
    LASTLFC = 0
    LASTWAV = 0
    LASTSWF = 0
    LASTLFMID = 0
    CHEK = 0
    if len(F) < 1:
        quit("Didn't open a file.")
    ON = F.split("/")
    ON2 = ON[len(ON)-1]
    fld = str(ON2.split(".")[0])
    fld2 = str(fld.split("(")[0])
    fld2 = str(fld2.split(",")[0])
    #Cleaned this up. Path IDs are listed to make it easier to make code reference them. paths[0] is the root folder while paths[2] is the Flash movies folder just as some examples.
    paths = [str(os.getcwd())+"/GAMES/%s/" % (fld),                #ID 0: The root folder where assets and game info gets extracted to. (needs work, the info.txt file generation is broken and some info doesn't get written.)
             str(os.getcwd())+"/GAMES/%s/UNKNOWN/" % (fld),        #ID 1: The unknown data (needs work, the script only gets one set of files here...)
             str(os.getcwd())+"/GAMES/%s/FLASH/" % (fld),          #ID 2: Flash movies (SWF files)
             str(os.getcwd())+"/GAMES/%s/SOUNDS_WAV/" % (fld),     #ID 3: Sounds with a WAV header added so you can listen to them
             str(os.getcwd())+"/GAMES/%s/VOICES/" % (fld),         #ID 4: Voice files (no idea how they work yet, so the extraction process is a bit messy...)
             str(os.getcwd())+"/GAMES/%s/MUSIC/" % (fld),          #ID 5: The music sequences. They're internally referred to as "SYN" files in the BIOS ROMs while cartridge ROMs use the "LF_BGMIDI" and "LF_FGMIDI" commands to play them. These aren't MIDI files at all.
             str(os.getcwd())+"/GAMES/%s/SOUNDS_RAW/" % (fld),     #ID 6: Sounds (no WAV header added)
             str(os.getcwd())+"/GAMES/%s/OTHER/" % (fld),          #ID 7: Where known formats (that get used by specific games) will get saved to. DPAK from Torus Games being a good example.
             str(os.getcwd())+"/GAMES/%s/OTHER/EXTRACTED/" % (fld),#ID 8: Where known, extractable formats (like packages) get extracted to.
             #str(os.getcwd())+"/GAMES/%s/OFFSETS/" % (fld),       #ID 9: Where extra game info gets stored (text files containing file offsets for each extracted file). Could be useful for rebuilding the ROMs in the future.
             #str(os.getcwd())+"/GAMES/%s/HEADER_DATA/" % (fld),   #ID 10: If I ever decide to make the script extract the raw header data, this is where it will go. Could be useful for rebuilding the ROMs in the future. (Needed because the NOREPEATS list will aim to stop double extractions from happening)
             ]

    for path in paths:
        try:
            os.makedirs(path)
        except:
            ""
    H = open(paths[0]+"/GAMEINFO.txt", "w")
    f = open(F, "r+b")
    start = f.tell() #Save our offset. Time to scan for various files that I have no other idea on how to detect.
    scan = ""
    if os.path.basename(F).startswith("Learning") == False and os.path.basename(F).startswith("152") == False and os.path.basename(F).startswith("leapster") == False and os.path.basename(F).startswith("Cosmic") == False:
        print("Test passed")
        try:
            while scan != "DPAK":
                try:
                    scan = f.read(4).decode("UTF-8")
                except:
                    "Not a valid string, I know... This exception is to prevent Python from killing the DPAK search early without having to add extra code."
                    try:
                        f.read(4)
                        f.seek(-4, 1)
                    except:
                        print("End of file reached. Ending the scan.")
                        break
                    
            f.seek(-4, 1)
            DPAKOffset = f.tell()
            try:
                f.read(4)
            except:
                break
            DATACOUNT = struct.unpack("<H", f.read(2))[0]
            TORUS = f.read(5).decode("UTF-8")
            DATA = f.read(5)
            for i in range(DATACOUNT): #Get the last pointer in the list and add the size of the referenced data to the offset to get the full DPAK's size
                try:
                    DATA = f.read(4)
                    DATAOFFSET = struct.unpack("<I", f.read(4))[0]
                    DATASIZE = struct.unpack("<I", f.read(4))[0]
                    DATA = f.read(4)
                    FileSize = DATAOFFSET+DATASIZE
                except:
                    break
            f.seek(DPAKOffset)
            DATA = f.read(FileSize)
            with open(paths[7]+"DATA.DPAK", "w+b") as o: #Split the DPAK file from the ROM
                o.write(DATA)
                o.flush()
                o.close()
            with open(paths[7]+"DATA.DPAK", "r+b") as o: #Extract the contents from the DPAK file
                try:
                    o.read(4)
                    DATACOUNT = struct.unpack("<H", o.read(2))[0]
                    TORUS = o.read(5).decode("UTF-8")
                    DATA = o.read(5)
                    for i in range(DATACOUNT): #Get the last pointer in the list and add the size of the referenced data to the offset to get the full DPAK's size
                        DATA = o.read(4)
                        DATAOFFSET = struct.unpack("<I", o.read(4))[0]
                        DATASIZE = struct.unpack("<I", o.read(4))[0]
                        DATA = o.read(4)
                        Type = ""
                        JumpBack = o.tell() #Save our current offset for later so we can just split the file already
                        o.seek(DATAOFFSET)
                        with open(paths[8]+"DPAK_SPLIT%d.bin" % (i), "w+b") as split_file:
                            try:
                                Type = o.read(4).decode("UTF-8")
                                o.seek(-4, 1)
                            except:
                                "Not an SPRT section"
                                o.seek(-4, 1)
                            split_file.write(o.read(DATASIZE))
                            split_file.flush()
                            split_file.close()
                            if Type == "SPRT":
                                try:
                                    os.rename(paths[8]+"DPAK_SPLIT%d.bin" % (i), paths[8]+"DPAK_SPLIT%d.SPRT" % (i))
                                except:
                                    "Already exists."
                                    os.remove(paths[8]+"DPAK_SPLIT%d.bin" % (i))
                            if Type == "MDE7":
                                try:
                                    os.rename(paths[8]+"DPAK_SPLIT%d.bin" % (i), paths[8]+"DPAK_SPLIT%d.MDE7" % (i))
                                except:
                                    "Already exists."
                                    os.remove(paths[8]+"DPAK_SPLIT%d.bin" % (i))
                        o.seek(JumpBack)
                except:
                    print("I ran into an error while splitting the DPAK file...")
                    
            print("This game is from Torus Games. The DPAK (game assets) file has been split from the ROM.")
        except:
            "There's no DPAK file in this ROM. In other words, this isn't a game from Torus Games. Carry on."
    f.seek(start)
    G = f.read(4)
    while G != b'LEAP':
        G = f.read(4)
    if f.tell() > 0x100:
        f.seek(-8, 1)
        GAMT = 1
    else:
        f.seek(-4,1)
        print(f.tell())
        ROMTYPE = 0x80000000
        GAMT = 0
        
    if f.tell() == 0:
        ROMTYPE = 0x80000000
    if f.tell() == 0x140:
        ROMTYPE = struct.unpack("<I", f.read(4))[0]-0x144
    f.read(4)
    if ROMTYPE == SDCD:
        SHFT = SDCD
    if ROMTYPE == BIOS:
        SHFT = BIOS
    if ROMTYPE == CART:
        SHFT = CART
    LEN = f.read(4)[2]
    f.read(0x18)
    CHEK += 1
    #Get start offsets for later lists
    for i in range(LEN+1):
        CHEK += 1
        DAT = f.read(4)
        DATS.append(DAT)
        PTR = struct.unpack("<I", f.read(4))[0]-SHFT
        PTRS.append(PTR)

    for i in range(len(PTRS)):
        if PTRS[i] > 0:
            f.seek(PTRS[i])
        DAT2 = 2
        #Get title info
        if DATS[i][0] == 3:
            for Z in range(DATS[i][2]):
                DAT = f.read(4)[0]
                PTR = struct.unpack("<I", f.read(4))[0]
                if PTR > SHFT:
                    PTR -= SHFT
                OLD = f.tell()
                txt = ""
                if DAT in range(4,12):
                    ""
                    if DAT != 8 and GAMT == 1:
                        print("Start offset for %s:" % (TIN[DAT]), hex(PTR))
                    if GAMT == 0:
                        print("Start offset for %s:" % (TIN[DAT]), hex(PTR))
                    #print("___________________________________________")
                if DAT in range(4,16) and str(TIN[DAT]).startswith("UNKNOWN") == False:
                    txt = ""
                    A = b'1'
                    B = ""
                    f.seek(PTR)
                    while A[0] != 0:
                        A = f.read(1)
                        if A[0] != 0:
                            B = str(A).split("'")[1]
                            txt = txt+B
                    if TIN[DAT].startswith("Approved") == True:
                        txt = "Message %d: " % (DAT-3)+txt+"\n"
                        H.write(txt)
                        H.flush()
                    if TIN[DAT].startswith("Approved") != True:
                        #if DAT != 8 and GAMT == 1:
                        #    print(TIN[DAT]+":",txt)
                        if DAT == 7:
                            print(TIN[DAT]+":",txt)
                            txt = "Version: "+txt
                        if DAT == 8: #Copyright string? Doesn't read for some reason.
                            print(TIN[DAT]+":",txt)
                            txt = ""
                        if DAT == 9: #Unknown. Isn't text though.
                            print(TIN[DAT]+":",txt)
                            txt = ""
                        if DAT == 10:
                            print(TIN[DAT]+":",txt)
                            txt = "Product: "+txt
                        if DAT == 12:
                            print(TIN[DAT]+":",txt)
                            txt = "Compiler version: "+txt
                        if DAT == 13:
                            print(TIN[DAT]+":",txt)
                            txt = "Compiler machine: "+txt
                        if DAT == 14:
                            print(TIN[DAT]+":",txt)
                            txt = "Compiler username: "+txt
                        if DAT == 15:
                            print(TIN[DAT]+":",txt)
                            txt = "Build date: "+txt
                        if DAT == 16:
                            print(TIN[DAT]+":",txt)
                            txt = "Unknown encoded data: "+txt
                        if GAMT == 0:
                            print(TIN[DAT]+":",txt)
                        if DAT == 11:
                            txt = "Name: "+txt
                        if DAT == 11:
                            GNM = str(txt)
                            if ":" in GNM or '"' in GNM or "/" in GNM or "\\" in GNM or "'" in GNM:
                                try:
                                    GNM.replace(":", "")
                                except:
                                    ""
                                try:
                                    GNM.replace('"', '')
                                except:
                                    ""
                                try:
                                    GNM.replace("/", "")
                                except:
                                    ""
                                try:
                                    GNM.replace("\\", "")
                                except:
                                    ""
                                try:
                                    GNM.replace("'", "")
                                except:
                                    ""
                            
                        H.write(txt+'\n')
                        H.flush()
                f.seek(OLD)
        #End title info
        if DATS[i][0] == 3:
            print("\n___________________________________________\nEND OF GAME INFO\n___________________________________________\n")
        if DATS[i][0] == 6:
            
            for ZZ in range(DATS[i][2]):
                
                DAT = f.read(4)[0]
                PTR = struct.unpack("<I", f.read(4))[0]
                OLD = f.tell()
                if PTR > SHFT:
                    PTR -= SHFT
                    f.seek(PTR)
                #Get SWF files and various other assets
                if DAT in range(7, 15):
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    NUMB = struct.unpack("<I", f.read(4))[0]
                    for R in range(int(NUMB)):
                        try:
                            PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                            #print(hex(PT_1))
                            OG = f.tell()
                            f.seek(PT_1)
                            if f.read(4) == b'\x46\x57\x53\x05':
                                SIZ = struct.unpack("<I", f.read(4))[0]
                                f.seek(-8,1)
                                DATA = f.read(SIZ)
                                O = open(paths[2]+"output%d.SWF" % (LASTSWF), "w+b")
                                O.write(DATA)
                                O.flush()
                                O.close()
                                f.seek(OG)
                                LASTSWF+=1
                                #print("FoundSWF")
                            else:
                                DATP = []
                                f.seek(OG-4)
                                print(OG)
                                for R1 in range(int(NUMB)):
                                    PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                                    DATP.append(PT_1)
                                DATP.sort()
                                for R2 in range(len(DATP)-1):
                                    try:
                                        f.seek(DATP[R2])
                                        DATA = f.read(DATP[R2+1]-DATP[R2])
                                        O = open(paths[1]+"output%d.bin" % (LAST), "w+b")
                                        O.write(DATA)
                                        O.flush()
                                        O.close()
                                        f.seek(OG)
                                        LAST+=1
                                    except:
                                        ""#print("Error")
                        except:
                            f.seek(OG)
                #Get compressed voice clips
                if DAT == 4:
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    print("Voices are at", hex(f.tell()))
                    NUMB = struct.unpack("<I", f.read(4))[0]
                    for R in range(int(NUMB)):
                        PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                        OFF = f.tell()
                        f.seek(PT_1)
                        CHK = 0
                        O = open(paths[4]+"output%d.LFC" % (LASTLFC), "w+b")
                        while CHK != b'\xC0\x0F':
                            DATA = f.read(2)
                            CHK = DATA
                            O.write(DATA)
                        DATA = f.read(0x640) #Read some extra data and add it to the file just in case (a few voice clips got cut out very early)
                        O.write(DATA)
                        O.flush()
                        O.close()
                        f.seek(OFF)
                        LASTLFC+=1
                #Get sound effects
                if DAT == 5:
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    NUMB = struct.unpack("<I", f.read(4))[0]
                    
                    for R in range(int(NUMB)):
                        PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                        PT_2 = struct.unpack("<I", f.read(4))[0]-SHFT
                        OG = f.tell()
                        f.seek(PT_1)
                        LNG = PT_2-PT_1
                        DATA = f.read(LNG)
                        if DATA[0] == 0x4C and DATA[1] == 0x46 and DATA[2] == 0x5F:
                            print("Bad word list found")
                            f.seek(OG-8)
                            
                            for R2 in range(int(NUMB)):
                                PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                                OG = f.tell()
                                txt = ""
                                A = f.read(1)
                                f.seek(-1,1)
                                while A[0] != 0:
                                    A = f.read(1)
                                    B = str(A).split("'")[1]
                                    txt = txt+B
                                txt = txt+'\n'
                            O = open(paths[0]+"BadWordsList.txt", "w+")
                            O.write(txt)
                            O.flush()
                            O.close()
                            break
                        with open(paths[3]+"output%d.WAV" % (LASTWAV), "w+b") as O: #Write the sounds to the SOUNDS_WAV folder (basically converts them to WAV files)
                            O.write(b'RIFF')
                            O.write(struct.pack("<I",LNG))
                            O.write(b'WAVEfmt ')
                            O.write(b'\x14\x00\x00\x00')
                            O.write(b'\x06\x00\x01\x00\x40\x1F\x00\x00\x40\x1F\x00\x00\x01\x00\x08\x00\x00\x00\x00\x00')
                            O.write(b'fact\x04\x00\x00\x00')
                            O.write(struct.pack("<I",LNG))
                            O.write(b'data')
                            O.write(DATA)
                            O.flush()
                            O.close()
                        with open(paths[6]+"output%d.BIN" % (LASTWAV), 'w+b') as O2: #Write the sounds to the SOUNDS folder
                            O2.write(DATA)
                            O2.flush()
                        f.seek(OG) #Go back to the pointer list to get the next sound
                        LASTWAV+=1
                #Get SYN ("LF_BGMIDI" and"LF_FGMIDI") data
                if DAT == 6:
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    struct.unpack("<I", f.read(4))[0]
                    NUMB = struct.unpack("<I", f.read(4))[0]
                    if NUMB not in MUSP:
                        for R in range(int(NUMB)):
                            PT_1 = struct.unpack("<I", f.read(4))[0]-SHFT
                            OG = f.tell()
                            f.seek(PT_1)
                            f.read(2)
                            CHCT = f.read(2)[0]
                            SIZ = CHCT*2+2
                            for LL in range(CHCT):
                                CHO = struct.unpack("<H", f.read(2))[0]
                                CHV = f.read(2)
                            f.seek(-SIZ, 1)
                            SIZ+=CHO
                            DATA1 = f.read(CHO)
                            DATA2 = f.read(2)
                            SIZ+=2
                            while DATA2[0] != 0xFF and DATA2[1] != 0xFF:
                                DATA2 = f.read(2)
                                SIZ+=2
                            f.seek(-SIZ,1)
                            DATA = f.read(SIZ)
                            O = open(paths[5]+"output_%d.SYN" % (R), "w+b")
                            O.write(DATA)
                            O.write(b'\x00')
                            O.flush()
                            O.close()
                            if OUTPUTMUS1 == True:
                                O = open(paths[6]+"%s_output_%d.SYN" % (GNM,TOTLFM), "w+b")
                                O.write(DATA)
                                O.write(b'\x00')
                                O.flush()
                                O.close()
                                
                            f.seek(OG)
                            TOTLFM+=1
                    MUSP.append(NUMB)
                print("Start offset for %s pointer list:" % (LNM[DAT]), hex(PTR))
                
                f.seek(OLD)
        if DATS[i][0] == 6:
            print("\n___________________________________________\nEND OF GAME ASSETS\n___________________________________________\n")
    H.close()
    f.close()
