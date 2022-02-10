import subprocess                                                                   # Able to write scrip to the Command line
import os
import csv                                                                          # For writing to a csv file
import time                                                                         # Able to use clock

output= open ("Result.csv", "w")                                                    
#Device
subprocess.run("adb devices",shell=True)                                             # Device name print to cmd
subprocess.run("adb devices",shell=True, stdout=output)                              # Printing the device name to result.csv

#Model number
read = open ("Pre_log.txt", "w")
print("Model Name:")                                                              
subprocess.run("adb shell getprop ro.product.model",shell=True)                              # Printing the model number to cmd
output.write("Model Number:\n")                                                              # print "model number to Result.csv
subprocess.run("adb shell getprop ro.product.model",shell=True, stdout=read)                 # printing the model number to pre_log 
read.close()

# reading pre_log for the model number and printing it to result.csv
read = open("Pre_log.txt")
content = read.readlines()
read.close()
output.write(content[0])

#Build number
print("\nBuild Number:")                                                                       # Print "Build Number to cmd"
subprocess.run("adb shell getprop ro.build.version.incremental",shell= True)                   # Printing the Build Number to cmd                     
output.write("\nBuild Number:\n")                                                              # Print "Build Number to result.csv"
read = open("Pre_log.txt", "w")                                                                # openingg file to write log so we can read from it
subprocess.run("adb shell getprop ro.build.version.incremental",shell=True,stdout=read)        # Printing data to pre_Log.txt
read.close()

# Reading from pre_log and saving it to result.csv
read = open("Pre_log.txt")
content = read.readlines()                                                                     # Reads file lines
read.close()
output.write(content[0])                                                                       # Reading a specific line

#System version
print("\nAndroid system version:")                                                     # Print "Build Number to cmd"
subprocess.run("adb shell getprop ro.build.version.release", shell= True)              # Printing the Build Number to cmd                     
output.write("\nBuild Number:\n")                                                      # Print "Build Number to result.csv"
read = open("Pre_log.txt", "w")                                                        # openingg file to write log so we can read from it
subprocess.run("adb shell getprop ro.build.version.release",shell=True,stdout=read)    # Printing data to pre_Log.txt
read.close()

# Reading from pre_log and saving it to result.csv
read = open("Pre_log.txt")
content = read.readlines()
read.close()
output.write(content[0])

# Arrays lol
time_array=[]       # holds the time values
ping_array=[]       # holds the ping values
temp_array=[]       # holds the temperature values

Totmem_array=[]     # holds total memory value
Usedmem_array=[]    # holds used memory value
Freemem_array=[]    # holds free memory value
Buffermem_array=[]  # holds buffers mem value

Totswap_array=[]     # holds total swip value
Usedswap_array=[]    # holds used swip value
Freeswap_array=[]    # holds free swip value
Bufferswap_array=[]  # holds cache swip value

Totswap_array=[]     # holds total swip value
Usedswap_array=[]    # holds used swip value
Freeswap_array=[]    # holds free swip value
Bufferswap_array=[]  # holds cache swip value

CPUuser_array=[]     # cpu user
CPUnice_array=[]     # cpu nice
CPUsys_array=[]      # cpu usys
CPUidle_array=[]     # cup idle
CPUiow_array=[]      # cpu iow
CPUirq_array=[]      # cpu irq
CPUsirq_array=[]     # cpu sirq
CPUhost_array=[]     # cpu host

output.write("\nThe name of the workout and length of the workout:\n")
userinput = input("\nWhat workout are you running and how long is the workout, press enter after:")
output.write(userinput)   
output.write("\n")                                                              
userinput = input("\nDesired Test length in minutes: ")                                 # user input for the length of test
print("\nPlease Wait, test is running\n") 

t_end = time.time()+ 60 * int(userinput)                                                # calculating the duration of the test in minutes
incr = 0                                                                                # used to indicate the initial time
check = 0                                                                               # Used to check if a connection is lost so that a value will not be missed in the ping array

