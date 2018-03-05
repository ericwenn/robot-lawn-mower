import json
from matplotlib.path import Path

def testSave():
    coordlist=[]
    coordlist.append({
        'x': 0,
        'y': 0
    })
    coordlist.append({
        'x': 0,
        'y': 3
    })
    coordlist.append({
        'x': 3,
        'y': 3
    })
    coordlist.append({
        'x': 3,
        'y': 0
    })
    saveCoords(coordlist,'coord.json')

def checkIfPointInArea(x,y):
    coords=loadCoords('coord.json')
    verts=[]
    codes=[]

    for coord in coords:
        verts.append((coord['x'],coord['y']))
    verts.append((0,0))

    codes.append(Path.MOVETO)
    for x in range(0,len(verts)-2):
        codes.append(Path.LINETO)
    codes.append(Path.CLOSEPOLY)

    path = Path(verts,codes)
    print verts
    print codes
    print path
    print path.contains_point((x,y))
def saveCoords(listOfCoords,filePath):
        with open(filePath, 'w') as f:
            json.dump(listOfCoords, f)

def loadCoords(filePath):
    try:
        with open(filePath, 'r') as f:
            datastore = json.load(f)
    except ValueError, e:
        print "No json"
        return []
    else:
        print " json"
        return datastore


def addCoordToList(x,y,filePath):
    coordlist = loadCoords(filePath)
    coordlist.append({
        'x':x,
        'y':y
    })
    saveCoords(coordlist,filePath)


#testSave()
#checkIfPointInArea(1,2)
while(True):
    x = int(float(raw_input("x: ")))
    y = int(float(raw_input("y: ")))
    addCoordToList(x,y,'coord.json')
    more = raw_input("continue?Y/N: ")

    if(more=="N"):
        print json.dumps(loadCoords('coord.json'))
        x = int(float(raw_input("x: ")))
        y = int(float(raw_input("y: ")))
        print checkIfPointInArea(x,y)
        break
