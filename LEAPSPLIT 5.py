import struct
import os
from tkinter import filedialog
from tkinter import * #import filedialog as fd
#Pointer types
TIN = ["UNKNOWN0","UNKNOWN1","UNKNOWN2_Some sort of game ID 1?","UNKNOWN3_Some sort of game ID 2?","Approved content check string 1","Approved content check string 2","Approved content check string 3","Game version","Copyright LeapFrog text","UNKNOWN9","Product number","Game name","Compiler version","Machine used to compile with username","Username","Build date","Unknown encoded data","UNKNOWN17","UNKNOWN18","UNKNOWN19"]
LTP = ["UNKNOWN0","UNKNOWN1","UNKNOWN2","Title info","UNKNOWN4","UNKNOWN5","File pointer lists","UNKNOWN7","UNKNOWN8","UNKNOWN9","UNKNOWN10","UNKNOWN11","UNKNOWN12","UNKNOWN13","UNKNOWN14","UNKNOWN15","UNKNOWN16","UNKNOWN17","UNKNOWN18"]
LNM = ["UNKNOWN0","UNKNOWN1","UNKNOWN2","UNKNOWN3","LFC","RAW","LFMIDI","SWF/DATA","UNKNOWN8","SWF/DATA","UNKNOWN10","UNKNOWN11","UNKNOWN12","UNKNOWN13","UNKNOWN14","UNKNOWN15","UNKNOWN16","UNKNOWN17","UNKNOWN18","UNKNOWN19","UNKNOWN20"]
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
    paths = [str(os.getcwd())+"/GAMES/%s/" % (fld),str(os.getcwd())+"/GAMES/%s/UNKNOWNDATA/" % (fld),str(os.getcwd())+"/GAMES/%s/SWF/" % (fld),str(os.getcwd())+"/GAMES/%s/WAV/" % (fld),str(os.getcwd())+"/GAMES/%s/LFCODEC/" % (fld),str(os.getcwd())+"/GAMES/%s/LFMIDI/" % (fld)]#,str(os.getcwd())+"/GAMES/LFM/"]

    for path in paths:
        try:
            os.makedirs(path)
        except:
            ""
    H = open(paths[0]+"/GAMEINFO.txt", "w")
    f = open(F, "r+b")
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
                if DAT in range(4,12) and str(TIN[DAT]).startswith("UNKNOWN") == False:
                    txt = ""
                    A = b'1'
                    B = ""
                    f.seek(PTR)
                    while A[0] != 0:
                        A = f.read(1)
                        if A[0] != 0:
                            B = str(A).split("'")[1]
                            txt = txt+B
                    if TIN[DAT].startswith("Approved") != True:
                        if DAT != 8 and GAMT == 1:
                            print(TIN[DAT]+":",txt)
                        if GAMT == 0:
                            print(TIN[DAT]+":",txt)
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
                if DAT == 7 or DAT == 8 or DAT == 9 or DAT == 10:
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
                        CELP.append(PT_1)
                    CELP.sort()
                    for R in range(int(NUMB)):
                        try:
                            PT_1 = CELP[R]
                            PT_2 = CELP[R+1]
                            OG = f.tell()
                            f.seek(PT_1)
                            LNG = PT_2-PT_1
                            DATA = f.read(LNG)
                            O = open(paths[4]+"output%d.LFC" % (LASTLFC), "w+b")
                            O.write(DATA)
                            O.flush()
                            O.close()
                            f.seek(OG)
                            LASTLFC+=1
                        except:
                            f.seek(OG)
                            break
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
                        O = open(paths[3]+"output%d.WAV" % (LASTWAV), "w+b")
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
                        f.seek(OG)
                        LASTWAV+=1
                #Get LFMIDI tracks
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
                            O = open(paths[5]+"output_%d.LFM" % (R), "w+b")
                            O.write(DATA)
                            O.write(b'\x00')
                            O.flush()
                            O.close()
                            if OUTPUTMUS1 == True:
                                O = open(paths[6]+"%s_output_%d.LFM" % (GNM,TOTLFM), "w+b")
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
