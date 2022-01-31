from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
from math import floor
import math
import numpy as np
import cv2 as cv
import pandas as pd

root = Tk()
root.geometry("1300x700")
root.title("IMAGE EDITOR")

# canvas defined
image_canvas = Canvas(root, width = 670, height = 500, bg = "white")    # canvas where image is placed
image_canvas.place(relx = 0.3, rely = 0.5, anchor= CENTER)

#Frames defined
colour_change_frame = LabelFrame(root, text = "COLOUR MANIPULATION", pady = 20)
colour_change_frame.place(relx = 0.96, rely = 0.33, anchor = NE)
multiple_gen_frame = LabelFrame(root, text = "MULTIPLE CERTIFICATES GENERATION")
multiple_gen_frame.place(relx = 0.57, rely = 0.015, anchor = NE)

#INPUTS DEFINED
text_entry = Entry(root, width = 50)
text_entry.place(relx = 0.825, rely= 0.88, anchor = NE)

#LABELS DEFINED
text_entry_label = Label(root, text = "ENTER TEXT: ").place(relx = 0.535, rely= 0.88)
text_entry_label = Label(root, text = "*NOTE - (PRESS 'ENTER' KEY TWICE TO CROP").place(relx =0.8, rely= 0.095, anchor = NE)
text_entry_label = Label(root, text = "THE IMAGE AFTER SELECTING AREA)").place(relx =0.8, rely= 0.12, anchor = NE)

img_filename = "Images/scene1.png"
image1 = Image.open(img_filename)
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
    global image1, img_filename
    global image2
    global image_show
    global ims, h, w
    img_filename = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select an image", filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    image1 = Image.open(img_filename)
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
    next_button["state"] = "disable"           #disable next image button whenver new image is loaded
    back_button["state"] = "disable"            #disable previous image button whenver new image is loaded
    gen_cert_button["state"] = "disable"             #disable generate certificate button whenver new image is loaded

def save_image():    # function to save images
    global image1 
    savefile = filedialog.asksaveasfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Save Image", filetypes=(("png image", "*.png"), ("jpg image", "*.jpg")), defaultextension=(".png"))
    ims.save(savefile)
    
def flip_vert():      # function for flip vertical
    global ims, w, h
    global image_show
    global image2

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
    
    # algorithm to invert colours:
    for x in range(1, w):
        for y in range(1, h):
            global inv_p
            pixel_access = ims.load()
            inv_p = (255 - floor(pixel_access[x,y][0]), 255 - floor(pixel_access[x,y][1]), 255 -  floor(pixel_access[x,y][2]))
            pixel_access[x,y] = inv_p 

    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def img_bw():         #function for converting image to black and white
    global ims
    global image_show
    global image2
    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to convert the image into a black and white image")   #applying message box
    if mess_box == 1:
        image_canvas.delete(image_show)

        #algorithm for converting image into black and white image using grayscale formula 
        p_access = ims.getdata()         
        list_ni = []
        for x in p_access:
                list_ni.append(x[0]*0.299 + x[1]*0.587 + x[2]*0.114)       #Here i used the (r, g, b) to grayscale code formula which is 0.299 * R + 0.587 * G + 0.114 * B
        ims = Image.new("L", ims.size)  
        ims.putdata(list_ni)  

        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
    else:
        return

def rot():      # function for rotating
    global ims, w, h, rot_slider
    global image_show
    global image2
    
    ims = ims.rotate(rot_slider.get())
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
    rot_slider.set(0)

def image_sat_slide(var):            #function for saturation slider
    global ims
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
    global ims
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
    global ims
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
        global ims
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
        image_exp_slider.set(0)
    else:
        return

