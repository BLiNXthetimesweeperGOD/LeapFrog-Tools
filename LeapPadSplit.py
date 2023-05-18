import struct
import os
from tkinter import filedialog
from tkinter import * #import filedialog as fd
root = Tk()
#Splits LeapPad/iQuest/Imagination Desk/My Own Learning Leap/Turbo Twist/Turbo Extreme ROMs into their individual ROM banks
root.F = filedialog.askopenfilenames(title = "Select file",filetypes = (("LeapFrog ROMs","*.bin"),("all files","*.*")))
for F in root.F:
    fld = os.path.basename(F)
    paths = [str(os.getcwd())+"/GAMES/%s/" % (fld),
             str(os.getcwd())+"/GAMES/%s/BANKS/" % (fld)]

    for path in paths:
        try:
            os.makedirs(path)
        except:
            ""
    size = int(os.path.getsize(F)/0x10000)
    print(size)
    with open(F, "r+b") as f:
        for i in range(size):
            if i < 9:
                O = paths[1]+str(f"BANK0{i+1}.BIN")
            if i >=9:
                O = paths[1]+f"BANK{i+1}.BIN"
            with open(O, "w+b") as o:
                data = f.read(0x10000)
                o.write(data)
