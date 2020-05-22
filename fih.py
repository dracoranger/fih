#!/usr/bin/env python3
import os
import glob
import argparse
import hashlib
import shutil
import sys


'''
TODO make tests
TODO replace fileSeparator with os.root.join()?

'''

parser = argparse.ArgumentParser(prog = "fih.py", description="File Iterator and Hasher - checks for duplicates, then moves and renames files in numerical order")
parser.add_argument("-N", "--name", help = "sets the name of the output", default = "Default_")
parser.add_argument("-I", "--initial", help = "sets the initial value", type = int, default = 0)
parser.add_argument("-S", "--start", help = "from this location, defaults to renamer.py's current location")
parser.add_argument("-T", "--to", help = "to this location")
parser.add_argument("-M", "--make", help = "create new folder if not found? Y for yes", default = '')
parser.add_argument("-C", "--check", help = "test for all duplicates, Y for yes", default = '')
parser.add_argument("-D", "--delim", help = "check and correct for delims and non-zero fronted numbering, Y for yes", default = '')
#parser.add_argument("-t", "--test", help = "run automated check on components to ensure functionality") #TODO, need to use this to call fih-test.py?

args = parser.parse_args()

rename = args.name
start = args.initial
target = args.to
fro = args.start
merge = args.make
check = args.check
#test = args.test
delim = args.delim

fileSeparator = "//"
if os.name == "nt":
    fileSeparator = "\\"

if not target:
    print("Error: no location provided", file = sys.stderr)
    parser.print_help(sys.stderr)
    exit()

def check_for_duplicates_all(target_passed, hash_storage = {}):
    targetLocation = target_passed
    hashes = hash_storage
    BLOCKSIZE = 65536

    for root, dirs, files in os.walk(targetLocation):
        for tfile in files:
            hasher = hashlib.sha256()
            with open(os.path.join(root,tfile), "rb") as hashFile:
                buf = hashFile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = hashFile.read(BLOCKSIZE)
            if hasher.hexdigest() not in hashes:
                hashes[hasher.hexdigest()] = os.path.join(root,tfile)
            else:
                print(hashes[hasher.hexdigest()] + " <-Old file New file-> " + os.path.join(root,tfile))

    for directory in dirs:
        check_for_duplicates_all(os.path.join(root, directory), hashes)

def check_for_duplicates(local_files):
    global target
    global fro

    currentLocation = os.curdir
    targetLocation = target
    hashes = {}
    current = []
    BLOCKSIZE = 65536

    targetFiles = glob.glob(os.path.join(targetLocation, "*"))

    if fro:
        currentLocation = fro

    for tfile in targetFiles:
        hasher = hashlib.sha256()
        with open(tfile, "rb") as hashFile:
            buf = hashFile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = hashFile.read(BLOCKSIZE)
            if hasher.hexdigest() not in hashes:
                hashes[hasher.hexdigest()] = os.path.join(root,tfile)
            else:
                print(hashes[hasher.hexdigest()] + " <-Old file New file-> " + os.path.join(root,tfile))

    for file in local_files:
        if not os.path.isdir(file):
            print(file)
            #thisFile = os.path.join(currentLocation, file)
            thisFile = file
        with open(thisFile, "rb") as hashFile:
            hasher = hashlib.sha256()
            buf = hashFile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = hashFile.read(BLOCKSIZE)
        if hasher.hexdigest() not in hashes:
            curr = os.path.join(os.curdir , thisFile)
            current.append(curr)
        else:
            print(hashes[hasher.hexdigest()]+" <-Old file New file-> " + thisFile)
            current.append(False)

    return(current)


def main():
    global start
    global rename
    global merge
    global target
    global check
    global fro
    global delim

    currentLocation = "*"
    if fro:
        currentLocation = fro + fileSeparator + "*"

    deliminators = ["-"," ",":"]

    if check:
        check_for_duplicates_all(target)
    else:
        if not os.path.isdir(target) and merge:
            os.mkdir(target)
            print("Created Directory "+ target)
        if delim:
            files = glob.glob(currentLocation)
            for file in files:
                for delim in deliminators:
                    new_name = ""
                    parts = file.split(delim)
                    for part in parts:
                        if len(parts) == 1:
                            new_name = new_name + part
                        elif part == parts[-1]:
                            new_name = new_name + part
                        elif part.find("0") == -1:
                            try:
                                if int(part)<10:
                                    new_name = new_name + "0" + part + delim
                                else:
                                    new_name = new_name + part + delim
                            except:
                                new_name = new_name + part + delim
                        else:
                            new_name = new_name + part + delim
                    if new_name != file and file != os.path.basename(__file__):
                        os.rename(file, new_name)
                        break

        local_files = glob.glob(currentLocation)
        curr = check_for_duplicates(local_files)
        num = 0
        #TODO check length of local_files, and make this actually logical, rather than just working for the first 1000 files
        for file in local_files:
            new_name = rename
            if start < 10:
                new_name=new_name+"0"
            if start < 100:
                new_name=new_name+"0"
            parts = file.split(".")  # [abc, 2000.jpg]
            new_name =new_name+str(start)+"."+ parts[-1]
            if file != os.path.basename(__file__) and not os.path.isdir(file) and file != "fih-test.py":
                if curr[num]:
                    shutil.move(file, target + fileSeparator + new_name)
                start = start + 1
            num = num + 1

main()
