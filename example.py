import datetime
from nmeasorter import nmea2fix, nmea2nmea
import sys
# change below path to your local directory
sys.path.append('/path/to/nmeasorter')

nmeadir = '/path/to/nmea'  # input data
outdir = '/path/to/gnssrefl_input'  # output directory

# first get an estimate of lat, lon, altitude from station (you will need this later for gnssrefl)
# pick any nmea file from data
lat, lon, hgt = nmea2fix(nmeadir + '/xxxx.nmea')
# the output will print something like this in the terminal:
# mean lat is 47.448818715277774
# mean lon is -70.36556071874999
# mean hgt is -17.704166666666666
# you can use these as inputs for https://gnss-reflections.org/rzones

# sdt and edt are not required inputs
# will just go through all data if they are left out
sdt = datetime.datetime(2021, 11, 14)  # start time 
edt = datetime.datetime(2021, 11, 17)  # end time

# antennaids = names of antennas as automatically recorded in NMEA data
antennaids = ["ACM0", "ACM1", "ACM2", "ACM3"]  # if you have multiple antennas
# for gnssrefl, you need to give a 4 char ID for each antenna
klprefix_ants = ["abc0", "abc1", "abc2", "abc3"]


nmea2nmea(nmeadir, outdir, antennaids, klprefix_ants=klprefix_ants, sdt=sdt, edt=edt)

