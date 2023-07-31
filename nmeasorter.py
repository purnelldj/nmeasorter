import numpy as np
from astropy.time import Time
import datetime
from pathlib import Path
from micropyGNSS import MicropyGPS
from os import listdir

# ALL CODE WRITTEN BY DAVID PURNELL

def nmea2nmea(nmeadir, outdir, antennaids, **kwargs):
    # nmeadir contains nmea files to analyse
    # outdir is the output directory
    # antenna ids are e.g., 'ACM0', 'ACM1'...

    # check if there are directories for each day
    dirlist = listdir(nmeadir)
    dirdt = []
    dirlist = [dl for dl in dirlist if len(dl) == 6]
    try:
        dirdt = [datetime.datetime.strptime(dl, "%d%m%y") for dl in dirlist]
    except:
        print('there might be a badly named directory - directories should be of form DDMMYY')
        exit()
    dirlist = [nmeadir + '/' + dl for dl in dirlist]
    
    # if it is a single directory containing nmea files
    if len(dirdt) == 0:
        dirdt = [False]
        dirlist = [nmeadir]
    
    # get start and end time if given
    if 'sdt' in kwargs and 'edt' in kwargs:
        sdt = kwargs.get('sdt')
        edt = kwargs.get('edt')

    # go through directory by directory to collect nmea files to analyze
    nmeafiles = []
    for tdir, tdt in zip(dirlist, dirdt):
        if 'sdt' in kwargs and 'edt' in kwargs and tdt:
            # now should check if in date range
            if tdt < sdt or tdt >= edt:
                # skip if outside range
                continue
        # you could add a different format here if you want, you just need to give the extension
        tnmea = listdir(tdir)
        tnmea = [tdir +'/' + tn for tn in tnmea if tn[-5:] == '.nmea']
        nmeafiles = np.append(nmeafiles, tnmea)
    
    # you could alternatively just directly give a list of nmea files
    if 'nmeafiles' in kwargs:
        nmeafiles = kwargs.get('nmeafiles')

    if len(nmeafiles) == 0:
        print('did not find any data!')
        exit()

    # now go through file by file and sort nmea data
    nmeafiles = np.sort(nmeafiles)
    counter = 0
    for nmeaf in nmeafiles:
        if np.mod(counter, 60) == 0:
            # display every hour assuming minute files, change if you have larger nmea files
            print(nmeaf.split('/')[-1])
        counter = counter + 1
        nmeasort(nmeaf, antennaids, outdir, **kwargs)


def nmeasort(tnmea, antennaids, outdir, multiant=True, outfiledt=24*60*60, decimate=1, **kwargs):
    # make new nmea data in gnssrefl format

    klprefix_ants = ['' for aid in antennaids]
    if 'klprefix_ants' in kwargs:
        klprefix_ants = kwargs.get('klprefix_ants')

    aidsize = len(antennaids[0])
    for aid in antennaids:
        if len(aid) != aidsize:
            print('all antenna IDs should be the same length...for now')
            exit()

    nmeat = [MicropyGPS() for aid in antennaids]
    gotdate = False
    printedonce = False
    for line in open(tnmea, 'r'):
        nmealine = line
        aidt = antennaids
        ii = 0
        if multiant:
            aidt = line[0:aidsize]
            nmealine = line[aidsize+1:]
            ii = [ii for ii in range(len(antennaids)) if antennaids[ii] == aidt]
            if len(ii) == 0:
                if not printedonce:
                    print('ISSUE - either unrecognised antenna or bad data - are you expecting this?')  # this error will only show once
                    printedonce = True
                continue
            if len(ii) > 1:
                print('ISSUE - non unique input antenna ID - stopping')
                exit()
            try:
                ii = ii[0]
            except IndexError:
                print('this should not happen')
                exit()
        if nmealine.count('$') > 1:  # error that happens sometimes - avoid data to be safe
            #print('dollarerror')
            continue
        if nmealine[1:6] == 'GNRMC':
            [nmeat[ii].update(tt) for tt in nmealine]  # feeding line into MicropyGNSS

        if nmealine[1:6] == 'GNRMC':  # use this line to obtain date and time
            gdatet = nmeat[ii].date
            gtimet = nmeat[ii].timestamp
            try:
                dtt = datetime.datetime(gdatet[2] + 2000, gdatet[1], gdatet[0], gtimet[0], gtimet[1], int(gtimet[2]))
            except ValueError:
                print('error with date or time - continuing')
                print(gdatet)
                print(gtimet)
                continue
            if gotdate:
                if dtt >= efdt:
                    [fs.close() for fs in f_nmea]
                    gotdate = False
            if not gotdate:
                tfdt = datetime.datetime(gdatet[2] + 2000, gdatet[1], gdatet[0], 0, 0, 0)
                efdt = tfdt + datetime.timedelta(seconds=outfiledt)
                # /nmea/ABCD/2021/ABCD0030.21.A
                nmeadirs = [outdir + '/nmea/' + klpf + '/' + tfdt.strftime('%Y') for klpf in klprefix_ants]
                [checkdir(nmead) for nmead in nmeadirs]
                nmeafs = [nmead + '/' + klpf + tfdt.strftime('%j0.%y.A') for nmead, klpf in zip(nmeadirs, klprefix_ants)]
                f_nmea = [open(nmeaf, 'a+') for nmeaf in nmeafs]
                gotdate = True
        
        if not gotdate or np.mod(int(gtimet[2]), decimate) != 0:
            continue

        f_nmea[ii].write(nmealine)

    if gotdate:
        [fs.close() for fs in f_nmea]


def checkdir(dirstr):
    # check if  directory exists or if not then make a new one
    Path(dirstr).mkdir(parents=True, exist_ok=True)


def datetime2gps(dt):
    timeobj = Time(dt, format='datetime')
    gpstime = timeobj.gps
    return gpstime
