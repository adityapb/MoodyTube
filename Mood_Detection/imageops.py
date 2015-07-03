from PIL import Image
from numpy import array
import cv2

class XImage:
    def __init__(self,filename):
        self._readImage(filename)
        
    def _readImage(self,fname):
		if isinstance(fname,str): im=Image.open(fname).convert("L")
		else: im = Image.fromarray(fname)
		self._width,self._height=im.size
		self._pixellist =[pix for pix in im.getdata()]


def make_image(v, filename,imsize,scaled=True):
    v.shape = (-1,)    #change to 1 dim array
    im = Image.new('L', imsize)
    if scaled:
        a, b = v.min(), v.max()    
        v=((v-a)* 255/(b - a))    
    im.putdata(v)    
    im.save(filename)
    return array(im)
