
import logging

a = [1, 2, 3]
try:
    print a[3]
except Exception, e:
    logging.error(e)

print "=============="

b = [1, 2, 3]
try:
    print b[3]
except Exception, e:
    logging.exception(e)