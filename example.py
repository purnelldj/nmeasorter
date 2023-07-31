import datetime
from nmeasorter import nmea2nmea
import sys
# change below path to your local directory
sys.path.append('/Users/dave/git/nmeasorter')

# download nmea data from SJDLR here: 
# https://drive.google.com/file/d/1CCWTYl2Wr8T0nHuXyBngcrMuL5ioKNPc/view?usp=drive_link
# unzip the data and put the contents in the following directory:
nmeadir = '/Users/dave/git/nmeasorter/local_processing/sjdlr/nmea'  # input data
# note: i put local_processing/ in the .gitignore file
# i suggest you make your own directory called local_processing

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
