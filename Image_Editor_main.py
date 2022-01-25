from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
from math import floor
import math
import numpy as np

root = Tk()
root.geometry("1200x700")
root.title("IMAGE EDITOR")

# canvas defined
image_canvas = Canvas(root, width = 670, height = 500, bg = "white")    # canvas where image is placed
image_canvas.place(relx = 0.3, rely = 0.5, anchor= CENTER)

#Frames defined
colour_change_frame = LabelFrame(root, text = "COLOUR MANIPULATION", padx = 20, pady = 20)
colour_change_frame.place(relx = 0.85, rely = 0.33, anchor = NE)

image1 = Image.open("Images/scene1.png")
h = image1.height
w = image1.width
m = max(h, w)
if h < 400 and w < 600:
    h = h
    w = w
else:
    if w == m:
         h = round(h/w * 600)
         w = 600
    else: 
        w = round((w/h) * 400)
        h = 400
ims = image1.resize((w, h))
image2 = ImageTk.PhotoImage(ims)
image_show = image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def new_image():           # function for new image button 
    global image1 
    global image2
    global image_show
    global ims, h, w
    image_canvas.delete(image_show)
    filename = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select an image", filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    image1 = Image.open(filename)
    h = image1.height
    w = image1.width
    m = max(h, w)
    if h < 400 and w < 600:
        h = h
        w = w
    else:
        if w == m:
            h = round(h/w * 600)
            w = 600
        else: 
            w = round((w/h) * 400)
            h = 400
    ims = image1.resize((w, h))
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def save_image():    # function to save images
    global image1 
    savefile = filedialog.asksaveasfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Save Image", filetypes=(("png image", "*.png"), ("jpg image", "*.jpg")), defaultextension=(".png"))
    ims.save(savefile)
    
def flip_vert():      # function for flip vertical
    global ims, w, h
    global image_show
    global image2
    image_canvas.delete(image_show)

    # algorithm for flip vertical:
    for x in range(1, w):
        for y in range(1, round(h/2)):
            global p_shift
            pixel_access = ims.load()
            p_shift =  pixel_access[x, y]
            pixel_access[x, y] = pixel_access[x, h - y]
            pixel_access[x, h - y] = p_shift

    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def flip_horiz():      # function for flip horizontal
    global ims,w, h
    global image_show
    global image2
    image_canvas.delete(image_show)
    
    # algorithm for flip horizontal:
    for x in range(1, round(w/2)):
        for y in range(1, h):
            global p_shift
            pixel_access = ims.load()
            p_shift =  pixel_access[x, y]
            pixel_access[x, y] = pixel_access[w - x, y]
            pixel_access[w - x, y] = p_shift

    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def inv_img():      # function for invert image
    global ims, w, h
    global image_show
    global image2
    image_canvas.delete(image_show)
    
    # algorithm to invert colours:
    for x in range(1, w):
        for y in range(1, h):
            global inv_p
            pixel_access = ims.load()
            inv_p = (255 - floor(pixel_access[x,y][0]), 255 - floor(pixel_access[x,y][1]), 255 -  floor(pixel_access[x,y][2]))
            pixel_access[x,y] = inv_p 

    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def rot():      # function for rotating right
    global ims, w, h, rot_slider
    global image_show
    global image2
    
    # algorithm to rotate by using numpy arrays:
    image = np.array(ims)
    angle = int(rot_slider.get())  #gettinng angle value from slider

    image_canvas.delete(image_show)

    angle=math.radians(angle)                               #converting degrees to radians
    cosine=math.cos(angle)
    sine=math.sin(angle)

    new_height  = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1     # height and width of the new image that is to be formed
    new_width  = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1      
    output=np.zeros((new_height,new_width,image.shape[2]))    # defining output numpy array 

    original_centre_height   = round(((image.shape[0]+1)/2)-1)   # centre of the image about which we have to rotate the image
    original_centre_width    = round(((image.shape[1]+1)/2)-1)    

    new_centre_height= round(((new_height+1)/2)-1)        # Find the centre of the new image that will be obtained
    new_centre_width= round(((new_width+1)/2)-1)          

    for i in range(h):
        for j in range(w):
            y=image.shape[0]-1-i-original_centre_height           #co-ordinates of pixel with respect to the centre of original image
            x=image.shape[1]-1-j-original_centre_width                      

            new_y=round(-x*sine+y*cosine)      #co-ordinate of pixel with respect to the rotated image
            new_x=round(x*cosine+y*sine)

            new_y=new_centre_height-new_y
            new_x=new_centre_width-new_x
            if 0 <= new_x < new_width and 0 <= new_y < new_height and new_x>=0 and new_y>=0:
                output[new_y,new_x,:]=image[i,j,:]    
    h = new_height
    w = new_width
    ims = Image.fromarray((output).astype(np.uint8)) 
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def image_sat_slide(var):            #function for saturation slider
    global ims, image_sat_slider
    global image_show
    global image2
    image_canvas.delete(image_show)
    if int(image_sat_slider.get()) >= 0:           #defining scale of saturation
        x = float(image_sat_slider.get())/20 + 1
    else:
        x = 1 - abs(float(image_sat_slider.get())/20)
    im_sat = ImageEnhance.Color(ims)
    ims_var = im_sat.enhance(x)
    image2 = ImageTk.PhotoImage(ims_var)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def image_sat():            #function for saturation button
    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to apply saturation")
    if mess_box == 1:
        global ims, image_sat_slider
        global image_show
        global image2
        image_canvas.delete(image_show)
        if int(image_sat_slider.get()) >= 0:             #defining sacle of saturation
            x = float(image_sat_slider.get())/20 + 1
        else:
            x = 1 - abs(float(image_sat_slider.get())/20)
        im_sat = ImageEnhance.Color(ims)
        ims = im_sat.enhance(x)
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
        image_sat_slider.set(0)
    else:
        return

