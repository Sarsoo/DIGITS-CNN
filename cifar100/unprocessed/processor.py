"""
Turn a combined, unsorted all images list into a sorted list with the right paths
"""

from os import listdir
from os.path import isfile, join
import random

ALLFILE="allimages.txt"

def main():
    with open("allimages-us.txt",'r') as source:

        data = [ line.split(' ') for line in source ]
        data = [ (line[0].replace('fine', 'fine_comb'), line[1]) for line in data ]
        data = [ (line[0].replace('test', 'all_ims'), line[1]) for line in data ]
        data = [ (line[0].replace('train', 'all_ims'), line[1]) for line in data ]

        data = [ (line[0].split('/'), line[1]) for line in data ]
        data.sort(key=lambda x: (x[1], x[0][-1]))

        data = [ ('/'.join(line[0]), line[1]) for line in data ]
        data = [ ' '.join((line[0], line[1])) for line in data ]

        for i in data[:5]:
            print(i)

        op=open(ALLFILE,'w')
        for i in data:
            op.write(i)

if __name__ == "__main__":
    main()
