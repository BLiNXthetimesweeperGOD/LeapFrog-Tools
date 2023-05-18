# Leapster-Tools
Contains (incomplete) tools for splitting original Leapster, L-MAX and Leapster 2 ROMs for analysis and reverse engineering purposes.
Supports the following ROM types:
- BIOS (BaseROM)
- Cartridge (the games and Leapster 2 kiosk demo cartridges you'd find in places like Toys 'R Us)
- SD card (Leapster 2 had a bunch of downloadable games which get loaded into RAM when launched)

# Leapster memory map
Each ROM type has a different base address in memory.
- SDRM - 0x3C000000 (System RAM. Internally referred to as "SDRAM".)
- SDCD - 0x3C800000 ("SDCD" is "SD CarD". Leapster 2 SD Card games are mapped here.)
- BIOS - 0x40000000 (Where the BaseROM is mapped in memory)
- CART - 0x80000000 ("CART" is "CARTridge". Cartridge games are mapped here.)

# Unused memory range and what it was probably for
The Leapster's manufacturing test screen has 3 or 4 cartridge ports listed with only one of them actually functioning. They were likely mapped to the following addresses:
- 0x50000000
- 0x60000000
- 0x70000000

# How to use
To split any non-Torus Games ROM, use LeapSplit 5. 
To split the following games from Torus Games and get their DPAK files, use LeapSplit 6 (might also partially work on a few GBA titles that used this too):
- Counting on Zero: Numbers on the Run
- Cars
- Cars: Supercharged
- Cars 2 (might not be from Torus, needs to be checked)
- Sonic X
- Go, Diego Go! Animal Rescuer

(MAME just calls the first one "Numbers on the Run", but the internal name for the ROM is "Counting on Zero" which tells me that's supposed to be the main title.)

# What needs work
The code could be cleaner, how the voice data ends still needs to be figured out and a ton of the pointer lists still need to be implemented. One of the end goals will be to split every single piece of data out of the ROMs in a way that allows us to rebuild the said ROMs.
Maybe some more conversion would be nice. A small part of the Leapster music data needs to be figured out still.