#While loop testing for ping, CPU, Memory, Temperature, Timestamp
while time.time()< t_end: #While start
    # Collecting the instance time a ping was requested 
    if incr==0:
            init_time=time.time()                                                       # Getting the inital time stamp                                                   
            time_array.append(time.time()-init_time)                                    # Calculating the intial time
            incr=1                      
    else:
        time_array.append(time.time()- init_time)                                       # Calculating the intial time after the initial start time
    #End else

    # Checking if wifi is connected
    read = open("Pre_log.txt", "w")
    subprocess.run("adb shell settings get global wifi_on",shell=True,stdout=read)        # Checks for wifi connection before running a ping test. 
    read.close()
    read = open("Pre_log.txt")
    content = read.readlines()
    read.close()
    test = int(content[0])                                                                # If wifi is connected, test=1 else test=0 and ping will be skipped

    #ping test
    if test>0:                                                                             # if test=0 ping test will be skipped                                                      
        read = open("Pre_log.txt", "w")
        subprocess.run("adb shell ping -c 1 google.com",shell=True,stdout=read)            # Writing ping log. Able to adjust the amount of ping packets you want to transmit
        read.close()                                                                       # Close file

        #Extracting Ping result and saving it to result.csv
        read = open("Pre_log.txt")
        content = read.readlines()
        read.close()
        if os.stat("Pre_log.txt").st_size > 200:
            dummy_CPU = content[1].split()                                                         # Splits the items on the line for better access
            if dummy_CPU[0] == "64":                                                               # checking the line before getting ping time
                mem = dummy_CPU[7].split("=")                                                      # splits the item into 2 items one before the = sign and one after
                ping_array.append(mem[1])                                                          # Saving the ping result to an array
                check = 1                                                                          # Used to check if a connection is lost
            #End if
        #End if

    #If a connection gets lost a zero will be inserted to the ping array
    if check != 1:
        ping_array.append(0)
    else:
        check = 0
    #Else end

    #Extracting the CPU temperature and saving it to result.csv
    read = open( "Pre_log.txt","w")
    subprocess.run("adb shell cat /sys/class/thermal/thermal_zone*/temp",shell= True,stdout=read) 
    read.close()
    read = open("Pre_log.txt")
    content = read.readlines()
    read.close()
    temp_array.append(float(content[7])/1000)                                                  # Getting the temperature value 

    #writing cpu/mem log to live_log.txt
    read = open("Pre_log.txt","w")
    subprocess.run("adb shell top -m 9 -n 1",shell=True, stdout=read)
    read.close()
    read = open("Pre_log.txt")
    content = read.readlines()
    read.close()

    #Getting CPU nd memory usage
    dummy_CPU = content[2].split()                                  # Splits the lines to get access to individual items 
    mem=dummy_CPU[1].split("k")                                     # Spliting item before K and after k
    Totmem_array.append(mem[0])                                     # Saving the result to array
    mem=dummy_CPU[3].split("k")
    Usedmem_array.append(mem[0])
    mem=dummy_CPU[5].split("k")
    Freemem_array.append(mem[0])
    mem=dummy_CPU[7].split("k")
    Buffermem_array.append(mem[0])

    #Getting Swap memory
    dummy_CPU= content[4].split()
    mem=dummy_CPU[1].split("k")
    Totswap_array.append(mem[0])
    mem=dummy_CPU[3].split("k")
    Usedswap_array.append(mem[0])
    mem=dummy_CPU[5].split("k")
    Freeswap_array.append(mem[0])
    mem=dummy_CPU[7].split("k")
    Bufferswap_array.append(mem[0]) 

    #Getting CPU usage
    dummy_CPU = content[6].split()
    mem=dummy_CPU[1].split("%")
    CPUuser_array.append(mem[0])
    mem=dummy_CPU[2].split("%")
    CPUnice_array.append(mem[0])
    mem=dummy_CPU[3].split("%")
    CPUsys_array.append(mem[0])
    mem=dummy_CPU[4].split("%")
    CPUidle_array.append(mem[0])
    mem=dummy_CPU[5].split("%")
    CPUiow_array.append(mem[0])
    mem=dummy_CPU[6].split("%")
    CPUirq_array.append(mem[0])
    mem=dummy_CPU[7].split("%")
    CPUsirq_array.append(mem[0])
    mem=dummy_CPU[8].split("%")
    CPUhost_array.append(mem[0])
