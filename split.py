from os import listdir
from os.path import isfile, join
import random
import sys

ALLFILE="allimages.txt"
TRAINFILE="train.txt"
VALIDFILE="val.txt"
TESTFILE="test.txt"

# Change this from 1.0 to some lower fraction to subsample the data
# e.g. 0.05 will use 5 percent of all the data
SUBSAMP=1.0

def main(path, TRAINPERC, VALIDPERC):

   with open(join(path, ALLFILE),'r') as source:

      data = [ (random.random(), line) for line in source ]
      data.sort()
      train=open(join(path, TRAINFILE),'w')
      valid=open(join(path, VALIDFILE),'w')
      test=open(join(path, TESTFILE),'w')

      count=len(data) # number of images
      cumlvalid=int(TRAINPERC*count) # number of training images
      cumltest=cumlvalid+int(VALIDPERC*count) # no. of training + validation images

      print("Total records = %d" % count)
      print("Train %d%% = %d" % (round(TRAINPERC*100), cumlvalid) )
      print("Valid %d%% = %d" % (round(VALIDPERC*100), cumltest-cumlvalid) )
      print("Test  %d%% = %d" % (round((1-TRAINPERC-VALIDPERC)*100), count-cumltest))

      didwrite=0
      ctr=0
      for _, line in data:
        if (ctr>=cumltest):
           if (random.uniform(0,1)<SUBSAMP):
              test.write( line )
        elif (ctr>=cumlvalid):
           if (random.uniform(0,1)<SUBSAMP):
              valid.write( line )
        else:
           if (random.uniform(0,1)<SUBSAMP):
              train.write( line )
              didwrite=didwrite+1
        ctr=ctr+1

      print('Wrote training data %d' % didwrite)

if __name__ == "__main__":
    main(input('Path: '), float(input('Train: ')), float(input('Val: ')))
