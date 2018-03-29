<<<<<<< HEAD
from takePicture import * as camera

cm = camera.camera()

print cm.analyzeImage(cm.takePicture())
=======
from takePicture import camera as c

cm = c.camera()
print (cm.get_picture_info())
>>>>>>> origin/master
