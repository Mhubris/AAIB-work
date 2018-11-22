import getLinesFromCSV as info

from os import listdir
from os.path import isfile, join

# folder with csv files
mypath = 'database_final\\'

# get all the file names in that folder
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# get line from the feature extraction algorithm used in data for each file
featuresmatrix = [info.get_line(name) for name in onlyfiles]

# print to the console for debugging
print(onlyfiles)
print(featuresmatrix)

# create or overwrite file to store the database (.tab file)
f = open("database.tab", "w")
# the first line is the header (features and target class)
firstline = '\t'.join((
    r'muX',
    r'medianX',
    r'sigmaX',
    r'kurtosisX',
    r'skewX',
    r'corrXY1',
    r'corrXZ1',
    r'countCrossXZ',
    r'vppX',
    r'maxX',
    r'minX',
    r'len(t)',
    r'integralX',
    r'sumX',
    r'goalClass' + '\n'
    ))
f.write(firstline)
# each line corresponds to relevant information of one particular .csv file
for line in featuresmatrix:
    f.write(line)
f.close()
