# bnk-extractor-with-TSV-parsing
extracts .bnk files to wav and ogg and organises them using the TSV included with the .bnk

uses [bnkextr](https://github.com/eXpl0it3r/bnkextr) to extract the banks, parses the TSV information to organise and name the files. exports wems as wavs and oggs.

##Usage
- Place .bnk file and the accociated TSV (in the folder as the bnk as a .txt file, should share the same name as the bnk file) into the Game-Sounds folder.
- run unpack.py ``py unpack.py``
