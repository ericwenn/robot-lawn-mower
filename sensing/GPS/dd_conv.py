import serial
from time import sleep
ser = serial.Serial('/dev/serial0', 9600, timeout=0.5)

config = False
coords[]

#Will return a tuple [a,b] where a is latitude in decimal degrees and b is longitude...
def getDDconv():
    while True:
        try:
            str=ser.readline()
        except:
            pass
        if(str[1:6]!="GPRMC"):
            continue


        #sentence to decimal degrees conversion code

        data = str.split(",")

        lat=data[3]
        lat_sign=data[4]
        lng=data[5]
        lng_sign=data[6]

        if(lat=="" or lat_sign=="" or lng=="" or lng_sign==""):
                raise ValueError('NO FIX!')

        if(lat_sign == "N"):
            lat_sign = 1
        else:
            lat_sign = -1

        if(lng_sign == "E"):
            lng_sign = 1
        else:
            lng_sign = -1

        dd=[lat_sign*(float(lat[0:2])+(float(lat[2:])/60)),lng_sign*(float(lng[0:3])+(float(lng[3:]))/60)]
        return(dd)

def save_point():
    if(config):
        x = 0
        y = 0
        c = [0,0]
        for i in range(0, 5):
            e_count = 0
            while(True):
                try:
                    c = getDDconv()
                    break;
                except ValueError:
                    e_count+=1
                    if(e_count > 5):
                        raise ValueError('Save time out')

            x = x + c[0]
            y = y + c[1]
        point=[c[0]/5,c[1]/5]
        coords.append(point)
    else:
        raise Exception('Not possible outside of config mode, please run setup_config(True) first')

def setup_config(val):
    if(val):
        config = True
    else:
        file = open("config_data.java", "a")
        for c in coords:
            file.write(str(c[0])+","+str(c[1]+"\n"))
        config = False

def load_file(file_name)
    coords_tmp[]
    with open(file_name) as file
        for line in file
           splitted_line = line.split(",")
           coords_tmp.append( [ int(splitted_line[0]) , int(splitted_line[1]) ] )
    coords = coords_tmp
    
def isPointInPath(x, y, poly):
    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i                              
    return c


