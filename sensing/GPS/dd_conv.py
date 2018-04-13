import subprocess

subprocess.check_output(["stty", "-F", "/dev/serial0", "raw", "9600", "cs8", "clocal", "-cstopb"])

while(True):
    str=subprocess.check_output(["cat", "/dev/serial0", "|", "grep", "GPRMC"]) 

    #sentence to decimal degrees convertion code

    data = str.split(",")

    lat=data[3]
    lat_sign=data[4]
    lng=data[5]
    lng_sign=data[6]

    if(lat_sign == "N"):
        lat_sign = 1
    else:
        lat_sign = -1

    if(lng_sign == "E"):
        lng_sign = 1
    else:
        lng_sign = -1

    dd=[lat_sign*(float(lat[0:2])+(float(lat[2:])/60)),lng_sign*(float(lng[0:3])+(float(lng[3:]))/60)]
    print(dd)


