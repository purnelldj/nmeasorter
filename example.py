import datetime
from nmeasorter import nmea2fix, nmea2nmea
import sys
# change below path to your local directory
sys.path.append('/Users/dave/git/nmeasorter')

# download nmea data from SJDLR here: 
# https://drive.google.com/file/d/1CCWTYl2Wr8T0nHuXyBngcrMuL5ioKNPc/view?usp=drive_link
# unzip the data and put the contents in the following directory:
nmeadir = '/Users/dave/git/nmeasorter/local_processing/sjdlr/nmea'  # input data
# note: i put local_processing/ in the .gitignore file
# i suggest you make your own directory called local_processing

# first get an estimate of lat, lon, altitude from station (you will need this later for gnssrefl)
# pick any nmea file from data
lat, lon, hgt = nmea2fix(nmeadir + '/151121_0000.nmea')
# the output will print in the terminal:
# mean lat is 47.448818715277774
# mean lon is -70.36556071874999
# mean hgt is -17.704166666666666
# you can use these as inputs for example for https://gnss-reflections.org/rzones
# note that the precise location is not really important

outdir = '/Users/dave/git/nmeasorter/local_processing/sjdlr/gnssrefl_input'  # output directory
# sdt and edt are not required inputs
# will just go through all data if they are left out
sdt = datetime.datetime(2021, 11, 14)  # start time 
edt = datetime.datetime(2021, 11, 17)  # end time

antennaids = ["ACM0", "ACM1", "ACM2", "ACM3"]  
# antennaids = names of antennas as automatically recorded in NMEA data
klprefix_ants = ["sjra", "sjrb", "sjrc", "sjrd"]  
# for gnssrefl, you need to give a 4 char ID for each antenna


nmea2nmea(nmeadir, outdir, antennaids, klprefix_ants=klprefix_ants, sdt=sdt, edt=edt)
