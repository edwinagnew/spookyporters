import tkinter as tk
from tkinter import messagebox
from tkinter import *


class popUpWindow:
    def  __init__(self,title,string):
        self.title = title
        self.string =string
        Tk().wm_withdraw()
        messagebox.showinfo(title,string)




#popUpWindow('Hint', 'This is the hint message')