def image_sharp_slide(var):       #function for sharpness slider
    global ims, image_sat_slider
    global image_show
    global image2
    image_canvas.delete(image_show)
    x = 0.5 + float(image_sharp_slider.get())/2      #defining sharpness scale
    im_sat = ImageEnhance.Sharpness(ims)
    ims_var = im_sat.enhance(x)
    image2 = ImageTk.PhotoImage(ims_var)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def image_sharp():     #function for sharpness button
    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to apply sharpness")
    if mess_box == 1:
        global ims, image_sat_slider
        global image_show
        global image2
        image_canvas.delete(image_show)
        x = 0.5 + float(image_sharp_slider.get())/2      #defining sharpness scale
        im_sat = ImageEnhance.Sharpness(ims)
        ims = im_sat.enhance(x)
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
        image_sharp_slider.set(1)
    else:
        return

def image_exp_slide(var):       #function for exposure slider
    global ims, image_sat_slider
    global image_show
    global image2
    image_canvas.delete(image_show)
    if int(image_exp_slider.get()) >= 0:             #defining sacle of exposure
        x = float(image_exp_slider.get())/100 + 1
    else:
        x = 1 - abs(float(image_exp_slider.get())/200)
    im_sat = ImageEnhance.Brightness(ims)
    ims_var = im_sat.enhance(x)
    image2 = ImageTk.PhotoImage(ims_var)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def image_exp():     #function for exposure button
    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to apply exposure")
    if mess_box == 1:
        global ims, image_sat_slider
        global image_show
        global image2
        image_canvas.delete(image_show)
        if int(image_exp_slider.get()) >= 0:             #defining sacle of exposure
            x = float(image_exp_slider.get())/100 + 1
        else:
            x = 1 - abs(float(image_exp_slider.get())/200)
        im_sat = ImageEnhance.Brightness(ims)
        ims = im_sat.enhance(x)
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
        image_sharp_slider.set(1)
    else:
        return

# BUTTONS DEFINAITION
new_file_button = Button(root, text = "New Image", command= new_image)
save_file_button = Button(root, text = "Save", command= save_image)
flip_vert_button = Button(root, text = "FLIP VERTICAL", command = flip_vert, padx = 50, pady = 20)
flip_horiz_button = Button(root, text = "FLIP HORIZONTAL", command = flip_horiz, padx = 50, pady = 20)
inv_img_button = Button(colour_change_frame, text = "INVERT IMAGE", command = inv_img, padx = 50, pady = 20)
rot_button = Button(root, text = "ROTATE IMAGE", command = rot, padx = 50, pady = 20)
image_sat_button = Button(root, text = "APPLY SATURATION", command = image_sat, padx = 20, pady = 10)
image_sharp_button = Button(root, text = "APPLY SHARPNESS", command = image_sharp, padx = 20, pady = 10)
image_exp_button = Button(root, text = "APPLY EXPOSURE", command = image_exp, padx = 20, pady = 10)

# BUTTONS EXECUTION
new_file_button.grid(row=0,column=0)
save_file_button.grid(row = 0, column =1)
flip_vert_button.place(relx = 0.75, rely = 0.2, anchor= NE)
flip_horiz_button.place(relx = 0.95, rely = 0.2, anchor= NE)
inv_img_button.pack()   
rot_button.place(relx = 0.95, rely = 0.54, anchor= NE)
image_sat_button.place(relx = 0.95, rely = 0.67, anchor= NE)
image_sharp_button.place(relx = 0.95, rely = 0.8, anchor= NE)
image_exp_button.place(relx = 0.95, rely = 0.93, anchor= NE)


#SLIDERS
rot_slider = Scale(root, from_= 0, to=360, length = 180, orient=HORIZONTAL)
rot_slider.place(relx = 0.75, rely = 0.54, anchor= NE)
image_sat_slider = Scale(root, from_= -100, to = 100, length = 180, orient=HORIZONTAL, command= image_sat_slide)
image_sat_slider.set(0)
image_sat_slider.place(relx = 0.75, rely = 0.67, anchor= NE)
image_sharp_slider = Scale(root, from_= 1, to = 100, length = 180, orient=HORIZONTAL, command= image_sharp_slide)
image_sharp_slider.place(relx = 0.75, rely = 0.8, anchor= NE)
image_exp_slider = Scale(root, from_= -100, to = 100, length = 180, orient=HORIZONTAL, command= image_exp_slide)
image_exp_slider.set(0)
image_exp_slider.place(relx = 0.75, rely = 0.93, anchor= NE)
root.mainloop()