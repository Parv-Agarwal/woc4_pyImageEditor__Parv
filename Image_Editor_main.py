from ctypes import resize
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

root = Tk()
root.geometry("1200x700")
root.title("IMAGE EDITOR")

image_frame = LabelFrame(root, padx = 20, pady = 20)        # frame where image is placed
image_frame.place(relx = 0.3, rely = 0.5, anchor= CENTER)
image1 = Image.open("Images/scene1.png")
default_image = ImageTk.PhotoImage(image1.resize((500,450)))
image_show = Label(image_frame, image = default_image)
image_show.pack()

def new_image():           # function for new image button 
    global image1 
    global image2
    global image_show
    image_show.pack_forget()
    filename = filedialog.askopenfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Select an image", filetypes=(("png images", "*.png"), ("jpg images", "*.jpg")))
    image1 = Image.open(filename)
    image2 = ImageTk.PhotoImage(image1.resize((500, 450)))
    image_show = Label(image_frame, image = image2)
    image_show.pack()

def save_image():    # function to save images
    global image1 
    savefile = filedialog.asksaveasfilename(initialdir= "/woc4_pyImageEditor_Parv/Images", title = "Save Image", filetypes=(("png image", "*.png"), ("jpg image", "*.jpg")), defaultextension=(".png"))
    image1.save(savefile)
    

new_file_button = Button(root, text = "New Image", command= new_image)
save_file_button = Button(root, text = "Save", command= save_image)
new_file_button.grid(row=0,column=0)
save_file_button.grid(row = 0, column =1)

root.mainloop()