# fih
usage: fih.py [-h] [-N NAME] [-I INITIAL] [-S START] [-T TO] [-M MAKE] [-C CHECK] [-D DELIM] [-V VERBOSE] 

File Iterator and Hasher - checks for duplicates, then moves and renames files in numerical order  

**arguments:**  
  -h, --help -> show this help message and exit  
  -N NAME, --name NAME -> sets the name of the output  
  -I INITIAL, --initial INITIAL -> sets the initial value  
  -S START, --start START -> from this location, defaults to renamer.py's current location  
  -T TO, --to TO -> to this location **mandatory**  
  -M MAKE, --make MAKE -> create new folder if not found, Y for yes  
  -C CHECK, --check CHECK -> test for all duplicates, Y for yes  
  -D DELIM, --delim DELIM -> check and correct for delims and non-zero fronted numbering, Y for yes  
  -V VERBOSE, --verbose VERBOSE -> Print out all actions, Y for yes


**TODO**  

1. allow a -t test option to run fih-test.py  
2. currently handles up to 1000 files because I'm lazy.  Need to make it work with arbitrary numbers  
3. enable automatic numbering, semi-necessary for 2
4. Add machine number reading?
5. GUI?  (Major strech goal)
6. Allow for more control over naming conventions?  Such as taking part of the existing name?  
