import datetime
from nmeasorter import nmea2nmea

antennaids = ["ACM0", "ACM1", "ACM2", "ACM3"]  # names of antennas as automatically recorded in NMEA data
klprefix_ants = ["sjra", "sjrb", "sjrc", "sjrd"]  # for gnssrefl, you need to give a 4 char ID for each antenna 

# download nmea data from SJDLR here: https://drive.google.com/file/d/1CCWTYl2Wr8T0nHuXyBngcrMuL5ioKNPc/view?usp=drive_link
# unzip the data and put the contents in the following directory:
nmeadir = "C:\Users\dapur3\git\nmeasorter\local_processing\sjdlr\nmea"  # input data

outdir = "C:\Users\dapur3\git\nmeasorter\local_processing\sjdlr\nmea_kl"  # output directory
sdt = datetime.datetime(2021, 11, 14)
edt = datetime.datetime(2021, 11, 18)

nmea2nmea(nmeadir, outdir, antennaids, klprefix_ants, sdt=sdt, edt=edt)