#While End

#wrting the time stamp values to result.csv
wr = csv.writer(output)
output.write("\nTime stamp (seconds): \n") 
wr.writerow(time_array)   

#writing to the file result.csv
output.write("\nPing Test (Milliseconds): \n")
wr.writerow(ping_array)

#writing temperature value to result.csv
output.write("\nCPU Temperature (Celsius): \n")
wr.writerow(temp_array)
######################################################################################################################################################### Memory
output.write("\n######################################################################################### Memory\n")

# writing total memory value to result.csv
output.write("\nTotal memory (Kilobytes): \n")
wr.writerow(Totmem_array)

# writing Used memory value to result.csv
output.write("\nUsed memory (Kilobytes): \n ")
wr.writerow(Usedmem_array)

# writing Free memory value to result.csv
output.write("\nFree memory (Kilobytes): \n")
wr.writerow(Freemem_array)

# writing Buffers memory value to result.csv
output.write("\nBuffers memory (Kilobytes): \n")
wr.writerow(Buffermem_array)

######################################################################################################################################################### swap
output.write("\n######################################################################################### Swap\n")
# writing total memory value to result.csv
output.write("\nTotal Swap  (Kilobytes): \n")
wr.writerow(Totswap_array)

# writing Used memory value to result.csv
output.write("\nUsed Swap (Kilobytes): \n ")
wr.writerow(Usedswap_array)

# writing Free memory value to result.csv
output.write("\nFree Swap (Kilobytes): \n")
wr.writerow(Freeswap_array)

# writing Buffers memory value to result.csv
output.write("\nBuffers Swap (Kilobytes): \n")
wr.writerow(Bufferswap_array)

######################################################################################################################################################### 400% CPU
output.write("\n######################################################################################### 400% CPU\n")
# writing CPU User percentage to result.csv
output.write("\nCPU User (%): \n")
output.write("\n%User	Percentage of CPU utilization that occurred while executing at the user level (application).\n")
wr.writerow(CPUuser_array)

# writing CPU Nice percentage to result.csv
output.write("\nCPU Nice (%): \n")
output.write("\n%Nice	Percentage of CPU utilization that occurred while executing at the user level with nice priority\n")
wr.writerow(CPUnice_array)

# writing CPU Sys percentage to result.csv
output.write("\nCPU Sys (%): \n")
output.write("\n%System	 Percentage of CPU utilization that occurred while executing at the system level (kernel).\n")
wr.writerow(CPUsys_array)

# writing CPU Idle percentage to result.csv
output.write("\nCPU Idle (%): \n")
output.write("\n%Idle	Percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request.\n")
wr.writerow(CPUidle_array)

# writing CPU Iow percentage to result.csv
output.write("\nCPU Iow (%): \n")
output.write("\n%Iowait	  Percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request.\n")
wr.writerow(CPUiow_array)

# writing CPU Irq  percentage to result.csv
output.write("\nCPU Irq (%): \n")
output.write("\n%Irq   time spent servicing hardware interrupts\n")
wr.writerow(CPUirq_array)

# writing CPU Sirq percentage to result.csv
output.write("\nCPU Sirq (%): \n")
output.write("\n%Sirq   time spent servicing software interrupts\n")
wr.writerow(CPUsirq_array)

# writing CPU Host percentage to result.csv
output.write("\n%CPU Host (%): \n")
wr.writerow(CPUhost_array)

#closing all the files
read.close()
output.close()

# Deleting txt files
os.remove("Pre_log.txt")            
print("\nTest has finished. Result can be found in this directory with the file name, Result.csv\n")