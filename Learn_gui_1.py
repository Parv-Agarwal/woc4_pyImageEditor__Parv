from tkinter import *
from PIL import ImageTk, Image

root = Tk()
image1 = ImageTk.PhotoImage(Image.open("scene1.png"))
def click_image():
    label1 = Label(root, image= image1)
    label1.grid(row = 1, column= 0)
    def remove_image():
        global l
        l = label1.grid_remove()
    button3 = Button(root, text = "Remove image", command = remove_image)
    button3.grid(row=0, column=0)
button1 = Button(root, text = "Click to see the image", padx=40, pady=20, command= click_image)
button2 = Button(root, text = "EXIT PROGRAM", padx=40, pady=20, command= root.quit)
button1.grid(row = 0, column=1)
button2.grid(row = 0, column=2)
root.iconbitmap("scene1.png")

root.mainloop()
