#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Bdays={u'מאי': dt.datetime(2007,3,14,11,5,0) , u'איתי': dt.datetime(2011,6,21,9,45,0), u'קאי': dt.datetime(2014,06,8,13,43,0), u'איימי': dt.datetime(2016,3,2,8,5,0), u'דבי': dt.datetime(1977,9,4,17,5,0), u'יוסי': dt.datetime(1976,7,4,6,0,0)}
#mayBday = dt.datetime(2007,03,14,11,05,00)
now = dt.datetime.now()
#secs = (now - Bdays[u'מאי']).total_seconds()
#print("May: seconds {0}, minutes {1}, hours {2}, days {3}".format(secs, secs/60, secs/3600, secs/(3600*24)))
for name,date in Bdays.iteritems():
    secs = (now - date).total_seconds()
    print("{4} is alive for seconds {0}, minutes {1}, hours {2}, days {3}".format(secs, secs/60, secs/3600, secs/(3600*24), name))
