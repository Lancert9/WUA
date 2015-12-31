import time
import datetime

__author__ = 'j-lijiawei'

begin_time = datetime.datetime.now()
print begin_time
for i in range(20):
    print "***"
    time.sleep(1)
end_time = datetime.datetime.now()
print end_time
delta_time = end_time - begin_time
print delta_time
