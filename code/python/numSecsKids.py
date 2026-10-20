#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Bdays = {'Alice': dt.datetime(2008, 1, 15, 10, 0, 0), 'Bob': dt.datetime(2011, 5, 20, 9, 30, 0)}
#aliceBday = dt.datetime(2008, 1, 15, 10, 0, 0)
now = dt.datetime.now()
#secs = (now - Bdays['Alice']).total_seconds()
#print("May: seconds {0}, minutes {1}, hours {2}, days {3}".format(secs, secs/60, secs/3600, secs/(3600*24)))
for name,date in Bdays.iteritems():
    secs = (now - date).total_seconds()
    print("{4} is alive for seconds {0}, minutes {1}, hours {2}, days {3}".format(secs, secs/60, secs/3600, secs/(3600*24), name))
