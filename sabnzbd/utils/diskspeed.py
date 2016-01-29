#!/usr/bin/env python

import time
import os
import sys
import logging


def writetofile(filename, mysizeMB):
    # writes string to specified file repeat delay, until mysizeMB is reached. Then deletes file
    mystring = "The quick brown fox jumps over the lazy dog"
    writeloops = int(1000000 * mysizeMB / len(mystring))
    if os.name == 'nt':
        # On Windows, this crazy action is needed to
        # avoid a "permission denied" error
        try:
            os.system('echo Hi >%s' % filename)
        except:
            pass
    try:
        f = open(filename, 'wb')
    except:
        logging.debug('Cannot create file %s', filename)
        logging.debug("Traceback: ", exc_info=True)
        return False

    for x in range(0, writeloops):
        try:
            f.write(mystring)
        except:
            logging.debug('Cannot write to file %s', filename)
            logging.debug("Traceback: ", exc_info=True)
            return False
    f.close()
    os.remove(filename)
    return True


def diskspeedmeasure(dirname):
    # returns writing speed to dirname in MB/s
    # method: keep writing a file, until 0.5 seconds is passed. Then divide bytes written by time passed
    filesize = 1  # MB
    maxtime = 0.5  # sec
    filename = os.path.join(dirname, 'outputTESTING.txt')
    start = time.time()
    loopcounter = 0
    while True:
        if not writetofile(filename, filesize):
            return 0
        loopcounter += 1
        diff = time.time() - start
        if diff > maxtime:
            break
    return (loopcounter * filesize) / diff


if __name__ == "__main__":

    print "Let's go"

    if len(sys.argv) >= 2:
        dirname = sys.argv[1]
        if not os.path.isdir(dirname):
            print "Specified argument is not a directory. Bailing out"
            sys.exit(1)
    else:
        # no argument, so use current working directory
        dirname = os.getcwd()
        print "Using current working directory"

    try:
        speed = diskspeedmeasure(dirname)
        print("Disk writing speed: %.2f Mbytes per second" % speed)
    except IOError, e:
        # print "IOError:", e
        if e.errno == 13:
            print "Could not create test file. Check that you have write rights to directory", dirname
    except:
        print "Something else went wrong"
        raise

    print "Done"
