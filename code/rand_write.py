#!/usr/bin/python

import time, os, sys, string
import numpy as np

#get node name
myhost = os.uname()[1]
arg = sys.argv[1]
# get the node number
pros = string.atoi(arg, 10);
start = time.time()
seed = 1e4
for j in range(int(1e2)):
        mx = 0
        for i in range(int(1e3)):
                x = np.random.randn(int(seed))
                mx = mx + np.mean(x)
        f = open('/home/hemanta/Desktop/rand_%d.txt' %pros, 'a')
        #f = open('/scratch/hemanta.g/io/rand_%d.txt' %pros, 'a')
        #f = open('/scratch/home1/io/rand_%d.txt' %pros, 'a')
        f.write('%f\n' %(mx))
        f.close()
end = time.time()
#print hostname;io_file _size;time_taken
print myhost + ';condor;' + str(end-start)