def crop_img():                  #function for cropping image
    global ims, roi
    global image_show
    global image2
    
    img_read = cv.imread(img_filename)
    img_read =   cv.resize(img_read, (w, h))
    roi = cv.selectROI("SELECT AREA", img_read)
    cv.waitKey(0)
    image_canvas.delete(image_show)

    #algorithm for cropping image using numpy array
    image_arr = np.array(ims)                             #array initialisation
    image_arr = image_arr[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
    ims = Image.fromarray(image_arr)

    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

def ret_img():              #function for retrieving image
    global image1 
    global image2
    global image_show
    global ims, h, w

    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to discard the changes")
    if mess_box == 1:
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
    else:
        return

def insert_text():                #function to insert text on image
    global text, font_entry, x, y
    font_entry = colorchooser.askcolor()[1]
    def change_position(event):
        global text, x, y
        x = event.x
        y = event.y

        if text in image_canvas.find_overlapping(str(x-10), str(y-10), str(x+10), str(y+10)):
            image_canvas.coords(text, x, y)  # move text to mouse position
    
    text = image_canvas.create_text(50, 50, text= text_entry.get(), fill= font_entry, font=('arial', 20))
    image_canvas.bind("<B1-Motion>", change_position)

def fix_pos():                              #function to fix position of inserted text
    global ims, x, y, font_entry
    global image_show
    global image2
    image_canvas.delete(image_show)
    text_font = ImageFont.truetype("arial", 26)
    fix_text = ImageDraw.Draw(ims)
    fix_text.text((x-40, y-50), text_entry.get(), font_entry, font = text_font)
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
    text_entry.delete(0, END)

def face_det():                            #function to detect face
    global img_filename, h, w 
    img_read = cv.imread(img_filename)
    img_read = cv.resize(img_read, (w, h))
    img_gray = cv.cvtColor(img_read, cv.COLOR_BGR2GRAY)

    #algorithm for face detection
    haar_cascade_face = cv.CascadeClassifier("haar_FaceDetect.xml")              #used haar cascades (copiied 'haar_FaceDetect.xml' from github opencv)
    face_det_rect = haar_cascade_face.detectMultiScale(img_gray, scaleFactor = 1.1, minNeighbors = 4)
    for (x, y, w_f, h_f) in face_det_rect:                                 #making rectangle around detected face
        cv.rectangle(img_read, (x, y), (x + w_f, y + h_f), (0,255,0), thickness = 2)           
    
    cv.imshow("DETECTED FACES", img_read)

def open_cvs():                     #function to open cvs file                    
    global file_cvs
    file_cvs = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select a CSV file", filetypes=(("csv files", "*.csv"), ("excel files", "*.xlsx")))
    messagebox.showinfo("INFORMATION", "DOUBLE CLICK on the template at the point where you want to place the name on the certificate and that will also ENABLE 'GENERATE CERTIFICATE' button")

def coord(event):                                #function to get coordinates of double click on the template
    global width, height, ims
    width = int(event.x) - int((670 - ims.width)/2)
    height = int(event.y) - int((500 - ims.height)/2) - 10
    gen_cert_button["state"] = "normal"

image_canvas.bind("<Double-Button-1>", coord)   #binding double click

def get_cert():                               #function to generate multiple certificate after reading the csv file
    global font_size, img_filename
    global width, height, names
    global ims, image2

    #algorithm for printing  
    names = pd.read_csv(file_cvs)                #read csv file using pandas library
    for i,row in names.iterrows():
        empty_img = Image.open(img_filename)
        empty_img = empty_img.resize((w, h))
        name = str(row['NAME'])
        name = name.title()
        font_size = 15
        font = ImageFont.truetype("arial", 150)
        w1_img = empty_img.width 
        w2, h2 = font.getsize(name)
        if w1_img%w2 >= 2:
             font_size = w1_img/20

        font = ImageFont.truetype("arial", int(font_size))              #editing the selected template by placing the name on the template
        image_editable = ImageDraw.Draw(empty_img)
        image_editable.multiline_text((width, height), name, (35, 57, 75), font=font)
        empty_img.save("{}_{}.png".format((i + 1), name.replace(" ", "_")))
        
    print("Process Complete!")
    ims = Image.open("{}_{}.png".format((1), names["NAME"][0]))
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

    next_button["state"] = "normal"
    back_button["state"] = "normal"

def next_img(i_n):                             #next button to view multiple certificates generated
    global ims, image2, image_show, names
    global next_button, back_button
    image_canvas.delete(image_show)

    if i_n >= len(names.index):
        return

    else:
        ims = Image.open("{}_{}.png".format((i_n + 1), names["NAME"][i_n]))              
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

        next_button = Button(root, text = "NEXT", command = lambda: next_img(i_n + 1), padx = 7, pady = 4)      #used recurssion to generate the next image
        next_button.place(relx = 0.51, rely = 0.865, anchor= NE)
        back_button = Button(root, text = "BACK", command = lambda: back_img(i_n - 1), padx = 7, pady = 4)      #used recurssion to generate the previous image
        back_button.place(relx = 0.08, rely = 0.865, anchor= NE)
    
def back_img(i_n):                             #back button to view multiple certificates generated
    global ims, image2, image_show, names
    global back_button, next_button
    image_canvas.delete(image_show)

    if i_n < 0:
        return

    else:
        ims = Image.open("{}_{}.png".format((i_n + 1), names["NAME"][i_n]))
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

        next_button = Button(root, text = "NEXT", command = lambda: next_img(i_n + 1), padx = 7, pady = 4)          #used recurssion to generate the next image
        next_button.place(relx = 0.51, rely = 0.865, anchor= NE)
        back_button = Button(root, text = "BACK", command = lambda: back_img(i_n - 1), padx = 7, pady = 4)          #used recurssion to generate the previous image
        back_button.place(relx = 0.08, rely = 0.865, anchor= NE)
    
def high_bord():          #function to highlight border
    global ims, image2, image_show
    mess_box = messagebox.askyesno("Popup!", "Are you sure that you want to highlight border of the image")
    if mess_box == 1:
        img_read = cv.imread(img_filename)
        img_read =   cv.resize(img_read, (w, h))
        img_canny = cv.Canny(img_read, 125, 150)           #used edge cascade
        ims = Image.fromarray(img_canny)
        image2 = ImageTk.PhotoImage(ims)
        image_canvas.create_image(335, 250, anchor = CENTER, image = image2)
    else:
        return

def blend_img():         #function to blend images
    global ims, image2, image_show
    global w, h

    #algorithm to blend images using numpy arrays
    img1_arr = np.array((ims))     
    img2_filename = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select an image", filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    img_blend = Image.open(img2_filename)
    ims2 = ims = img_blend.resize((w, h))
    img2_arr = np.array(ims2) 
    blend_res = (img1_arr * 0.6 + img2_arr * 0.4).astype(np.uint8)   # Blending imsges in
    ims = Image.fromarray(blend_res)
    image2 = ImageTk.PhotoImage(ims)
    image_canvas.create_image(335, 250, anchor = CENTER, image = image2)

# BUTTONS DEFINAITION
new_file_button = Button(root, text = "New Image", command= new_image, bd = 4)
save_file_button = Button(root, text = "Save", command= save_image, bd = 4)
flip_vert_button = Button(root, text = "FLIP VERTICAL", command = flip_vert, padx = 50, pady = 20, bd = 4)
flip_horiz_button = Button(root, text = "FLIP HORIZONTAL", command = flip_horiz, padx = 50, pady = 20, bd = 4)
inv_img_button = Button(colour_change_frame, text = "INVERT IMAGE", command = inv_img, padx = 30, pady = 15, bd = 4)
rot_button = Button(root, text = "ROTATE IMAGE", command = rot, padx = 30, pady = 8)
image_sat_button = Button(root, text = "APPLY SATURATION", command = image_sat, padx = 20, pady = 5)
image_sharp_button = Button(root, text = "APPLY SHARPNESS", command = image_sharp, padx = 20, pady = 5)
image_exp_button = Button(root, text = "APPLY EXPOSURE", command = image_exp, padx = 20, pady = 5)
image_bw_button = Button(colour_change_frame, text = "BLACK AND WHITE IMAGE", command = img_bw, padx = 30, pady = 15, bd = 4)
crop_button = Button(root, text = "CROP IMAGE", command = crop_img, padx = 50, pady = 20, bd = 4)
ret_button = Button(root, text = "RETRIEVE ORIGINAL IMAGE", command = ret_img, padx = 30, pady = 10, bd = 4)
insert_text_button = Button(root, text = "INSERT TEXT", command = insert_text, padx = 10, pady = 5)
fix_pos_button = Button(root, text = "FIX POSITION", command = fix_pos, padx = 10, pady = 5)
face_det_button = Button(root, text = "DETECT FACE IN THE IMAGE", command = face_det, padx = 20, pady = 8, bd = 4)
next_button = Button(root, text = "NEXT", command = lambda: next_img(1), padx = 7, pady = 4, state = DISABLED)
back_button = Button(root, text = "BACK", command = back_img, padx = 7, pady = 4, state = DISABLED)
sel_csv_button = Button(multiple_gen_frame, text = "SELECT .CSV FILE", command = open_cvs, padx = 15, pady = 8, bd = 4)
gen_cert_button = Button(multiple_gen_frame, text = "GENERATE CERTIFICATES", command = get_cert, padx = 15, pady = 8, state = DISABLED, bd = 4)
high_bord_button = Button(root, text = "HIGHLIGHT BORDER", command = high_bord, padx = 25, pady = 10, bd = 4)
blend_img_button = Button(root, text = "BLEND IMAGE", command = blend_img, padx = 50, pady = 15, bd = 4)

# BUTTONS EXECUTION
new_file_button.grid(row=0,column=0)
save_file_button.grid(row = 0, column =1)
flip_vert_button.place(relx = 0.75, rely = 0.2, anchor= NE)
flip_horiz_button.place(relx = 0.95, rely = 0.2, anchor= NE)
inv_img_button.grid(row = 0, column = 0, padx= 20)   
rot_button.place(relx = 0.95, rely = 0.54, anchor= NE)
image_sat_button.place(relx = 0.95, rely = 0.63, anchor= NE)
image_sharp_button.place(relx = 0.95, rely = 0.71, anchor= NE)
image_exp_button.place(relx = 0.95, rely = 0.79, anchor= NE)
image_bw_button.grid(row = 0, column = 1, padx= 20)   
crop_button.place(relx = 0.95, rely = 0.08, anchor= NE)
ret_button.place(relx = 0.85, rely = 0.01, anchor= NE)
insert_text_button.place(relx = 0.91, rely = 0.865, anchor= NE)
fix_pos_button.place(relx = 0.994, rely = 0.865, anchor= NE)
face_det_button.place(relx = 0.2, rely = 0.07, anchor= CENTER)
back_button.place(relx = 0.08, rely = 0.865, anchor= NE)
next_button.place(relx = 0.51, rely = 0.865, anchor= NE)
sel_csv_button.grid(row = 0, column = 0, padx= 10, pady = 10) 
gen_cert_button.grid(row = 0, column = 1, padx= 10, pady = 10) 
high_bord_button.place(relx = 0.82, rely = 0.93, anchor= NE)
blend_img_button.place(relx = 0.35, rely = 0.91, anchor= NE)

#SLIDERS
rot_slider = Scale(root, from_= 0, to=360, length = 180, orient=HORIZONTAL)
rot_slider.place(relx = 0.75, rely = 0.53, anchor= NE)
image_sat_slider = Scale(root, from_= -100, to = 100, length = 180, orient=HORIZONTAL, command= image_sat_slide)
image_sat_slider.set(0)
image_sat_slider.place(relx = 0.75, rely = 0.62, anchor= NE)
image_sharp_slider = Scale(root, from_= 1, to = 100, length = 180, orient=HORIZONTAL, command= image_sharp_slide)
image_sharp_slider.place(relx = 0.75, rely = 0.7, anchor= NE)
image_exp_slider = Scale(root, from_= -100, to = 100, length = 180, orient=HORIZONTAL, command= image_exp_slide)
image_exp_slider.set(0)
image_exp_slider.place(relx = 0.75, rely = 0.78, anchor= NE)

root.mainloop()