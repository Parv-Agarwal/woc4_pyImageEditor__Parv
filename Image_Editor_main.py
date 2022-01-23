from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from math import floor

root = Tk()
root.geometry("1200x700")
root.title("IMAGE EDITOR")

#Frames defined
image_frame = LabelFrame(root, padx = 20, pady = 20)        # frame where image is placed
image_frame.place(relx = 0.3, rely = 0.5, anchor= CENTER)
colour_change_frame = LabelFrame(root, text = "COLOUR MANIPULATION", padx = 20, pady = 20)
colour_change_frame.place(relx = 0.85, rely = 0.4, anchor = NE)

image1 = Image.open("Images/scene1.png")
ims = image1.resize((500,450))
default_image = ImageTk.PhotoImage(image1.resize((500,450)))
image_show = Label(image_frame, image = default_image)
image_show.pack()

def new_image():           # function for new image button 
    global image1 
    global image2
    global image_show
    global ims
    image_show.pack_forget()
    filename = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select an image", filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    image1 = Image.open(filename)
    ims = image1.resize((500,450))
    image2 = ImageTk.PhotoImage(image1.resize((500, 450)))
    image_show = Label(image_frame, image = image2)
    image_show.pack()

def save_image():    # function to save images
    global image1 
    savefile = filedialog.asksaveasfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Save Image", filetypes=(("png image", "*.png"), ("jpg image", "*.jpg")), defaultextension=(".png"))
    ims.save(savefile)
    
def flip_vert():      # function for flip vertical
    global ims
    global image_show
    global image2
    image_show.pack_forget()

    # algorithm for flip vertical:
    for x in range(1, 500):
        for y in range(1,225):
            global p_shift
            pixel_access = ims.load()
            p_shift =  pixel_access[x, y]
            pixel_access[x, y] = pixel_access[x, 450 - y]
            pixel_access[x, 450 - y] = p_shift

    image2 = ImageTk.PhotoImage(ims)
    image_show = Label(image_frame, image = image2)
    image_show.pack()

def flip_horiz():      # function for flip horizontal
    global ims
    global image_show
    global image2
    image_show.pack_forget()
    
    # algorithm for flip horizontal:
    for x in range(1, 250):
        for y in range(1, 450):
            global p_shift
            pixel_access = ims.load()
            p_shift =  pixel_access[x, y]
            pixel_access[x, y] = pixel_access[500 - x, y]
            pixel_access[500 - x, y] = p_shift

    image2 = ImageTk.PhotoImage(ims)
    image_show = Label(image_frame, image = image2)
    image_show.pack()

def inv_img():      # function for invert image
    global ims
    global image_show
    global image2
    image_show.pack_forget()
    
    # algorithm to invert colours:
    for x in range(1, 500):
        for y in range(1, 450):
            global inv_p
            pixel_access = ims.load()
            inv_p = (255 - floor(pixel_access[x,y][0]), 255 - floor(pixel_access[x,y][1]), 255 -  floor(pixel_access[x,y][2]))
            pixel_access[x,y] = inv_p 

    image2 = ImageTk.PhotoImage(ims)
    image_show = Label(image_frame, image = image2)
    image_show.pack()

# BUTTONS DEFINAITION
new_file_button = Button(root, text = "New Image", command= new_image)
save_file_button = Button(root, text = "Save", command= save_image)
flip_vert_button = Button(root, text = "FLIP VERTICAL", command = flip_vert, padx = 50, pady = 20)
flip_horiz_button = Button(root, text = "FLIP HORIZONTAL", command = flip_horiz, padx = 50, pady = 20)
inv_img_button = Button(colour_change_frame, text = "INVERT IMAGE", command = inv_img, padx = 50, pady = 20)


# BUTTONS EXECUTION
new_file_button.grid(row=0,column=0)
save_file_button.grid(row = 0, column =1)
flip_vert_button.place(relx = 0.75, rely = 0.2, anchor= NE)
flip_horiz_button.place(relx = 0.95, rely = 0.2, anchor= NE)
inv_img_button.pack()   

root.mainloop()