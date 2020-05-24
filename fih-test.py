#fih.py tester

import os 
import glob
import subprocess
import time

fileSeparator = "//"
if os.name == "nt":
    fileSeparator = "\\"

testLocation = os.curdir

tests = ["python fih.py", #0 test default error output
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y",  #1 move files from folder to end 
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -I 5", #2 move files from folder to end, starting at #5 
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -S " + testLocation + fileSeparator + "start", #3 move files from start to end 
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -S " + testLocation + fileSeparator + "start -M Y", #4 move files from start to end, but make the end
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -S " + testLocation + fileSeparator + "start", #5 move files from start to end but test and output duplicates
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y -C Y", #6 Test for all duplicates
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -S " + testLocation + fileSeparator + "start -D Y", #7 move files from start to end but fix incorrect delimination
         "python fih.py -T " + testLocation + fileSeparator + "end -V Y" + " -S " + testLocation + fileSeparator + "start -N Successful_test_" #8 move files from start to end but rename from default
         #need to create a test that checks for identical files in the target and start location
         ]  

test_files = [{}, #none
              {"A" : "0", "B" : "1", "C" : "2", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #just testing movement
              {"A" : "0", "B" : "1", "C" : "2", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #testing start from 5 
              {"A" : "0", "B" : "1", "C" : "2", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #specify different start location
              {"A" : "0", "B" : "1", "C" : "2", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #create folder 
              {"A" : "0", "B" : "0", "C" : "0", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #test duplicates
              {"A" : "0", "B" : "0", "C" : "0", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"}, #test duplicates
              {"A-2" : "0", "B-3" : "1", "C-4" : "2", "D-5" : "3", "E-6" : "4", "F-7" : "5", "G-8" : "6", "H-9" : "7", "I-10" : "8", "J-11" : "9"}, #remove deliminators
              {"A" : "0", "B" : "0", "C" : "0", "D" : "3", "E" : "4", "F" : "5", "G" : "6", "H" : "7", "I" : "8", "J" : "9"} #test renaming
              ] 
expected_results = ["Error: no location provided\r\nusage: fih.py [-h] [-N NAME] [-I INITIAL] [-S START] [-T TO] [-M MAKE]\r\n              [-C CHECK] [-D DELIM] [-V VERBOSE]\r\n\r\nFile Iterator and Hasher - checks for duplicates, then moves and renames files\r\nin numerical order\r\n\r\noptional arguments:\r\n  -h, --help            show this help message and exit\r\n  -N NAME, --name NAME  sets the name of the output\r\n  -I INITIAL, --initial INITIAL\r\n                        sets the initial value\r\n  -S START, --start START\r\n                        from this location, defaults to renamer.py's current\r\n                        location\r\n  -T TO, --to TO        to this location\r\n  -M MAKE, --make MAKE  create new folder if not found, Y for yes\r\n  -C CHECK, --check CHECK\r\n                        test for all duplicates, Y for yes\r\n  -D DELIM, --delim DELIM\r\n                        check and correct for delims and non-zero fronted\r\n                        numbering, Y for yes\r\n  -V VERBOSE, --verbose VERBOSE\r\n                        Print out all actions, Y for yes\r\n", 
                    "A.txt->.\\end\\Default_000.txt\r\nB.txt->.\\end\\Default_001.txt\r\nC.txt->.\\end\\Default_002.txt\r\nD.txt->.\\end\\Default_003.txt\r\nE.txt->.\\end\\Default_004.txt\r\nF.txt->.\\end\\Default_005.txt\r\nG.txt->.\\end\\Default_006.txt\r\nH.txt->.\\end\\Default_007.txt\r\nI.txt->.\\end\\Default_008.txt\r\nJ.txt->.\\end\\Default_009.txt\r\nresults.txt->.\\end\\Default_010.txt\r\nComplete\r\n", 
                    "A.txt->.\\end\\Default_005.txt\r\nB.txt->.\\end\\Default_006.txt\r\nC.txt->.\\end\\Default_007.txt\r\nD.txt->.\\end\\Default_008.txt\r\nE.txt->.\\end\\Default_009.txt\r\nF.txt->.\\end\\Default_010.txt\r\nG.txt->.\\end\\Default_011.txt\r\nH.txt->.\\end\\Default_012.txt\r\nI.txt->.\\end\\Default_013.txt\r\nJ.txt->.\\end\\Default_014.txt\r\nComplete\r\n",
                    ".\\start\\A.txt->.\\end\\Default_000.txt\r\n.\\start\\B.txt->.\\end\\Default_001.txt\r\n.\\start\\C.txt->.\\end\\Default_002.txt\r\n.\\start\\D.txt->.\\end\\Default_003.txt\r\n.\\start\\E.txt->.\\end\\Default_004.txt\r\n.\\start\\F.txt->.\\end\\Default_005.txt\r\n.\\start\\G.txt->.\\end\\Default_006.txt\r\n.\\start\\H.txt->.\\end\\Default_007.txt\r\n.\\start\\I.txt->.\\end\\Default_008.txt\r\n.\\start\\J.txt->.\\end\\Default_009.txt\r\nComplete\r\n",
                    "Created Directory .\\end\r\n.\\start\\A.txt->.\\end\\Default_000.txt\r\n.\\start\\B.txt->.\\end\\Default_001.txt\r\n.\\start\\C.txt->.\\end\\Default_002.txt\r\n.\\start\\D.txt->.\\end\\Default_003.txt\r\n.\\start\\E.txt->.\\end\\Default_004.txt\r\n.\\start\\F.txt->.\\end\\Default_005.txt\r\n.\\start\\G.txt->.\\end\\Default_006.txt\r\n.\\start\\H.txt->.\\end\\Default_007.txt\r\n.\\start\\I.txt->.\\end\\Default_008.txt\r\n.\\start\\J.txt->.\\end\\Default_009.txt\r\nComplete\r\n",
                    ".\\end\\.\\end\\A.txt <-Old file New file-> .\\end\\.\\end\\B.txt\r\n.\\end\\.\\end\\A.txt <-Old file New file-> .\\end\\.\\end\\C.txt\r\n.\\end\\.\\end\\A.txt <-Old file New file-> .\\start\\A.txt\r\n.\\end\\.\\end\\A.txt <-Old file New file-> .\\start\\B.txt\r\n.\\end\\.\\end\\A.txt <-Old file New file-> .\\start\\C.txt\r\n.\\end\\.\\end\\D.txt <-Old file New file-> .\\start\\D.txt\r\n.\\end\\.\\end\\E.txt <-Old file New file-> .\\start\\E.txt\r\n.\\end\\.\\end\\F.txt <-Old file New file-> .\\start\\F.txt\r\n.\\end\\.\\end\\G.txt <-Old file New file-> .\\start\\G.txt\r\n.\\end\\.\\end\\H.txt <-Old file New file-> .\\start\\H.txt\r\n.\\end\\.\\end\\I.txt <-Old file New file-> .\\start\\I.txt\r\n.\\end\\.\\end\\J.txt <-Old file New file-> .\\start\\J.txt\r\nComplete\r\n",
                    ".\\end\\A.txt <-Old file New file-> .\\end\\B.txt\r\n.\\end\\A.txt <-Old file New file-> .\\end\\C.txt\r\nComplete\r\n", 
                    ".\\start\\A-2.txt->.\\end\\Default_000.txt\r\n.\\start\\B-3.txt->.\\end\\Default_001.txt\r\n.\\start\\C-4.txt->.\\end\\Default_002.txt\r\n.\\start\\D-5.txt->.\\end\\Default_003.txt\r\n.\\start\\E-6.txt->.\\end\\Default_004.txt\r\n.\\start\\F-7.txt->.\\end\\Default_005.txt\r\n.\\start\\G-8.txt->.\\end\\Default_006.txt\r\n.\\start\\H-9.txt->.\\end\\Default_007.txt\r\n.\\start\\I-10.txt->.\\end\\Default_008.txt\r\n.\\start\\J-11.txt->.\\end\\Default_009.txt\r\nComplete\r\n", 
                    ".\\start\\A.txt->.\\end\\Successful_test_000.txt\r\n.\\start\\B.txt->.\\end\\Successful_test_001.txt\r\n.\\start\\C.txt->.\\end\\Successful_test_002.txt\r\n.\\start\\D.txt->.\\end\\Successful_test_003.txt\r\n.\\start\\E.txt->.\\end\\Successful_test_004.txt\r\n.\\start\\F.txt->.\\end\\Successful_test_005.txt\r\n.\\start\\G.txt->.\\end\\Successful_test_006.txt\r\n.\\start\\H.txt->.\\end\\Successful_test_007.txt\r\n.\\start\\I.txt->.\\end\\Successful_test_008.txt\r\n.\\start\\J.txt->.\\end\\Successful_test_009.txt\r\nComplete\r\n" ]

def create_folders():
    global testLocation 
    global fileSeparator
    
    ret = True
    if not os.path.isdir("end"):
        os.mkdir("end")
    else:
        print("WARNING: end folder exists")
        files = glob.glob(testLocation + fileSeparator + "end" +  fileSeparator + "*")
        if not files == []:
            print("ERROR: end folder has files")
            ret = False
    if not os.path.isdir("start"):
        os.mkdir("start")
    else:
        print("WARNING: start folder exists")
        files = glob.glob(testLocation + fileSeparator + "start\\*")
        if not files == []:
            print("ERROR: start folder has files")
            ret = False

    return ret

def create_files(file_dictionary, push_down, push_to_end):
    global testLocation 
    global fileSeparator

    write_location = testLocation + fileSeparator

    if push_down:
        write_location = write_location + "start" + fileSeparator

    if push_to_end:
        for i in file_dictionary:
           with open(testLocation + fileSeparator + "end" + fileSeparator + str(i) + ".txt", "w+") as file:
               file.write(file_dictionary[i])

    for i in file_dictionary:
        with open(write_location + fileSeparator + str(i) + ".txt", "w+") as file:
            file.write(file_dictionary[i])
    return True

def reset():
    #delete files and folders
    global test_files

    home_files = glob.glob(testLocation + fileSeparator+"*")
    for files_num in range(5, len(test_files)):
        files = test_files[files_num]
        for file in files:
            if testLocation + fileSeparator + file + ".txt" in home_files:
                os.remove(testLocation + fileSeparator + file + ".txt")

    if os.path.isdir(testLocation + fileSeparator + "start"):
        files = glob.glob(testLocation + fileSeparator + "start" +  fileSeparator + "*")
        for i in files:
            os.remove(i)
        os.rmdir("start")
    if os.path.isdir(testLocation + fileSeparator + "end"):
        files = glob.glob(testLocation + fileSeparator + "end" +  fileSeparator + "*")
        for i in files:
            os.remove(i)
        os.rmdir("end")



def main():
    global tests
    global test_files
    global expected_results
    global testLocation 
    global fileSeparator

    failures = []
    successes = []

    different_start_location = False
    push_to_end = False
    no_end_folder = False


    for i in range(0,len(tests)):

        if i > 2:
            different_start_location = True

        if i == 5 or i == 6:
            push_to_end = True
            
        #create folders and files
        create_folders()
        create_files(test_files[i], different_start_location, push_to_end)

        if i == 4:
            no_end_folder = True
            os.rmdir("end")

        #Log this test
        print(tests[i])
        successes.append("\n"+tests[i]+"\n")
        failures.append("\n"+tests[i]+"\n")

        #spin off subprocess
        test = subprocess.run(tests[i], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(1)
        #get result
        results = test.stdout.decode("ASCII")
        print(results)
        #test result
            
        if results == expected_results[i]:
            print(str(i) + " SUCCCEEDED OUTPUT")
            successes.append(str(i) + " SUCCCEEDED OUTPUT")
        else:
            print(results)
            print(expected_results[i])
            print("Output FAILED: " + str(i))
            failures.append("Output FAILED: " + str(i) + "Actual Results\n" + str(results) + "Expected Results\n" + str(expected_results[i]))

        input("Halted, waiting for review\n\n")
        #reset folder
        reset()
        different_start_location = False
        push_to_end = False

    #print end summary
    with open("results.txt", "w+") as results:
        results.write("FAILURES:\n")
        for i in failures:
            results.write(i)
        results.write("\n\nSUCCESSES:\n")
        for i in successes:
            results.write(i)
    print("FAILURES:\n"+str(failures) + "\n\nSUCCESSES:\n"+str(successes))

main()