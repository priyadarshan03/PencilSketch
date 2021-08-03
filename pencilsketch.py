'''
1]Install python3 first
2]Install pillow - go to cmd and type "pip install Pillow"
3]Install opencv - go to cmd and type "pip install opencv-python"
'''

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2 as cv
from PIL import ImageTk, Image

WIDTH = 640
HEIGHT = 480

slot1 = False
slot2 = False
importedimage = None
importedimagearray = None
pencilsketch = None
pencilsketcharray = None

def resizeImage(inputimage):
    global WIDTH
    global HEIGHT
    return cv.resize(inputimage, (WIDTH, HEIGHT))

def displayInputImageOnWidget(givenimage, widget):
    rgbimage = cv.cvtColor(givenimage, cv.COLOR_BGR2RGB)
    rgbimage = ImageTk.PhotoImage(image = Image.fromarray(rgbimage))
    global importedimagearray
    importedimagearray = rgbimage
    widget.create_image(0,0, anchor="nw", image=rgbimage)

def displayPencilSketchImageOnWidget(givenimage, widget):
    rgbimage = cv.cvtColor(givenimage, cv.COLOR_GRAY2RGB)
    rgbimage = ImageTk.PhotoImage(image = Image.fromarray(rgbimage))
    global pencilsketcharray
    pencilsketcharray = rgbimage
    widget.create_image(0,0, anchor="nw", image=rgbimage)

def loadImageFromSystem(wind):
    wind.withdraw() # hides window
    filepath = filedialog.askopenfilename(initialdir="", title="Select image to import", filetypes=(("All Files", "*.*"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("PNG files", "*.png"), ("BMP files", "*.bmp"), ("TIF files", "*.tif"), ("GIF files", "*.gif"))) # asks user to open a file
    wind.deiconify() # shows window
    if filepath == "": # no file selected
        return None
    newimage = cv.imread(filepath)
    if newimage is None: # selected file failed to open
        throwInvalidImageError()
        return None
    return resizeImage(newimage)

def throwInvalidImageError():
    messagebox.showerror("Error in import image", "File is not a image or image is invalid or file is not accessible.")

def getPencilSketch(inputimage):
    res, _ = cv.pencilSketch(inputimage)
    global pencilsketch
    pencilsketch = res
    return res

def time_to_do_pencil_sketch(givenimage, widget):
    res = getPencilSketch(givenimage)
    displayPencilSketchImageOnWidget(res, widget)

def loadImageAndDisplay(widget1, widget2, wind):
    ret = loadImageFromSystem(wind)
    if ret is not None:
        global importedimage
        global slot1
        global slot2
        importedimage = ret
        displayInputImageOnWidget(ret, widget1)
        slot1 = True
        slot2 = False
        time_to_do_pencil_sketch(ret, widget2)
        slot2 = True

def save_pencil_sketch(wind):
    global slot1
    global slot2
    if slot1 is False or slot2 is False:
        return
    wind.withdraw()
    filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("PNG files", "*.png"), ("BMP files", "*.bmp"), ("TIF files", "*.tif")])
    wind.deiconify()
    if filename != "":
        global pencilsketch
        global WIDTH
        global HEIGHT
        saveimage = cv.resize(pencilsketch, (WIDTH, HEIGHT), interpolation = cv.INTER_LANCZOS4)
        cv.imwrite(filename, saveimage)

window = Tk()
window.title("Pencil Sketch Maker")
window.geometry("1300x520+100+100")
frame = Frame(window)
frame.pack(fill=BOTH, expand=1)
imageslot1 = Canvas(frame, bg="gray", width=WIDTH, height=HEIGHT)
imageslot1.grid(row=0, column=0)
imageslot2 = Canvas(frame, bg="gray", width=WIDTH, height=HEIGHT)
imageslot2.grid(row=0, column=1)
button1 = Button(frame, bd="5", text="Import image", command=lambda:loadImageAndDisplay(imageslot1, imageslot2, window))
button1.grid(row=1, column=0)
button2 = Button(frame, bd="5", text="Save image", command=lambda:save_pencil_sketch(window))
button2.grid(row=1, column=1)
window.mainloop()
