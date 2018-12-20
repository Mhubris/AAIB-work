"""
=====================
Generate classifier database file
=====================
This file contains information regarding the creation of a databse file (mainly for orange).
"""

import getLinesFromCSV as info

from os import listdir
from os.path import isfile, join

# folder with csv files
mypath = '19_12_db\\'

# get all the file names in that folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# get line from the feature extraction algorithm used in data for each file
featuresmatrix = [info.get_line(name) for name in onlyfiles]


# create or overwrite file to store the database (.tab file)
f = open("database.tab", "w")

# the first line is the header (features and target class)
f.write(info.get_first_line())

# each line corresponds to relevant information (features) of one particular .csv file
for line in featuresmatrix:
    f.write(line)
f.close()

# print results to the console for debugging
print(onlyfiles)
print(featuresmatrix)
print(len(featuresmatrix))
