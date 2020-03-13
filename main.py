#!/usr/bin/env python2
# -*- coding:utf-8 -*-

# --------------------------
# Author: Louis Huang
# Code on Jan. 20th, 2017
# UI of Handwritten digtial recognition system
# --------------------------

from tkinter import *
import tkinter.filedialog as td
import tkinter.messagebox as tb
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import sys
import random
import time
from datetime import timedelta
from PIL import Image, ImageTk, ImageDraw
import input_data
from use_model import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Recon(object):
    def __init__(self):
        # ----- Initialize  the window ----------------------------
        self.root = Tk()
        self.numberrec = ttk.LabelFrame(self.root, text='Recognizer')
        self.train = ttk.LabelFrame(self.root, text='Console')

        # ----- define the transferable variables-----------------
        self.imagepath = StringVar(self.root)
        self.inputreadom = StringVar(self.root)
        self.message = StringVar(self.root)
        self.number = StringVar(self.root)
        self.im_nparr = 0
        # ---- Initilaize the widgets -----------------------------
        # ------Menu--------------------
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label='OpenFile', command=self.openfile)

        self.plott = Menu(self.menubar, tearoff=0)

        self.menubar.add_command(label='Quit', command=sys.exit)

        # ------------Recognize LabelFrame----------------
        self.pathlab = Label(self.numberrec, text="the image path:")
        self.pathentry = Entry(self.numberrec, state="readonly", width=35,textvariable=self.imagepath)
        self.recbutton = Button(self.numberrec, width=8, height=1, text="Recognize",
                                state='disable', command=self.recobut)
        self.piccan = Canvas(self.numberrec,
                             width=168, height=168, bg='#f2f2f2')
        self.reshbutton = Button(self.numberrec, text='Reshape', state='disable',command=self.reshapepicc)
        self.graybutton = Button(self.numberrec, text='Graying', state='disable',command=self.gray)
        self.normalizebutton = Button(self.numberrec, text='Normalize', state='disable',command=self.normalize)
        self.resultlab = Label(self.numberrec, width=10, text="The result is:")
        self.resultnum = Entry(self.numberrec, width=9, state="readonly", textvariable=self.number)
        # ------------- console LabelFrame---------------------------
        self.trainmsg = ScrolledText(self.train,font=("Microsoft YaHei",10),width=30,height=13,padx=5,pady=5)
        self.printt("Welcome to NRzer")
        self.printt("-------------------------------")
        # ------- visualize the widgets ----------------------------
        self.root['menu']=self.menubar

        self.numberrec.grid(row=0,column=6,padx=5,pady=5)
        self.train.grid(row=0,column=7,padx=5,pady=5)

        self.pathlab.grid(row=0, column=0)
        self.pathentry.grid(row=1, column=0, padx=5, pady=5)
        self.recbutton.grid(row=1, column=1, padx=5, pady=5)

        self.piccan.grid(row=2, column=0, rowspan=3)
        self.reshbutton.grid(row=2, column=1)
        self.graybutton.grid(row=3, column=1)
        self.normalizebutton.grid(row=4, column=1,padx=5)
        self.resultlab.grid(row=5,column=0)
        self.resultnum.grid(row=5,column=1,padx=5,pady=5)

        self.trainmsg.grid(column=0,row=0,padx=5,pady=5)

    # -----  Function to print in the 'Console'------------------------------
    def printt(self, msg):
        self.message.set(msg+"\n")
        self.trainmsg.insert(INSERT, self.message.get())
        self.trainmsg.see(END)

    # ------ Menu function --------------------------------------
    def openfile(self):
        try:
            fname = td.askopenfilename(title="open", filetypes=[('Image','*.png'),('Image','*.bmp'), ('All Files', '*')])
            self.imagepath.set(fname)
            self.showimage()
            del(self.im_nparr)
            self.reshbutton['state']='normal'
        except AttributeError:
            tb.showwarning('Warining', "You haven't import any images!")
        except IOError:
            tb.showwarning('Warining', "You should import an image!")
    # ------- function to show image ------------------------------
    def showimage(self):
        self.__img = Image.open(self.imagepath.get())
        self.__photo = ImageTk.PhotoImage(self.__img)
        self.piccan.create_image((84, 84), image=self.__photo)
        #self.recbutton['state']='normal'


    # ------------ Recognizer button----------------------------
    def reshapepicc(self):
        self.piccan.delete("all")
        pic = self.imagepath.get()
        self.repic = reshapepic(pic)
        self.repicimg = ImageTk.PhotoImage(self.repic)
        self.piccan.create_image((84,84), image=self.repicimg)
        self.graybutton['state']='normal'
    def gray(self):
        self.piccan.delete("all")
        pic = self.repic
        self.graypp = graypic(pic)
        self.grayimg = ImageTk.PhotoImage(self.graypp)
        self.piccan.create_image((84,84), image=self.grayimg)
        self.normalizebutton['state']='normal'
    def normalize(self):
        pic = self.graypp
        self.im_nparr,self.finalpic = normalizepic(pic)
        self.recbutton['state']='normal'
    def recobut(self):
        try:
            self.start_time = time.time()
            self.recresult = str(rec(self.im_nparr))
            self.end_time = time.time()
            self.number.set("        "+self.recresult)
            self.printt("The recognition result is:"+self.recresult)
            self.time_dif = self.end_time-self.start_time
            self.printt("Time usage:"+str(timedelta(seconds=int(round(self.time_dif)))))
        except:
            tb.showwarning('Warining', "You should preprocess the image frist!")
# ------- function to mainkoop ---------------------------------
    def runloop(self):
        self.root.title("NRzer")
        self.root.geometry('650x300+150+30')
        self.root.resizable(False, False)
        self.root.iconbitmap("./bitmap/timg.ico")
        self.root.mainloop()

if __name__ == "__main__":
    window = Recon()
    window.runloop()
