from PIL import Image

img = Image.open("color-grid.jpg")
(imageWidth, imageHeight)=img.size

gridx=400
gridy=400
rangex=imageWidth/gridx
rangey=imageHeight/gridy
print rangex*rangey
for x in xrange(rangex):
    for y in xrange(rangey):
        bbox=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
        slice_bit=img.crop(bbox)
        slice_bit.save('out/xmap_'+str(x)+'_'+str(y)+'.png', optimize=True, bits=6)
        print 'out/xmap_'+str(x)+'_'+str(y)+'.png'
print imageWidth
