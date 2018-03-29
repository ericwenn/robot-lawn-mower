from takePicture import * as camera

cm = camera.camera()

print cm.analyzeImage(cm.takePicture())
