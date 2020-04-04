
import os
import tensorflow as tf
import cv2
import numpy as np
import math
IMG_SIZE = 60
dir =r"" #file where sequential images are kept taken by the UAV 
model = tf.keras.models.load_model( r"") # place where trained modal is kept

mapp = {225:"SW",0:"N",180:"S",270:"E",90:"W",315:"NE",45:"NW",135:"SW"} #pridection given by finally
mapp2 = {0:225 ,1:0,2:180,3:270 ,4: 90,5:315,6:45,7:135} #coverted to degree(from CNN modal) for final estimation of orent.

def revalimg(img):
       y=0
       x=0      
       crop_img = img[y:y-5, x:x-5]
       crop_img=cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
       crop_img = cv2.resize(crop_img, (IMG_SIZE,IMG_SIZE))
       crop_img= np.reshape(crop_img,(-1,IMG_SIZE,IMG_SIZE,1))
       return crop_img

def picorient(ii):    
        a= os.path.join(dir,ii)
        img = cv2.imread(a)
        img  =revalimg(img)
        aa = model.predict(img)
        NUM = (np.argmax(aa))
        val = mapp2[NUM]
        return val
   


def central(b):
    if ((b>0 and b<22.5) or (b>337.5 and b< 360)):
        b = 0
    elif(b>22.5 and b< 67.5):
        b=45
    elif(b>67.5 and b< 112.5):
        b=90
    elif(b>112.5 and b< 157.5):
        b=135
    elif(b>157.5 and b< 202.5):
        b=180
    elif(b>202.5 and b< 245.5):
        b=225
    elif(b>245.5 and b< 292.5):
        b=270
    elif(b>292.5 and b< 337.5):
        b=315
    return b
     

def orientation():
    aa =os.listdir(dir)
  #  print(aa)
 
    for i in range(1,len(aa)): 
        lat1 ,long1 ,h1 = aa[i-1].split()
       # lat1 ,long1  =  map(float, aa[i-1].strip().split())
        lat2 ,long2 ,h2 = aa[i].split()
        dlon =  (float(long2) - float(long1))
        y = math.sin(dlon) * math.cos(float(lat2))
        x = math.cos(float(lat1)) * math.sin(float(lat2)) - math.sin(float(lat1))* math.cos(float(lat2)) * math.cos(float(dlon))
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng = ((brng + 360) % 360)
        aaa = central(brng)
       # print(aa[i-1])
        #print(aaa)
        val = picorient(aa[i-1])
        final_head = aaa + val
       # print(final_head)
        
        if (final_head >= 360):
            final_head = final_head -360
        st = mapp[final_head]
        
        print(st)
    
orientation()
#print(mapp2[5])        
#picorient()       