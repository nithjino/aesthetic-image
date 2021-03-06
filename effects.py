from PIL import Image
import numpy as np
import wx, jpglitch, io

def wx_to_PIL(bitmap):
    size = tuple(bitmap.GetSize())
    try:
        buf = size[0]*size[1]*3*"\x00"
    except:
        del buf
        buf = bitmap.ConvertToImage().GetData()
    img = Image.frombuffer("RGBA",size,buf,"raw","RGBA",0,1)
    return img

def PIL_to_wx(image):
    width,height = image.size
    bitmap = wx.Bitmap.FromBufferRGBA(width,height,image.convert('RGBA').tobytes())
    return bitmap

def getBands(image):
    return image.split()

def shiftColor(image,color,x,y):
    bands = ("red", "green", "blue", "alpha")
    array = np.asarray(image).transpose().copy()
    #searches for given element in tuple and returns the index
    band  = bands.index(color)

    '''
    np.roll(input_array, shift, axis)
    shift and axis can be int or tuple of ints
    roll shifts that elements down the given amount
    '''
    array[band] = np.roll(array[band], (x, y), (0, 1))
    return Image.fromarray(array.transpose())

def glitch(image,amount,seed,iterations):
    if image.format is not 'JPEG':
        image = image.convert('RGB')
    image_bytes = io.BytesIO()
    image.save(image_bytes,format='JPEG')
    image_bytes = image_bytes.getvalue()
    jpeg_obj = jpglitch.Jpeg(image_bytes,amount,seed,iterations)
    image = jpeg_obj.save_image()
    return image
