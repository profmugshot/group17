import Tkinter as tk
import ImageDraw, Image, ImageTk
import sys, math
import os.path

eyePos=[[],[]]
cnt=0

def getEyePos(image):
    window = tk.Tk();
    canvas = tk.Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)
    
    def click(event):
        global cnt
        cnt+=1
        print "clicked at: ", event.x, event.y
        if cnt==1:
            eyePos[0] = [event.x, event.y]
        elif cnt==2:
            eyePos[1]= [event.x, event.y]
            cnt=0
            window.quit()
            window.destroy()
    
    canvas.bind("<Button-1>", click)
    window.mainloop()
    
def Distance(p1,p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx+dy*dy)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
    if (scale is None) and (center is None):
        return image.rotate(angle=angle, resample=resample)
    nx,ny = x,y = center
    sx=sy=1.0
    if new_center:
        (nx,ny) = new_center
    if scale:
        (sx,sy) = (scale, scale)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine/sx
    b = sine/sx
    c = x-nx*a-ny*b
    d = -sine/sy
    e = cosine/sy
    f = y-nx*d-ny*e
    return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (200,200)):
    # calculate offsets in original image
    offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
    offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
    # calc rotation angle in radians
    rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
    # distance between them
    dist = Distance(eye_left, eye_right)
    # calculate the reference eye-width
    reference = dest_sz[0] - 2.0*offset_h
    # scale factor
    scale = float(dist)/float(reference)
    # rotate original around the left eye
    image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
    # crop the rotated image
    crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
    crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
    image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
    # resize it
    image = image.resize(dest_sz, Image.ANTIALIAS)
    return image

if __name__ == "__main__":
#    getEyePos("E:/Documents/Dropbox/CMPT 456/Proj/faceRec/JianPei.0.jpg")
#    print eyePos
    _PATH="E:/Documents/Dropbox/CMPT 456/Proj/faceRec/img"
    
    if len(sys.argv) == 2:
        BASE_PATH=sys.argv[1]
    else:
        print "usage: create_csv <base_path>"
        BASE_PATH=_PATH
    print "<base_path> set to %s" % BASE_PATH

    SEPARATOR=";"
    label = 0
#    for dirname, dirnames, filenames in os.walk(BASE_PATH):
#        for filenames in dirnames:
#            subject_path = os.path.join(dirname, BASE_PATH)
    subject_path=BASE_PATH
    for filename in os.listdir(subject_path):
        abs_path = "%s/%s" % (subject_path, filename)
        if os.path.isfile(abs_path):
            image = Image.open(abs_path)
            getEyePos(image)
            save_path= "%s/%s" % (subject_path,filename[:filename.find('.')])
            save_file= "%s/%s" % (save_path,filename)
            if not os.path.exists(save_path):os.makedirs(save_path)
            CropFace(image, eyePos[0], eyePos[1], offset_pct=(0.25,0.25)).save(save_file)