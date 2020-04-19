#!/usr/bin/python3
#  created by Björn Bruch
# Published under the GNU-Licence
# Script to reduce the number of pictures taken with my timelapse script "raspi-cam.py" according to a given interval.
# My files are sorted in subfolders and the filename ist like: 2019-12-31_2056.jpg
# The format is important, because the script reads out the time of the filename to calculate the interval between taken pictures.


import os
import glob
import time
import math
import threading
from datetime import datetime
import subprocess
import time
import shutil

#  define variants
quellordner_rel = "GH-Bau/" #relativer quellordner zum sqriptspeicherort
zielordner_rel = "GH-Muell/" #relativer zielordner zum sqriptspeicherort
pfad = os.path.dirname(os.path.abspath(__file__)) # pfad herausfinden
all_quellpfad = os.path.join(pfad,quellordner_rel) #pfad und relativen quellpfad kombinieren
zielordner = os.path.join(pfad,zielordner_rel)
interval_1 = 300
interval_2 = 360

def folder_objects(dirname, otype = "all"):
    if (os.path.exists(dirname) == False or
        os.path.isdir(dirname) == False or
        os.access(dirname, os.R_OK) == False):
        return False
    else:
        objects = os.listdir(dirname)
        result = []
        for objectname in objects:
            objectpath = dirname + "/" + objectname
            if (otype == "all" or
                (otype == "dir"  and os.path.isdir(objectpath)  == True) or
                (otype == "file" and os.path.isfile(objectpath) == True) or
                (otype == "link" and os.path.islink(objectpath) == True)):
                result.append(objectname)
        result.sort()
        return result

#  find small (corrupted) files and move them
def small_files():
    count_small=0
    for folderName, subfolders, filenames in os.walk(all_quellpfad):
        subfolders[:] = [d for d in subfolders if not d.startswith('@eaDir')]
        # print("")
        # print('Ordername: ' + folderName)
        for each_file in filenames:
            fullpath = os.path.join(folderName,each_file)
            groesse = os.path.getsize(fullpath)
            if groesse < 10 * 5120:
                count_snall=count_small+1
                print(str(groesse) + ' Weg damit!: ' + str(fullpath))
                shutil.move(fullpath,zielordner)
    print("Es wurden " + str(count_small) + " Dateien gefunden")

#  find files with an interval smaller than given and move the following file
def duennen():
    for folderName, subfolders, filenames in os.walk(all_quellpfad):
        subfolders[:] = [d for d in subfolders if not d.startswith('@eaDir')]
        print("")
        print('Ordername: ' + folderName)
        dateiliste = []
        for filename in filenames:
    #        print('Datei in ' + folderName + ': ' + filename)
            dateiliste.append(filename)
        dateiliste.sort()
        print(str(len(dateiliste)) + '  Dateien im Verzeichnis')
    #    print("")
    #    print(dateiliste)
        dateizaehler = 0
        dateizeiten = []
        while dateizaehler < len(dateiliste):
            dateiname = dateiliste[dateizaehler]
            # print("Dateiname : " + str(dateiliste[dateizaehler]))
            # dateiname_jahr = int(dateiname[0:4])
            # dateiname_monat = int(dateiname[5:7])
            # dateiname_tag = int(dateiname[8:10])
            dateiname_stunde = int(dateiname[11:13])
            dateiname_minute = int(dateiname[13:15])
            # dateiname_zeit = int(dateiname[11:15])
            dateiname_zeit_sek = int(dateiname_minute * 60 + dateiname_stunde * 3600)
            dateizeiten.append(dateiname_zeit_sek)
            dateizaehler = dateizaehler+1

        del_counter=0
        first_file = 0
        second_file = 1
        while second_file < len(dateiliste):
            interval = (dateizeiten[second_file]-dateizeiten[first_file])
            if interval == interval_1 or interval == interval_2:
                quelldatei = os.path.join(folderName,dateiliste[second_file])
                print(str(interval) + '-----Die Datei würde weggeschmissen: ' + str(quelldatei))
                shutil.move(quelldatei,zielordner)
                del_counter=del_counter+1
            if interval > interval_2:
                # print(str(interval) + '+++++Die Datei würde behalten werden: ' + str(dateiliste[second_file]))
                first_file=second_file
            second_file=second_file+1
        if del_counter < 0:
            print("")
            print(str(len(dateiliste)) + '  Dateien im Verzeichnis')
            print(str(del_counter) + '  bereinigte Dateien im Ordner ' + str(folderName))
            # print('Intervall zwischen ' + str(dateiliste[counter]) + ' und ' + str(dateiliste[0]) + ': ' + str(interval))

print ("Quellpfad: " + str(all_quellpfad))
print ("Zielordner: " + str(zielordner))

small_files()
time.sleep(2)
duennen()
