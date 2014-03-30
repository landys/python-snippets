#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pytz import timezone
import pytz, time

#def convert_datetime(unix_timestamp=1143408000, tz=1, long_fmt=1):
def convert_datetime(dt='2007-01-01 00:00:00', tz='', dest_fmt='', time_stamp=0):
    fmt      = '%Y-%m-%d %H:%M:%S'
    if time_stamp == 0:
        dt_stamp = time.mktime(time.strptime(dt, fmt))
    else:
        dt_stamp = float(dt)

    # ('Australia/Sydney','Asia/Hong_Kong')
    utc      = pytz.utc
    utc_dt   = datetime.utcfromtimestamp(dt_stamp).replace(tzinfo=utc)

    dest_tz  = timezone(tz)
    dest_dt  = dest_tz.normalize(utc_dt.astimezone(dest_tz))

    return dest_dt.strftime(dest_fmt)

if __name__ == '__main__':
    print "Asia/Hong_Kong: ", convert_datetime(dt='2007-01-01 00:00:00', tz='Asia/Hong_Kong',\
            dest_fmt='%Y-%m-%d %H:%M:%S')
    print "Australia/Sydney: ", convert_datetime(dt='2007-01-01 00:00:00', tz='Australia/Sydney',\
            dest_fmt='%Y-%m-%d %H:%M:%S')
    print "Australia/Sydney: ", convert_datetime(dt='1204210838', tz='Australia/Sydney',\
            dest_fmt='%Y-%m-%d %H:%M:%S', time_stamp=1)
    print "UTC: ", convert_datetime(dt='2009-01-14 13:45:50', tz='UTC',\
            dest_fmt='%Y-%m-%d %H:%M:%S')
    print "UTC: ", convert_datetime(dt='1204210838', tz='UTC',\
            dest_fmt='%Y-%m-%d %H:%M:%S', time_stamp=1)
