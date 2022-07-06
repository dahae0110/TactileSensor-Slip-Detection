import serial
import time
import csv
import sys
import os
import numpy as np
from datetime import datetime


def passiveserial(writtenmode):
    
    #deside timing on writing data to csv.
    ways_writtenmode = {'0' : 'passtime', '1' : 'measuretime', '2' : 'anytiming'}
    writtenmode = writtenmode

    ser = serial.Serial()

    #change port name and baurate for your condition.
    ser.baudrate = 115200
    ser.port = '/dev/tty.usbmodem14101'
    ser.open()

    #list for values of three cantilever lever
    firstlever = []
    secoundlever = []
    thirdlever = []
    
    #A variable that indicates which cantilever value is currently being taken
    whichlever = 0
    times = 0
    

    while(True):
        try:
            # We convert byte data to string as below
            line = ser.readline().decode()

            '''
            if (line.split()[0] == '') or len(line.split()[0]) >= 4 :
                ser.flushInput()
                return line
            else:
                return (line)
            
            if (line.split()[1] == '') or len(line.split()[1]) >= 4 :
                ser.flushInput()
                return line
            else:
                return (line)
            
            if (line.split()[2] == '') or len(line.split()[2]) >= 4 :
                ser.flushInput()
                return line
            else:
                return (line)
            '''
            
            line1 = line.split()[0]
            line2 = line.split()[1]
            line3 = line.split()[2]
            print(line1)
            print(line2)
            print(line3)

            '''
            if (line1 == '') or len(line1) >= 4 :
                ser.flushInput()
                return line1
            else:
                return (line1)
            
            if (line2 == '') or len(line2) >= 4 :
                ser.flushInput()
                return line2
            else:
                return (line2)
            
            if (line3 == '') or len(line3) >= 4 :
                ser.flushInput()
                return line3
            else:
                return (line3)
            
            '''
            
            
            if (line1 == ''):
                line1 = line1.replace('','0')
            elif (line2 == ''):
                line2 = line2.replace('','0')
            else: 
                line3 = line3.replace('','0')     
            
           
           #len(l) == 0
           #print(line1)
           #print(line2)
           #print(line3)

            if whichlever == 0:
                firstlever.append(line1)
                whichlever += 1

            elif whichlever == 1:
                secoundlever.append(line2)
                whichlever += 1

            else:
                thirdlever.append(line3)
                whichlever = 0
                times += 1

            #After a certain times of reading serial, write data for csv.
            if writtenmode == ways_writtenmode['1']: #measuretimes:
                samplingrate = 10 #refer arduino
                secounds = 10 #anytime
                times += 1
                #print(times)

                if times == samplingrate * secounds:
                    #print(firstlever, secoundlever, thirdlever)
                    writecsv(firstlever, secoundlever, thirdlever)
                    times = 0

        except KeyboardInterrupt:
            ser.close()
            break

def writecsv(firstlever, secoundlever, thirdlever):
    
    #A directry for saving data
    datadir = '/Users/dahaeshin/Desktop/TactileSenor/Data/'

    #category name of data
    category = 'testing'
    category = datadir + category

    os.makedirs(category +'/csvs', exist_ok = True)
    datetime_now = datetime.now()

    firstlever = list(map(int, firstlever))
    secoundlever = list(map(int, secoundlever))
    thirdlever = list(map(int, thirdlever))

    #Identifier of data file to be saved Decide so that the name of the file can be uniquely determined.
    identifier = 'dahaeshin'
    csvname = category + '/csvs/' + identifier + '_' + datetime_now.strftime('%Y_%m_%d_%H_%M_%S')

    with open(csvname + '.csv', 'w') as file:
        writer = csv.writer(file)

        firstleverarray = np.array(firstlever)
        secoundleverarray = np.array(secoundlever)
        thirdleverarray = np.array(thirdlever)

        #stacking
        firstleverarray = firstleverarray - firstleverarray[0]
        secoundleverarray = secoundleverarray - secoundleverarray[0]
        thirdleverarray = thirdleverarray - thirdleverarray[0]

        writer.writerow(firstleverarray)
        writer.writerow(secoundleverarray)
        writer.writerow(thirdleverarray)

        print("AmountOfData * " + str(len(os.listdir(category + '/csvs/'))) )

def main():
    
    #Change the writtenmode depending on the scenario
    writtenmode = 'measuretime'
    #Immediately after the start of processing, strange values may be sent serially, so sleep
    time.sleep(5)

    while(True):
        passiveserial(writtenmode)

if __name__ == "__main__":
    main()
