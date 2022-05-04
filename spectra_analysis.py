# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:27:39 2022

@author: tomasetti
"""

import numpy as np
import pandas as pd
import PIL.Image  
from PIL import ImageTk, Image                                                              # Avoid namespace issues
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.animation as animation
from matplotlib import style


# Import some tkinter things for GUI stuff
import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import Button, Entry, Label, Checkbutton, Scale, Spinbox, LabelFrame
from tkinter import Frame, CENTER, END, LEFT, W
from tkinter import filedialog
from tkinter import messagebox

style.use("ggplot")

    

# Define the GUI class
class GUI_spectra:
    def __init__(self, parent):
        self.myParent = parent
        self.containerLoad    = LabelFrame(parent,text = "Calibration of mass spectra", bg="white", fg="red", font='25')            # Create LOAD container

        # Place containers
        self.containerLoad.place(relwidth=0.95,relheight=0.95, relx=0.025, rely=0.025)                                          # Place the LOAD container
        
        # Frames in load container
        
        self.frame1 = LabelFrame(self.containerLoad,text = "1) Load the datas", bg="white", fg="black", font='15')
        self.frame2 = LabelFrame(self.containerLoad,text = "2) Result ", bg="white", fg="black", font='15')
        
        # Place Frames in load container
        self.frame1.place(relwidth=0.5,relheight=0.90, relx=0.02, rely=0.05)
        self.frame2.place(relwidth=0.43,relheight=0.90, relx=0.55, rely=0.05)
        
        # Place subFrames in frame1
        self.subframe1 = LabelFrame(self.frame1,text = "", bg="white", fg="black", font='15')
        self.subframe1.place(relwidth=0.90,relheight=0.75, relx=0.05, rely=0.20)
        
        # Place subFrames in frame2
        self.subframe2 = LabelFrame(self.frame2,text = "", bg="white", fg="black", font='15')
        self.subframe2.place(relwidth=0.90,relheight=0.75, relx=0.05, rely=0.20)
        
        # Instance variables
        self.time                  = None
        self.volt                  = None
        self.time_refs             = None
        self.mass_refs             = None
        self.coeffs_fit_poly = None
        self.residuel_fit = None
        self.Time_column = None
        self.Time_row = None
        self.Volt_column = None
        self.Volt_row = None
        self.chksonic           = tk.IntVar()                                    # Checkbox for sonic nozzle
        self.chkconical         = tk.IntVar()                                    # Checkbox for conical nozzle
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- W I D G E T S ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # // == // ============= \\ == \\
        # // == // == L O A D == \\ == \\
        # // == // ============= \\ == \\
        
        # ===== frame1 =====
        
        self.buttonload = Button(self.frame1)
        self.buttonload.configure(text="Load spectrum",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Load_values)
        self.Edit_time_column = Entry(self.frame1, width= 8)
        self.Edit_time_column.insert(END, 0)
        self.Edit_time_row = Entry(self.frame1, width= 8)
        self.Edit_time_row.insert(END, 20)
        self.Edit_volt_column = Entry(self.frame1, width= 8)
        self.Edit_volt_column.insert(END, 1)
        self.Edit_volt_row = Entry(self.frame1, width= 8)
        self.Edit_volt_row.insert(END, 20)
        
        self.Label_time_column= Label(self.frame1,text="Time column",bg = "grey", fg="white")
        self.Label_time_row= Label(self.frame1,text="Time row",bg = "grey", fg="white")
        self.Label_volt_column= Label(self.frame1,text="Volt colum",bg = "grey", fg="white")
        self.Label_volt_row= Label(self.frame1,text="Volt row",bg = "grey", fg="white")
        
        
        # ===== frame2 =====
        
        self.Label_mass_ref = Label(self.frame2,text="Mass reference (amu)",bg = "Steel Blue",fg = "White")
        self.Label_time_ref = Label(self.frame2,text="Time reference (µs)",bg = "Steel Blue",fg = "White")
        
        self.Label_mass1 = Label(self.frame2,text="Mass 1",bg = "grey", fg="white")
        self.Label_mass2 = Label(self.frame2,text="Mass 2",bg = "grey", fg="white")
        self.Label_mass3 = Label(self.frame2,text="Mass 3",bg = "grey", fg="white")
        self.Label_mass4 = Label(self.frame2,text="Mass 4",bg = "grey", fg="white")
        
        self.Edit_mass1 = Entry(self.frame2)
        self.Edit_mass1.insert(END, 40)
        self.Edit_mass2 = Entry(self.frame2)
        self.Edit_mass2.insert(END, 120)
        self.Edit_mass3 = Entry(self.frame2)
        self.Edit_mass3.insert(END, 160)
        self.Edit_mass4 = Entry(self.frame2)
        self.Edit_mass4.insert(END, 360)
        
        self.Edit_time1 = Entry(self.frame2)
        self.Edit_time1.insert(END, 20.3)
        self.Edit_time2 = Entry(self.frame2)
        self.Edit_time2.insert(END, 34.9)
        self.Edit_time3 = Entry(self.frame2)
        self.Edit_time3.insert(END, 40.3)
        self.Edit_time4 = Entry(self.frame2)
        self.Edit_time4.insert(END, 60.4)
        
        self.Label_space1 = Label(self.frame2,text="",bg = "white", fg="white")
        
        self.buttonplot = Button(self.frame2)
        self.buttonplot.configure(text="Calibrate and plot",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Calibrate)
        self.buttonsave = Button(self.frame2)
        self.buttonsave.configure(text="Save calibration",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Save_calib)
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # ----------------------------- L A Y O U T ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # LOAD (frame1)
        self.buttonload.grid(column = 0, row = 0,sticky = "EW")
        self.Edit_time_column.grid(column = 1, row = 2,sticky = "EW")
        self.Edit_time_row.grid(column = 1, row = 3,sticky = "EW")
        self.Edit_volt_column.grid(column = 1, row = 4,sticky = "EW")
        self.Edit_volt_row.grid(column = 1, row = 5,sticky = "EW")
        
        self.Label_time_column.grid(column = 0, row = 2,sticky = "EW")
        self.Label_time_row.grid(column = 0, row = 3,sticky = "EW")
        self.Label_volt_column.grid(column = 0, row = 4,sticky = "EW")
        self.Label_volt_row.grid(column = 0, row = 5,sticky = "EW")
        
        # Calibration (frame1)
        self.Label_mass_ref.grid(column = 1, row = 0,sticky = "EW")
        self.Label_time_ref.grid(column = 2, row = 0,sticky = "EW")
        
        self.Label_mass1.grid(column = 0, row = 1,sticky = "EW")
        self.Label_mass2.grid(column = 0, row = 2,sticky = "EW")
        self.Label_mass3.grid(column = 0, row = 3,sticky = "EW")
        self.Label_mass4.grid(column = 0, row = 4,sticky = "EW")
        
        self.Edit_mass1.grid(column = 1, row = 1,sticky = "EW")
        self.Edit_mass2.grid(column = 1, row = 2,sticky = "EW")
        self.Edit_mass3.grid(column = 1, row = 3,sticky = "EW")
        self.Edit_mass4.grid(column = 1, row = 4,sticky = "EW")
        
        self.Edit_time1.grid(column = 2, row = 1,sticky = "EW")
        self.Edit_time2.grid(column = 2, row = 2,sticky = "EW")
        self.Edit_time3.grid(column = 2, row = 3,sticky = "EW")
        self.Edit_time4.grid(column = 2, row = 4,sticky = "EW")
        
        self.Label_space1.grid(column = 3, row = 0,sticky = "EW")
        
        self.buttonplot.grid(column = 4, row = 0,sticky = "EW")
        self.buttonsave.grid(column = 4, row = 1,sticky = "EW")
        
        
        
    def Load_values(self):
        
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/measurements/Stargate_spectra",
                                       title = "Select signal folder",
                                       filetypes = (("Excel", "*.xlsx"),
                                                    ("JPG Files", "*.jpg"),
                                                    ("PNG Files", "*.png"),
                                                    ("BMP Files", "*.bmp")))


        df = pd.read_excel(file_path)  
        arr = df.to_numpy()


        
        self.Time_column = int(self.Edit_time_column.get())
        self.Time_row = int(self.Edit_time_row.get())
        self.Volt_column = int(self.Edit_volt_column.get())
        self.Volt_row = int(self.Edit_volt_row.get())
        
        
        self.time, self.volt = arr[self.Time_row:, self.Time_column], arr[self.Volt_row:, self.Volt_column]
        self.time *= 1e6
        self.volt *= -1e3
        fig = plt.figure(figsize=(6.5, 4.5), dpi=90)
        fig.add_subplot(111).plot(self.time,self.volt,'r', linewidth=0.5)
        plt.xlabel('time (µs)')
        plt.ylabel('volt (mV)')

        canvas = FigureCanvasTkAgg(fig, self.subframe1)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        frame = Frame(self.subframe1)
        frame.grid(row=0, column=0)
        toobar = NavigationToolbar2Tk(canvas, frame)
        canvas.get_tk_widget().grid(row=1, column=0)
        
        
    def Calibrate(self):
        
        self.mass_refs = [float(self.Edit_mass1.get()),float(self.Edit_mass2.get()),float(self.Edit_mass3.get()),float(self.Edit_mass4.get())]
        self.time_refs = [float(self.Edit_time1.get()),float(self.Edit_time2.get()),float(self.Edit_time3.get()),float(self.Edit_time4.get())]
        
        
        data = np.zeros(shape=(len(self.time),2), dtype=float)
        data[:,0] = self.time
        data[:,1] = self.volt
        
        data = data[np.where(data[:,0]>0)[0],:]
        
        self.coeffs_fit_poly,self.residuel_fit = np.polyfit(self.time_refs,self.mass_refs,2, cov =True)
        print("Coeffecient fit 2nd degres :\n",self.coeffs_fit_poly)
        print("Covariance matrice :\n",self.residuel_fit)

        data_conv = self.coeffs_fit_poly[0]*data[:,0]**2+self.coeffs_fit_poly[1]*data[:,0] +self.coeffs_fit_poly[2]
        

        fig = plt.figure(figsize=(6.5, 4.5), dpi=90)
        fig.add_subplot(111).plot(data_conv,data[:,1],'r', linewidth = 0.5)
        plt.xlabel('mass (m/z)')
        plt.ylabel('volt (mV)')

        canvas = FigureCanvasTkAgg(fig, self.subframe2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        frame2 = Frame(self.subframe2)
        frame2.grid(row=0, column=0)
        toobar = NavigationToolbar2Tk(canvas, frame2)
        canvas.get_tk_widget().grid(row=1, column=0)
        
    def Save_calib(self):
        
        
        file = filedialog.asksaveasfile(initialdir = "C:/Users/tomasetti/Documents/measurements/Stargate_spectra",
                                       title = "Select signal folder",
                                       filetypes = (("Text file", "*.txt"),
                                                    ("Excel", "*.xlsx")))
        

        file.write("\nTemps références : "+str(self.time_refs))
        file.write("\nMasse attribution: "+str(self.mass_refs))
        file.write("\nCoefficient poly 2nd degre : "+str(self.coeffs_fit_poly))
        file.write("\nCovariance matrice :\n"+str(self.residuel_fit))
        
        
        
        
        


root = Tk()
root.wm_title("Mass spectra calibration")                                        # Set window title
#root.iconbitmap("icon.ico")                                                     # Set icon bitmap
root.geometry("1500x800")
#root.configure(bg="#263D42")
gui_spectra = GUI_spectra(root)                                                   # Instantiate the class GUI_BOS
root.mainloop()
