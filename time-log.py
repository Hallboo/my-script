#!/usr/bin/python

import time

timestd = time.localtime(time.time())
print(" validation error: %.5f  time: %02d:%02d %02d" % (3.1213243432432,timestd.tm_hour,timestd.tm_min,timestd.tm_sec))#md by herb
