#fih.py tester

import os 
import glob
import subprocess
import time

fileSeparator = "//"
print(os.name)
if os.name == "nt":
    fileSeparator = "\\"

print(os.curdir)
testLocation = os.curdir

tests = ["python fih.py", #0 test default error output
         "python fih.py -T " + testLocation + fileSeparator + "end",  #1 move files from folder to end 
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -I 5", #2 move files from folder to end, starting at #5 
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start", #3 move files from start to end 
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start -M Y", #4 move files from start to end, but make the end
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start", #5 move files from start to end but test and output duplicates
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start -C Y", #6 move files from start to end but test for all duplicates
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start -D Y", #7 move files from start to end but fix incorrect delimination
         "python fih.py -T " + testLocation + fileSeparator + "end" + " -S " + testLocation + fileSeparator + "start -N Successful_test_" #8 move files from start to end but rename from default
         #need to create a test that checks for identical files in the target and start location
         ]  

test_files = [{}, #none
              {"A" : "0","B" : "1","C" : "2","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #just testing movement
              {"A" : "0","B" : "1","C" : "2","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #testing start from 5 
              {"A" : "0","B" : "1","C" : "2","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #specify different start location
              {"A" : "0","B" : "1","C" : "2","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #create folder 
              {"A" : "0","B" : "0","C" : "0","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #test duplicates
              {"A" : "0","B" : "0","C" : "0","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"}, #test duplicates
              {"A-2" : "0","B-3" : "1","C-4" : "2","D-5" : "3","E-6" : "4","F-7" : "5","G-8" : "6","H-9" : "7","I-10" : "8","J-11" : "9"}, #remove deliminators
              {"A" : "0","B" : "0","C" : "0","D" : "3","E" : "4","F" : "5","G" : "6","H" : "7","I" : "8","J" : "9"} #test renaming
              ] 
expected_results = ["","" ,"" ,"" ,"" ,"" ,"", "", "" ]
expected_files = ["","" ,"" ,"" ,"" ,"" ,"", "", "" ]

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
           with open(testLocation + fileSeparator + "end" + fileSeparator + str(i) + ".txt","w+") as file:
               file.write(file_dictionary[i])

    for i in file_dictionary:
        with open(write_location + fileSeparator + str(i) + ".txt","w+") as file:
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
                print(testLocation + fileSeparator + file)
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

        #spin off subprocess
        test = subprocess.run(tests[i], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(1)
        #get result
        results = test.stdout
        print(results.decode("ASCII"))
        #test result
            
        if results == expected_results[i]:
            print(str(i) + " SUCCCEEDED OUTPUT")
            successes.append(str(i) + " SUCCCEEDED OUTPUT")
        else:
            print("Output FAILED: " + str(i))
            failures.append("Output FAILED: " + str(i) + str(results) + str(expected_results[i]))
        files = glob.glob(testLocation+ fileSeparator + "end" +  fileSeparator + "*")
        if files == expected_files[i]:
            print(i + " SUCCCEEDED FILES")
            successes.append(i + " SUCCCEEDED FILES")
        else:
            print("Files FAILED: " + str(i))
            failures.append("Files FAILED: " + str(i) + str(files) + str(expected_files[i]))

        input("Halted, waiting for review")
        #reset folder
        reset()
        different_start_location = False
        push_to_end = False

    #print end summary
    with open("results.txt","w+") as results:
        results.write("FAILURES:\n"+str(failures) + "\n\nSUCCESSES:\n"+str(successes))
    print("FAILURES:\n"+str(failures) + "\n\nSUCCESSES:\n"+str(successes))

main()