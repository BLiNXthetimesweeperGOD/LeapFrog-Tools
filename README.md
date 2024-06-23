(This page will stay outdated due to me doing a complete rewrite of the scripts seen here)

# Update
The LeapSplit script has been rewritten and moved to https://github.com/BLiNXthetimesweeperGOD/Leapster-Tools

This repository will no longer receive updates. I'll keep it up for historical purposes though.

# LeapFrog-Tools
Contains (incomplete) tools for splitting original Leapster, L-MAX and Leapster 2 ROMs for analysis and reverse engineering purposes. LeapPad-based toys are also being worked on (but incomplete).
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
The Leapster's manufacturing test screen has 3 or 4 cartridge ports listed with only one of them actually functioning. They were likely mapped to the following addresses (and probably weren't used for games):
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

# Submitting issues
If think you've come across an issue, please make sure it's valid! This isn't meant to emulate the Leapster or convert ROMs to be playable off of an SD card. This also doesn't convert anything yet (all the output WAV files are is the raw A-Law audio data with a header added to them). 
In other words, don't make issues like "I can't run X game with your tools!", "Can you please make an emulator?", or "Why aren't the music files being converted to MIDI?".

# Other goals for this project
- Make scripts for original (1999-2008) LeapPad ROMs, as they use a ton of the same codecs and formats as the Leapster.
- Try to add conversion for some of the formats (voice data and music being the main focus for now)
- Make documents going over what's known about the various formats so people don't have to dig through the scripts to figure it out.
- Document the various Leapster 2 SD card/RAM Drive formats (Creativity Castle, a few games without a save chip like Mr. Pencil, LeapFrog Learning Path data...)


# System support list
The following systems are planned to be supported.
- Any toy that uses the "Leap-Font" while also having a dumpable ROM
- LeapPad (1999-2008) (Including the MANY variants. Several BIOS revisions need to be dumped! Several cartridges need to be dumped!)
- Imagination Desk (2001-2002) (Not a lot of cartridges exist. BIOS needs to be dumped! Several cartridges need to be dumped!)
- My Own Learning Leap (2002) (Only has 4 cartridges. They came with books. BIOS needs to be dumped! I've dumped all 4 cartridges.)
- Turbo Twists/Extremes (2002) (Each variant has 3 or 4 cartridges)
- iQuest Handheld (2003-2005) (Not a lot of cartridges exist. The 4.0 variants are the same as the earlier ones)
- Leapster (2003-2012) (All revisions. Some cartridges and BIOS revisions still need to be dumped)
- LeapReader (Same binary format as the Leapster, but has an actual filesystem. Entirely digital. No cartridges exist.)

# Unrelated systems that won't be supported
- LeapFrog Mind Mania clips (unknown hardware, uses square waves, can't be dumped currently)
- LeapFrog ClickStart
- Crammer
- Didj, Leapster Explorer, LeapPad Explorer and LeapTV (none of these are related in any way to the Leapsters or LeapPads from the late 90's and early 2000's. They use MIDI, OGG Vorbis, WAV and MP3 for audio.)
- LeapFrog Epic and Academy (like the previous, these are entirely unrelated to the older systems.)
- LeapBand (Uses SunPlus hardware, not related to any of the previous handhelds at all)
- RockIt Twist (technically a VTech handheld. Uses a SunPlus ARM7 chip.)
- Non-LeapFrog systems like the V.Smile
