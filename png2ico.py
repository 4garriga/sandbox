"""Convert png file to icon."""
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# launch dialog
root = tk.Tk()
root.withdraw()  # hide window
filename = filedialog.askopenfilename()

# convert
saveas = filename.split('.')[0]
img = Image.open(filename)
img.save(f'{saveas}.ico', sizes=[(32, 32)])