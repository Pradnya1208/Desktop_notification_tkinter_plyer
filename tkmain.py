#from ttkthemes import ThemedStyle
import tkinter as tk
import ttk
#import PySimpleGUI as sg
#from ttkthemes import themed_tk
import os
import subprocess
import platform
from tkinter import Tk, ttk, Toplevel
from PIL import ImageTk, ImageDraw
import PIL.Image
from tkinter import *
import sys
from bs4 import BeautifulSoup
import requests
import plyer
import time
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')

from Indian_states import state_name
from nameCorrection import name_correction
from states_data import merged
from city_data import notify_app_city_data

import covid_data

LARGE_FONT = ("verdana", 12)
FRAME1_FONT = ("verdana", 12, "bold")

FRAME0_FONT = ("Helvetica",20, "bold") #Courier New
FRAME1 = ("verdana", 15, "bold")
FRAME1_1 = ("verdana", 16)
NOTIFY_F = ("Helvetica", 8, "bold")

WIDTH = 400
HEIGHT = 380
IMAGE_PATH = 'images//c_t.png'
ICON_PATH = 'images//ico.png'
ICON = 'images//ico.ico'
WORLD_IMG = 'images//banner.png'
MENU_IMAGE = 'images//menu.png'



class CovidApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.create_window(WIDTH, HEIGHT, tk.Tk)

        self.create_menuBar()


        # set the frame width and height
        container = tk.Frame(self, width=WIDTH, height=HEIGHT)
        container.grid_propagate(False)
        container.pack()
        container.grid_rowconfigure(0, weight=0)
        container.grid_columnconfigure(0, weight=0)

 

        # dictionary of frames
        self.frames = {}

        for F in (TT, WorldData, Andaman_and_Nikobar_Islands, Andhra_Pradesh, Arunachal_Pradesh, 
                  Assam, Bihar, Chandigarh, Chhattisgarh, Delhi, 
                  Dadra_and_Nagar_Haveli_and_Daman_and_Diu, Goa, Gujarat, Himachal_Pradesh, 
                  Haryana, Jharkhand, Jammu_and_Kashmir, Karnataka, Kerala, Ladakh, 
                  Maharashtra, Meghalaya, Manipur, Madhya_Pradesh, Mizoram, Nagaland, 
                  Odisha, Punjab, Puducherry, Rajasthan, Sikkim, Telangana, Tamil_Nadu,
                  Tripura, Uttar_Pradesh, Uttarakhand, West_Bengal):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TT)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
 

    def create_window(self, w, h, root):
        global close_button
        ws = root.winfo_screenwidth(self)
        hs = root.winfo_screenheight(self)
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry(self, '%dx%d+%d+%d' % (w, h, x, y))
        root.attributes(self, "-topmost", True)
        #root.title(self, "COVID19 DATA TRACKER")
        icon = PhotoImage(file=ICON_PATH)
        root.iconphoto(self, False, icon)
        root.wm_overrideredirect(self,TRUE)
        # set new geometry
        back_ground = "#2c2c2c"
        # set background of window
        content_color = "#ffffff"
        # make a frame for the title bar
        title_bar = Frame(self, bg=back_ground, relief='raised', bd=0,
                          highlightcolor=back_ground, highlightthickness=0)

        def minimizeWindow():
            self.withdraw()
            self.overrideredirect(False)
            self.iconify()


        minimize_button = Button(title_bar, text='-', command=minimizeWindow,
                                 bg=back_ground, padx=5, pady=0,
                                 activebackground="red", bd=0, font="bold", fg='white', activeforeground="white",
                                 highlightthickness=0
                                 )
        # put a close button on the title bar
        close_button = Button(title_bar, text='x', command=self.destroy, bg=back_ground, padx=5, pady=0,
                              activebackground="red", bd=0, font="bold", fg='white', activeforeground="white",
                              highlightthickness=0)

        # add icon button
        icon_img = PIL.Image.open(ICON_PATH)
        render = ImageTk.PhotoImage(icon_img)
        img = Label(title_bar, image=render)
        img.image = render

        # window title
        title_window = "COVID19 DATA TRACKER"
        title_name = Label(title_bar, text=title_window, bg=back_ground, fg="white")
        # pack the widgets
        title_bar.pack(expand=1, fill=X)
        img.pack(side=LEFT)
        title_name.pack(side=LEFT)
        close_button.pack(side=RIGHT)
        minimize_button.pack(side=RIGHT)


        x_axis = None
        y_axis = None

        def move_window(event):
            self.geometry(f"+{event.x_root}+{event.y_root}")

        def change_on_hovering(event):
            close_button['bg'] = 'red'

        def min_hover(event):
            minimize_button['bg'] = 'red'

        def return_to_normal_state(event):
            close_button['bg'] = back_ground

        def min_to_normal_state(event):
            minimize_button['bg'] = back_ground


        def check_map(event):  # apply override on deiconify.
            if str(event) == "<Map event>":
                self.overrideredirect(1)


        title_bar.bind('<B1-Motion>', move_window)
        close_button.bind('<Enter>', change_on_hovering)
        close_button.bind('<Leave>', return_to_normal_state)
        minimize_button.bind('<Enter>', min_hover)
        minimize_button.bind('<Leave>', min_to_normal_state)
        self.bind('<Map>', check_map)  # added bindings to pass windows status to function
        self.bind('<Unmap>', check_map)

    def create_menuBar(self):
        back = "#2c2c2c"
        # set the default option
        st_ =[]
        for state in state_name:   
            if not "TT" in state:
                st_ .append(name_correction(state))
            
        state_options = StringVar()
        state_optionsList =st_
        state_options.set("Select State")

            
        country = StringVar()
        country_list = ["Cases Worldover"] #TODO: CSV to DF worldcsv
        country.set('Options')
     

        
        def stateOptionMenu(opt):
         
            self.show_frame(eval(state_options.get().replace(' ','_')))
            state_options.set("Select State")
      
        def countryMenu(opt):
            if "Cases Worldover" in country.get():
                self.show_frame(WorldData)
            country.set('Options')
            
                
        def homeMenu():
            self.show_frame(TT)
        
        def changeHM_on_hover(event):
            homeMenu['bg'] = 'red'

        def returnHM_to_normal(event):
            homeMenu['bg'] = "black"

        menuBar = Frame(self, bg=back, relief='raised', bd=0,
                          highlightcolor=back, highlightthickness=0)
        stateOptionsMenu = OptionMenu(menuBar, state_options, *state_optionsList, command =stateOptionMenu)
        stateOptionsMenu.configure(bg = "black", fg = "White")
        
       
        countryMenu = OptionMenu(menuBar, country, *country_list, command=countryMenu)
        countryMenu.configure(bg="black", fg="White")
        
        homeMenu = Button(menuBar, text = "Home", command = homeMenu)
        homeMenu.configure(bg="black", fg="White")
        
       
        homeMenu.bind('<Enter>', changeHM_on_hover)
        homeMenu.bind('<Leave>', returnHM_to_normal)

        menuBar.pack(expand=1, fill=X)

        
        stateOptionsMenu.pack(side=LEFT)
        countryMenu.pack(side=LEFT)
        homeMenu.pack(ipadx = 4, ipady = 4,side = RIGHT)
       
        

class WorldData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        self.setWidget(background,controller)
        self.worldData(background)
        self.bannerName(background)
        #self.detailed_info(background, controller)
 
    
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)


    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=15, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - WORLD ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)
        

    def worldData(self, frame1_back):
        frame_1 = LabelFrame(frame1_back, text = "Covid19 Cases Worldover", font = FRAME1_FONT, padx=5, pady=10, bg= 'Black', fg ="Red")
        frame_1.place(x=50, y=150)

        f1_label = Label(frame_1, text=covid_data.covid.covid_d,
                         font = FRAME1_1, fg="White", bg = "black", padx = 10, pady = 10, justify = LEFT)
        f1_label.pack(side=LEFT)

  

class TT(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        self.setWidget(background,controller)
        self.IndiaData(background)
        self.bannerName(background)
     
 
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)


    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def IndiaData(self, frame1_back):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "India" in m:
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
        
        frame_1 = LabelFrame(frame1_back, text = "Covid19 Cases in India", font = FRAME1_FONT, padx=5, pady=10, bg= 'Black', fg ="Red")
        frame_1.place(x=60, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", padx = 10, pady = 10, justify = LEFT)
        f1_label.pack(side=LEFT)
        
    

class Maharashtra(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

     
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Maharashtra" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else:  
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Maharashtra" in m:
                        #print(CC, RC, DC)
                          frame_notify = "Maharashtra => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
        
                var.set("Enable Notifications")
                
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Maharashtra",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
        
                self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.MHData(background, frame_text)
        self.bannerName(background)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
      
        m.add_command(label = 'Ahmednagar', command = lambda:self.notify_func("Ahmednagar", "Maharashtra"))
        m.add_command(label = 'Akola', command = lambda:self.notify_func("Akola", "Maharashtra"))
        m.add_command(label = 'Amravati', command = lambda:self.notify_func("Amravati", "Maharashtra"))
        m.add_command(label = 'Aurangabad', command = lambda:self.notify_func("Aurangabad", "Maharashtra"))
        m.add_command(label = 'Beed', command = lambda:self.notify_func("Beed", "Maharashtra"))
        m.add_command(label = 'Bhandara', command = lambda:self.notify_func("Bhandara", "Maharashtra"))
        m.add_command(label = 'Buldhana', command = lambda:self.notify_func("Buldhana", "Maharashtra"))
        m.add_command(label = 'Chandrapur', command = lambda:self.notify_func("Chandrapur", "Maharashtra"))
        m.add_command(label = 'Dhule', command = lambda:self.notify_func("Dhule", "Maharashtra"))
        m.add_command(label = 'Gadchiroli', command = lambda:self.notify_func("Gadchiroli", "Maharashtra"))
        m.add_command(label = 'Gondia', command = lambda:self.notify_func("Gondia", "Maharashtra"))
        m.add_command(label = 'Hingoli', command = lambda:self.notify_func("Hingoli", "Maharashtra"))
        m.add_command(label = 'Jalgaon', command = lambda:self.notify_func("Jalgaon", "Maharashtra"))
        m.add_command(label = 'Jalna', command = lambda:self.notify_func("Jalna", "Maharashtra"))
        m.add_command(label = 'Kolhapur', command = lambda:self.notify_func("Kolhapur", "Maharashtra"))
        m.add_command(label = 'Latur', command = lambda:self.notify_func("Latur", "Maharashtra"))
        m.add_command(label = 'Mumbai', command = lambda:self.notify_func("Mumbai", "Maharashtra"))
        m.add_command(label = 'Nagpur', command = lambda:self.notify_func("Nagpur", "Maharashtra"))
        m.add_command(label = 'Nanded', command = lambda:self.notify_func("Nanded", "Maharashtra"))
        m.add_command(label = 'Nandurbar', command = lambda:self.notify_func("Latur", "Maharashtra"))
        m.add_command(label = 'Latur', command = lambda:self.notify_func("Latur", "Maharashtra"))
        m.add_command(label = 'Nashik', command = lambda:self.notify_func("Nashik", "Maharashtra"))
        m.add_command(label = 'Osmanabad', command = lambda:self.notify_func("Osmanabad", "Maharashtra"))
        m.add_command(label = 'Palghar', command = lambda:self.notify_func("Palghar", "Maharashtra"))
        m.add_command(label = 'Pune', command = lambda:self.notify_func("Pune", "Maharashtra"))
        m.add_command(label = 'Raigad', command = lambda:self.notify_func("Raigad", "Maharashtra"))
        m.add_command(label = 'Ratnagiri', command = lambda:self.notify_func("Ratnagiri", "Maharashtra"))
        m.add_command(label = 'Sangli', command = lambda:self.notify_func("Sangli", "Maharashtra"))
        m.add_command(label = 'Satara', command = lambda:self.notify_func("Satara", "Maharashtra"))
        m.add_command(label = 'Sindhudurg', command = lambda:self.notify_func("Sindhudurg", "Maharashtra"))
        m.add_command(label = 'Thane', command = lambda:self.notify_func("Thane", "Maharashtra"))
        m.add_command(label = 'Wardha', command = lambda:self.notify_func("Wardha", "Maharashtra"))
        m.add_command(label = 'Washim', command = lambda:self.notify_func("Washim", "Maharashtra"))
        m.add_command(label = 'Yavatmal', command = lambda:self.notify_func("Yavatmal", "Maharashtra"))
        

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Maharashtra" in m:
                        #print(CC, RC, DC)
                          frame_notify_ = "Maharashtra => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + "| Total Deaths : " + f'{DC_:n}' +  "| Recovered : " + f'{RC_:n}' 
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")  
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def MHData(self, frame1_back, frame_text):
        
        
        frame_1 = LabelFrame(frame1_back, text = "Maharashtra", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
     
       
class Andaman_and_Nikobar_Islands(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

     
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Andaman and Nikobar Islands" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
             
            for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                if "Andaman and Nikobar Islands" in m:
                    #print(CC, RC, DC)
                      frame_notify = "Andaman and Nikobar Islands => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
            messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
            var.set("Enable Notifications")
            
            # calling plyer Notification
            while True:
                plyer.notification.notify( title = "Covid19 cases of Andaman and Nikobar Islands",
                                          message = frame_notify, app_icon = ICON,timeout = 20)
                time.sleep(self.t1)
    
            self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.ANData(background, frame_text)
        self.bannerName(background)
      
  
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Andaman and Nikobar Islands" in m:
                        #print(CC, RC, DC)
                          frame_notify_ = "Andaman and Nikobar Islands => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + "| Total Deaths : " + f'{DC_:n}' +  "| Recovered : " + f'{RC_:n}' 
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def ANData(self, frame1_back, frame_text):
        
        
        frame_1 = LabelFrame(frame1_back, text = "Andaman and Nikobar", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
  
                
class Andhra_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Andhra Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else:  
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Andhra Pradesh" in m:
                        #print(CC, RC, DC)
                          frame_notify = "Andhra Pradesh => | Total : " + f'{CC:n}'  + " | Deaths : "  + f'{DC:n}'  + " | Recovered : " + f'{RC:n}' 
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
        
                var.set("Enable Notifications")
                
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Andhra Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
        
                self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.APData(background, frame_text)
        self.bannerName(background)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
        m.add_command(label = 'Anantapur', command = lambda:self.notify_func("Anantapur", "Andhra_Pradesh"))
        m.add_command(label = 'Chittoor', command = lambda:self.notify_func("Chittoor", "Andhra_Pradesh"))
        m.add_command(label = 'East Godavari', command = lambda:self.notify_func("East Godavari", "Andhra_Pradesh"))
        m.add_command(label = 'Guntur', command = lambda:self.notify_func("Guntur", "Andhra_Pradesh"))
        m.add_command(label = 'Krishna', command = lambda:self.notify_func("Krishna", "Andhra_Pradesh"))
        m.add_command(label = 'Kurnool', command = lambda:self.notify_func("Kurnool", "Andhra_Pradesh"))
        m.add_command(label = 'Prakasam', command = lambda:self.notify_func("Prakasam", "Andhra_Pradesh"))
        m.add_command(label = 'S.P.S. Nellore', command = lambda:self.notify_func("S.P.S. Nellore", "Andhra_Pradesh"))
        m.add_command(label = 'Srikakulam', command = lambda:self.notify_func("Srikakulam", "Andhra_Pradesh"))
        m.add_command(label = 'Visakhapatnam', command = lambda:self.notify_func("Visakhapatnam", "Andhra_Pradesh"))
        m.add_command(label = 'Vizianagaram', command = lambda:self.notify_func("Vizianagaram", "Andhra_Pradesh"))
        m.add_command(label = 'West Godavari', command = lambda:self.notify_func("West Godavari", "Andhra_Pradesh"))
        m.add_command(label = 'Y.S.R. Kadapa', command = lambda:self.notify_func("Y.S.R. Kadapa", "Andhra_Pradesh"))
        
 
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Andhra Pradesh" in m:
                        #print(CC, RC, DC)
                          frame_notify_ = "Andhra Pradesh => | Total : " + f'{CC:n}'  + " | Deaths : "  + f'{DC:n}'  + " | Recovered : " + f'{RC:n}' 
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
        
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}'  + " | Total Deaths : " + f'{DC_:n}'  +  " | Recovered : " + f'{RC_:n}' 
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def APData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Andhra Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
   
       
class Arunachal_Pradesh(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Arunachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else:  
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Arunachal Pradesh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Arunachal Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
        
                var.set("Enable Notifications")
                
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Arunachal_Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
        
                self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.ARData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
        m.add_command(label = 'Anjaw', command = lambda:self.notify_func("Anjaw", "Arunachal_Pradesh"))
        m.add_command(label = 'Changlang', command = lambda:self.notify_func("Changlang", "Arunachal_Pradesh"))
        m.add_command(label = 'Dibang Valley', command = lambda:self.notify_func("Dibang Valley", "Arunachal_Pradesh"))
        m.add_command(label = 'East Kameng', command = lambda:self.notify_func("East Kameng", "Arunachal_Pradesh"))
        m.add_command(label = 'East Siang', command = lambda:self.notify_func("East Siang", "Arunachal_Pradesh"))
        m.add_command(label = 'Kra-Daadi', command = lambda:self.notify_func("Kra-Daadi", "Arunachal_Pradesh"))
        m.add_command(label = 'Kurung Kumey', command = lambda:self.notify_func("Kurung Kumey", "Arunachal_Pradesh"))
        m.add_command(label = 'Lepa Rada', command = lambda:self.notify_func("Lepa Rada", "Arunachal_Pradesh"))
        m.add_command(label = 'Longding', command = lambda:self.notify_func("Longding", "Arunachal_Pradesh"))
        m.add_command(label = 'Lower Dibang Valley', command = lambda:self.notify_func("Lower Dibang Valley", "Arunachal_Pradesh"))
        m.add_command(label = 'Lower Siang', command = lambda:self.notify_func("Lower Siang", "Arunachal_Pradesh"))
        m.add_command(label = 'Lower Subansiri', command = lambda:self.notify_func("Lower Subansiri", "Arunachal_Pradesh"))
        m.add_command(label = 'Namsai', command = lambda:self.notify_func("Namsai", "Arunachal_Pradesh"))
        m.add_command(label = 'Pakke Kessang', command = lambda:self.notify_func("Pakke Kessang", "Arunachal_Pradesh"))
        m.add_command(label = 'Papum Pare', command = lambda:self.notify_func("Papum Pare", "Arunachal_Pradesh"))
        m.add_command(label = 'Shi Yomi', command = lambda:self.notify_func("Shi Yomi", "Arunachal_Pradesh"))
        m.add_command(label = 'Siang', command = lambda:self.notify_func("Siang", "Arunachal_Pradesh"))
        m.add_command(label = 'Tawang', command = lambda:self.notify_func("Tawang", "Arunachal_Pradesh"))
        m.add_command(label = 'Tirap', command = lambda:self.notify_func("Tirap", "Arunachal_Pradesh"))
        m.add_command(label = 'Upper Siang', command = lambda:self.notify_func("Upper Siang", "Arunachal_Pradesh"))
        m.add_command(label = 'Upper Subansiri', command = lambda:self.notify_func("Upper Subansiri", "Arunachal_Pradesh"))
        m.add_command(label = 'West Kameng', command = lambda:self.notify_func("West Kameng", "Arunachal_Pradesh"))
        m.add_command(label = 'West Siang', command = lambda:self.notify_func("West Siang", "Arunachal_Pradesh"))


        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Arunachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Arunachal_Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")   
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def ARData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Arunachal Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Assam(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Assam" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else:  
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Assam" in m:
                        print(CC, RC, DC)
                        frame_notify = "Assam => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
        
                var.set("Enable Notifications")
                
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Assam",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
        
                self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.ASData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
        m.add_command(label = 'Baksa', command = lambda:self.notify_func("Baksa", "Assam"))
        m.add_command(label = 'Barpeta', command = lambda:self.notify_func("Barpeta", "Assam"))
        m.add_command(label = 'Biswanath', command = lambda:self.notify_func("Biswanath", "Assam"))
        m.add_command(label = 'Bongaigaon', command = lambda:self.notify_func("Bongaigaon", "Assam"))
        m.add_command(label = 'Cachar', command = lambda:self.notify_func("Cachar", "Assam"))
        m.add_command(label = 'Charaideo', command = lambda:self.notify_func("Charaideo", "Assam"))
        m.add_command(label = 'Chirang', command = lambda:self.notify_func("Chirang", "Assam"))
        m.add_command(label = 'Darrang', command = lambda:self.notify_func("Darrang", "Assam"))
        m.add_command(label = 'Dhemaji', command = lambda:self.notify_func("Dhemaji", "Assam"))
        m.add_command(label = 'Dhubri', command = lambda:self.notify_func("Dhubri", "Assam"))
        m.add_command(label = 'Dibrugarh', command = lambda:self.notify_func("Dibrugarh", "Assam"))
        m.add_command(label = 'Dima Hasao', command = lambda:self.notify_func("Dima Hasao", "Assam"))
        m.add_command(label = 'Goalpara', command = lambda:self.notify_func("Goalpara", "Assam"))
        m.add_command(label = 'Golaghat', command = lambda:self.notify_func("Golaghat", "Assam"))
        m.add_command(label = 'Hailakandi', command = lambda:self.notify_func("Hailakandi", "Assam"))
        m.add_command(label = 'Hojai', command = lambda:self.notify_func("Hojai", "Assam"))
        m.add_command(label = 'Jorhat', command = lambda:self.notify_func("Jorhat", "Assam"))
        m.add_command(label = 'Kamrup', command = lambda:self.notify_func("Kamrup", "Assam"))
        m.add_command(label = 'Kamrup Metropolitan', command = lambda:self.notify_func("Kamrup Metropolitan", "Assam"))
        m.add_command(label = 'Karbi Anglong', command = lambda:self.notify_func("Karbi Anglong", "Assam"))
        m.add_command(label = 'Karimganj', command = lambda:self.notify_func("Karimganj", "Assam"))
        m.add_command(label = 'Kishanganj', command = lambda:self.notify_func("Kishanganj", "Assam"))
        m.add_command(label = 'Kokrajhar', command = lambda:self.notify_func("Kokrajhar", "Assam"))
        m.add_command(label = 'Lakhimpur', command = lambda:self.notify_func("Lakhimpur", "Assam"))
        m.add_command(label = 'Majuli', command = lambda:self.notify_func("Majuli", "Assam"))
        m.add_command(label = 'Morigaon', command = lambda:self.notify_func("Morigaon", "Assam"))
        m.add_command(label = 'Nagaon', command = lambda:self.notify_func("Nagaon", "Assam"))
        m.add_command(label = 'Nalbari', command = lambda:self.notify_func("Nalbari", "Assam"))
        m.add_command(label = 'Sivasagar', command = lambda:self.notify_func("Sivasagar", "Assam"))
        m.add_command(label = 'Sonitpur', command = lambda:self.notify_func("Sonitpur", "Assam"))
        m.add_command(label = 'South Salmara Mankachar', command = lambda:self.notify_func("South Salmara Mankachar", "Assam"))
        m.add_command(label = 'Tinsukia', command = lambda:self.notify_func("Tinsukia", "Assam"))
        m.add_command(label = 'Udalguri', command = lambda:self.notify_func("Udalguri", "Assam"))
        m.add_command(label = 'West Karbi Anglong', command = lambda:self.notify_func("West Karbi Anglong", "Assam"))
       


        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Assam" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Assam=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")   
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def ASData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Assam", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Bihar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Bihar" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else:  
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Bihar" in m:
                        print(CC, RC, DC)
                        frame_notify = "Bihar => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
        
                var.set("Enable Notifications")
                
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Bihar",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
        
                self.master.master.destroy()
        
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.BRData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
        m.add_command(label = 'Araria', command = lambda:self.notify_func("Araria", "Bihar"))
        m.add_command(label = 'Arwal', command = lambda:self.notify_func("Arwal", "Bihar"))
        m.add_command(label = 'Aurangabad', command = lambda:self.notify_func("Aurangabad", "Bihar"))
        m.add_command(label = 'Banka', command = lambda:self.notify_func("Banka", "Bihar"))
        m.add_command(label = 'Begusarai', command = lambda:self.notify_func("Begusarai", "Bihar"))
        m.add_command(label = 'Bhagalpur', command = lambda:self.notify_func("Bhagalpur", "Bihar"))
        m.add_command(label = 'Bhojpur', command = lambda:self.notify_func("Bhojpur", "Bihar"))
        m.add_command(label = 'Buxar', command = lambda:self.notify_func("Buxar", "Bihar"))
        m.add_command(label = 'Darbhanga', command = lambda:self.notify_func("Darbhanga", "Bihar"))
        m.add_command(label = 'East Champaran', command = lambda:self.notify_func("East Champaran", "Bihar"))
        m.add_command(label = 'Gaya', command = lambda:self.notify_func("Gaya", "Bihar"))
        m.add_command(label = 'Gopalganj', command = lambda:self.notify_func("Gopalganj", "Bihar"))
        m.add_command(label = 'Jamui', command = lambda:self.notify_func("Jamui", "Bihar"))
        m.add_command(label = 'Jehanabad', command = lambda:self.notify_func("Jehanabad", "Bihar"))
        m.add_command(label = 'Kaimur', command = lambda:self.notify_func("Kaimur", "Bihar"))
        m.add_command(label = 'Katihar', command = lambda:self.notify_func("Katihar", "Bihar"))
        m.add_command(label = 'Khagaria', command = lambda:self.notify_func("Khagaria", "Bihar"))
        m.add_command(label = 'Kishanganj', command = lambda:self.notify_func("Kishanganj", "Bihar"))
        m.add_command(label = 'Lakhisarai', command = lambda:self.notify_func("Lakhisarai", "Bihar"))
        m.add_command(label = 'Madhepura', command = lambda:self.notify_func("Madhepura", "Bihar"))
        m.add_command(label = 'Madhubani', command = lambda:self.notify_func("Madhubani", "Bihar"))
        m.add_command(label = 'Munger', command = lambda:self.notify_func("Munger", "Bihar"))
        m.add_command(label = 'Muzaffarpur', command = lambda:self.notify_func("Muzaffarpur", "Bihar"))
        m.add_command(label = 'Nalanda', command = lambda:self.notify_func("Nalanda", "Bihar"))
        m.add_command(label = 'Nawada', command = lambda:self.notify_func("Nawada", "Bihar"))
        m.add_command(label = 'Patna', command = lambda:self.notify_func("Patna", "Bihar"))
        m.add_command(label = 'Purnia', command = lambda:self.notify_func("Purnia", "Bihar"))
        m.add_command(label = 'Rohtas', command = lambda:self.notify_func("Rohtas", "Bihar"))
        m.add_command(label = 'Saharsa', command = lambda:self.notify_func("Saharsa", "Bihar"))
        m.add_command(label = 'Samastipur', command = lambda:self.notify_func("Samastipur", "Bihar"))
        m.add_command(label = 'Saran', command = lambda:self.notify_func("Saran", "Bihar"))
        m.add_command(label = 'Sheikhpura', command = lambda:self.notify_func("Sheikhpura", "Bihar"))
        m.add_command(label = 'Sheohar', command = lambda:self.notify_func("Sheohar", "Bihar"))
        m.add_command(label = 'Sitamarhi', command = lambda:self.notify_func("Sitamarhi", "Bihar"))
        m.add_command(label = 'Siwan', command = lambda:self.notify_func("Siwan", "Bihar"))
        m.add_command(label = 'Supaul', command = lambda:self.notify_func("Supaul", "Bihar"))
        m.add_command(label = 'Vaishali', command = lambda:self.notify_func("Vaishali", "Bihar"))
        m.add_command(label = 'West Champaran', command = lambda:self.notify_func("West Champaran", "Bihar"))
        

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Bihar" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Bihar=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan") 
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def BRData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Bihar", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


    

class Chandigarh(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chandigarh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
             
            for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                if "Chandigarh" in m:
                    print(CC, RC, DC)
                    frame_notify = "Chandigarh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
            messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
            var.set("Enable Notifications")
            
            # calling plyer Notification
            while True:
                plyer.notification.notify( title = "Covid19 cases of Chandigarh",
                                          message = frame_notify, app_icon = ICON,timeout = 20)
                time.sleep(self.t1)
    
            self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.CHData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
        m.add_command(label = 'Chandigarh', command = lambda:self.notify_func("Chandigarh", "Chandigarh"))
          

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chandigarh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Chandigarh=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
         
                self.master.master.destroy() 
                
            else:
                messagebox.showerror("Error", "Please select Notification timespan")   
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def CHData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Chandigarh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Chhattisgarh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chhattisgarh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Chhattisgarh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Chhattisgarh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Chhattisgarh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.CTData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'Balod', command = lambda:self.notify_func("Balod","Chhattisgarh"))
        m.add_command(label = 'Baloda Bazar', command = lambda:self.notify_func("Baloda Bazar","Chhattisgarh"))
        m.add_command(label = 'Balrampur', command = lambda:self.notify_func("Balrampur","Chhattisgarh"))
        m.add_command(label = 'Bametara', command = lambda:self.notify_func("Bametara","Chhattisgarh"))
        m.add_command(label = 'Bastar', command = lambda:self.notify_func("Bastar","Chhattisgarh"))
        m.add_command(label = 'Bijapur', command = lambda:self.notify_func("Bijapur","Chhattisgarh"))
        m.add_command(label = 'Bilaspur', command = lambda:self.notify_func("Bilaspur","Chhattisgarh"))
        m.add_command(label = 'Dakshin Bastar Dantewada', command = lambda:self.notify_func("Dakshin Bastar Dantewada","Chhattisgarh"))
        m.add_command(label = 'Dhamtari', command = lambda:self.notify_func("Dhamtari","Chhattisgarh"))
        m.add_command(label = 'Durg', command = lambda:self.notify_func("Durg","Chhattisgarh"))
        m.add_command(label = 'Gariaband', command = lambda:self.notify_func("Gariaband","Chhattisgarh"))
        m.add_command(label = 'Gaurela Pendra Marwahi', command = lambda:self.notify_func("Gaurela Pendra Marwahi","Chhattisgarh"))
        m.add_command(label = 'Janjgir Champa', command = lambda:self.notify_func("Janjgir Champa","Chhattisgarh"))
        m.add_command(label = 'Jashpur', command = lambda:self.notify_func("Jashpur","Chhattisgarh"))
        m.add_command(label = 'Kabeerdham', command = lambda:self.notify_func("Kabeerdham","Chhattisgarh"))
        m.add_command(label = 'Kondagaon', command = lambda:self.notify_func("Kondagaon","Chhattisgarh"))
        m.add_command(label = 'Korba', command = lambda:self.notify_func("Korba","Chhattisgarh"))
        m.add_command(label = 'Koriya', command = lambda:self.notify_func("Koriya","Chhattisgarh"))
        m.add_command(label = 'Mahasamund', command = lambda:self.notify_func("Mahasamund","Chhattisgarh"))
        m.add_command(label = 'Mungeli', command = lambda:self.notify_func("Mungeli","Chhattisgarh"))
        m.add_command(label = 'Narayanpur', command = lambda:self.notify_func("Narayanpur","Chhattisgarh"))
        m.add_command(label = 'Raigarh', command = lambda:self.notify_func("Raigarh","Chhattisgarh"))
        m.add_command(label = 'Raipur', command = lambda:self.notify_func("Raipur","Chhattisgarh"))
        m.add_command(label = 'Rajnandgaon', command = lambda:self.notify_func("Rajnandgaon","Chhattisgarh"))
        m.add_command(label = 'Sukma', command = lambda:self.notify_func("Sukma","Chhattisgarh"))
        m.add_command(label = 'Surajpur', command = lambda:self.notify_func("Surajpur","Chhattisgarh"))
        m.add_command(label = 'Surguja', command = lambda:self.notify_func("Surguja","Chhattisgarh"))
        m.add_command(label = 'Uttar Bastar Kanker', command = lambda:self.notify_func("Uttar Bastar Kanker","Chhattisgarh"))
        
 
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chhattisgarh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Chhattisgarh=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def CTData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Chhattisgarh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        

class Delhi(tk.Frame):
 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Delhi" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
             
            for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                if "Delhi" in m:
                    print(CC, RC, DC)
                    frame_notify = "Delhi => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
            messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
            var.set("Enable Notifications")
            
            # calling plyer Notification
            while True:
                plyer.notification.notify( title = "Covid19 cases of Delhi",
                                          message = frame_notify, app_icon = ICON,timeout = 20)
                time.sleep(self.t1)
    
            self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.DLData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'Delhi', command = lambda:self.notify_func("Delhi","Delhi"))
   
 
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Delhi" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Delhi=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def DLData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Delhi", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
        
         
class Dadra_and_Nagar_Haveli_and_Daman_and_Diu(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):

            if "Dadra and Nagar Haveli and Daman and Diu" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Dadra and Nagar Haveli and Daman and Diu" in m:
                        print(CC, RC, DC)
                        frame_notify = "Dadra,Nagar... => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Dadra,Nagar,Haveli,Daman and Diu",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.DNData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'Dadra and Nagar Haveli', command = lambda:self.notify_func("Dadra and Nagar Haveli","Dadra_and_Nagar_Haveli_and_Daman_and_Diu"))
        m.add_command(label = 'Daman', command = lambda:self.notify_func("Daman","Dadra_and_Nagar_Haveli_and_Daman_and_Diu"))
        m.add_command(label = 'Diu', command = lambda:self.notify_func("Diu","Dadra_and_Nagar_Haveli_and_Daman_and_Diu"))

    
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Dadra and Nagar Haveli and Daman and Diu" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Dadra,Nagar..=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of "  + city ,
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def DNData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Dadra Nagar Haveli ..", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        


class Goa(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Goa" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Goa" in m:
                        print(CC, RC, DC)
                        frame_notify = "Goa => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Goa",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.GAData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'North Goa', command = lambda:self.notify_func("North Goa","Goa"))
        m.add_command(label = 'South Goa', command = lambda:self.notify_func("South Goa","Goa"))
       
        background.bind("<Button-3>", city_pop)
      
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Goa" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Goa=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def GAData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Goa", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        

class Gujarat(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Gujarat" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Gujarat" in m:
                        print(CC, RC, DC)
                        frame_notify = "Gujarat => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Gujarat",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.GJData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'Ahmedabad', command = lambda:self.notify_func("Ahmedabad","Gujarat"))
        m.add_command(label = 'Amreli', command = lambda:self.notify_func("Amreli","Gujarat"))
        m.add_command(label = 'Anand', command = lambda:self.notify_func("Anand","Gujarat"))
        m.add_command(label = 'Aravalli', command = lambda:self.notify_func("Aravalli","Gujarat"))
        m.add_command(label = 'Banaskantha', command = lambda:self.notify_func("Banaskantha","Gujarat"))
        m.add_command(label = 'Bharuch', command = lambda:self.notify_func("Bharuch","Gujarat"))
        m.add_command(label = 'Bhavnagar', command = lambda:self.notify_func("Bhavnagar","Gujarat"))
        m.add_command(label = 'Botad', command = lambda:self.notify_func("Botad","Gujarat"))
        m.add_command(label = 'Chhota Udaipur', command = lambda:self.notify_func("Chhota Udaipur","Gujarat"))
        m.add_command(label = 'Dahod', command = lambda:self.notify_func("Dahod","Gujarat"))
        m.add_command(label = 'Dang', command = lambda:self.notify_func("Dang","Gujarat"))
        m.add_command(label = 'Devbhumi Dwarka', command = lambda:self.notify_func("Devbhumi Dwarka","Gujarat"))
        m.add_command(label = 'Gandhinagar', command = lambda:self.notify_func("Gandhinagar","Gujarat"))
        m.add_command(label = 'Gir Somnath', command = lambda:self.notify_func("Gir Somnath","Gujarat"))
        m.add_command(label = 'Jamnagar', command = lambda:self.notify_func("Jamnagar","Gujarat"))
        m.add_command(label = 'Junagadh', command = lambda:self.notify_func("Junagadh","Gujarat"))
        m.add_command(label = 'Kheda', command = lambda:self.notify_func("Kheda","Gujarat"))
        m.add_command(label = 'Kutch', command = lambda:self.notify_func("Kutch","Gujarat"))
        m.add_command(label = 'Mahisagar', command = lambda:self.notify_func("Mahisagar","Gujarat"))
        m.add_command(label = 'Mehsana', command = lambda:self.notify_func("Mehsana","Gujarat"))
        m.add_command(label = 'Morbi', command = lambda:self.notify_func("Morbi","Gujarat"))
        m.add_command(label = 'Narmada', command = lambda:self.notify_func("Narmada","Gujarat"))
        m.add_command(label = 'Navsari', command = lambda:self.notify_func("Navsari","Gujarat"))
        m.add_command(label = 'Panchmahal', command = lambda:self.notify_func("Panchmahal","Gujarat"))
        m.add_command(label = 'Patan', command = lambda:self.notify_func("Patan","Gujarat"))
        m.add_command(label = 'Porbandar', command = lambda:self.notify_func("Porbandar","Gujarat"))
        m.add_command(label = 'Rajkot', command = lambda:self.notify_func("Rajkot","Gujarat"))
        m.add_command(label = 'Sabarkantha', command = lambda:self.notify_func("Sabarkantha","Gujarat"))
        m.add_command(label = 'Surat', command = lambda:self.notify_func("Surat","Gujarat"))
        m.add_command(label = 'Surendranagar', command = lambda:self.notify_func("Surendranagar","Gujarat"))
        m.add_command(label = 'Tapi', command = lambda:self.notify_func("Tapi","Gujarat"))
        m.add_command(label = 'Vadodara', command = lambda:self.notify_func("Vadodara","Gujarat"))
        m.add_command(label = 'Valsad', command = lambda:self.notify_func("Valsad","Gujarat"))
 
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Gujarat" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Gujarat=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def GJData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Gujarat", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
       
class Himachal_Pradesh(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Himachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Himachal Pradesh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Himachal Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Himachal Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.HPData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'Bilaspur', command = lambda:self.notify_func("Bilaspur","Himachal_Pradesh"))
        m.add_command(label = 'Chamba', command = lambda:self.notify_func("Chamba","Himachal_Pradesh"))
        m.add_command(label = 'Hamirpur', command = lambda:self.notify_func("Hamirpur","Himachal_Pradesh"))
        m.add_command(label = 'Kangra', command = lambda:self.notify_func("Kangra","Himachal_Pradesh"))
        m.add_command(label = 'Kinnaur', command = lambda:self.notify_func("Kinnaur","Himachal_Pradesh"))
        m.add_command(label = 'Kullu', command = lambda:self.notify_func("Kullu","Himachal_Pradesh"))
        m.add_command(label = 'Lahaul', command = lambda:self.notify_func("Lahaul","Himachal_Pradesh"))
        m.add_command(label = 'Mandi', command = lambda:self.notify_func("Mandi","Himachal_Pradesh"))
        m.add_command(label = 'Shimla', command = lambda:self.notify_func("Shimla","Himachal_Pradesh"))
        m.add_command(label = 'Sirmaur', command = lambda:self.notify_func("Sirmaur","Himachal_Pradesh"))
        m.add_command(label = 'Solan', command = lambda:self.notify_func("Solan","Himachal_Pradesh"))
        m.add_command(label = 'Una', command = lambda:self.notify_func("Una","Himachal_Pradesh"))

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Himachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Himachal Pradesh=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def HPData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Himachal Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Haryana(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Haryana" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Haryana" in m:
                        print(CC, RC, DC)
                        frame_notify = "Haryana => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Himachal Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.HRData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Haryana"))
      
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Haryana" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Haryana => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def HRData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Haryana", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Jammu_and_Kashmir(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jammu and Kashmir" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Jammu and Kashmir" in m:
                        print(CC, RC, DC)
                        frame_notify = "Jammu and Kashmir => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Jammu and Kashmir",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.JKData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Jammu_and_Kashmir"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jammu and Kashmir" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Jammu and Kashmir => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def JKData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Jammu and Kashmir", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Karnataka(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Karnataka" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Karnataka" in m:
                        print(CC, RC, DC)
                        frame_notify = "Karnataka => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Karnataka",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.KAData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Karnataka"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Karnataka" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Karnataka => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def KAData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Karnataka", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Karnataka(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Karnataka" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Karnataka" in m:
                        print(CC, RC, DC)
                        frame_notify = "Karnataka => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Karnataka",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.KAData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Karnataka"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Karnataka" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Karnataka => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def KAData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Karnataka", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Jharkhand(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jharkhand" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Jharkhand" in m:
                        print(CC, RC, DC)
                        frame_notify = "Jharkhand => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Jharkhand",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.JHData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Jharkhand"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jharkhand" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Jharkhand => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def JHData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Jharkhand", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



        
class Kerala(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Kerala" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Kerala" in m:
                        print(CC, RC, DC)
                        frame_notify = "Kerala => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Kerala",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.KLData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Kerala"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Kerala" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Kerala => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def KLData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Kerala", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Ladakh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Ladakh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Ladakh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Ladakh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Ladakh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.LAData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Ladakh"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Ladakh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Ladakh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def LAData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Ladakh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Meghalaya(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Meghalaya" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Meghalaya" in m:
                        print(CC, RC, DC)
                        frame_notify = "Meghalaya => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Meghalaya",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.MLData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Meghalaya"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Meghalaya" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Meghalaya => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def MLData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Meghalaya", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Manipur(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Manipur" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Manipur" in m:
                        print(CC, RC, DC)
                        frame_notify = "Manipur => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Manipur",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.MNData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Manipur"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Manipur" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Manipur => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def MNData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Manipur", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Madhya_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Madhya Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Madhya Pradesh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Madhya Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Madhya Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.MPData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Madhya_Pradesh"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Madhya Pradesh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Madhya Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def MPData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Madhya Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Mizoram(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Mizoram" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Mizoram" in m:
                        print(CC, RC, DC)
                        frame_notify = "Mizoram => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Mizoram",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.MZData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Mizoram"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Mizoram" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Mizoram => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def MZData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Mizoram", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Nagaland(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Nagaland" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Nagaland" in m:
                        print(CC, RC, DC)
                        frame_notify = "Nagaland => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Nagaland",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.NLData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Nagaland"))

        background.bind("<Button-3>", city_pop)
   
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Nagaland" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Nagaland => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def NLData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Nagaland", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Odisha(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Odisha" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Odisha" in m:
                        print(CC, RC, DC)
                        frame_notify = "Odisha => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Odisha",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.ORData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Odisha"))
      
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Odisha" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Odisha => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def ORData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Odisha", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Punjab(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Punjab" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Punjab" in m:
                        print(CC, RC, DC)
                        frame_notify = "Punjab => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Punjab",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.PBData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Punjab"))
      
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Punjab" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Punjab => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def PBData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Punjab", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Puducherry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Puducherry" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Puducherry" in m:
                        print(CC, RC, DC)
                        frame_notify = "Puducherry => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Puducherry",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.PYData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Puducherry"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Puducherry" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Puducherry => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def PYData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Puducherry", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Rajasthan(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Rajasthan" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Rajasthan" in m:
                        print(CC, RC, DC)
                        frame_notify = "Rajasthan => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Rajasthan",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.RJData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Rajasthan"))


        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Rajasthan" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Rajasthan => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def RJData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Rajasthan", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Sikkim(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Sikkim" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Sikkim" in m:
                        print(CC, RC, DC)
                        frame_notify = "Sikkim => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Sikkim",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.SKData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Sikkim"))
     
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Sikkim" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Sikkim => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def SKData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Sikkim", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



#missing data
class Telangana(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Telangana" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        # def notify(t):
        #     if "half hourly" in var.get():
        #         self.t1 = 1800
        #     if "hourly" in var.get():
        #         self.t1 = 3600
        #     if "4 hourly" in var.get():
        #         self.t1 = 14400
        #     if "8 hourly" in var.get():
        #         self.t1 = 28800
        #     if "12 hourly" in var.get():
        #         self.t1 = 43200
                
        #     response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
        #     if response == "yes":
        #         messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
        #     else: 
        #         for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
        #             if "Telangana" in m:
        #                 print(CC, RC, DC)
        #                 frame_notify = "Telangana => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
        #         messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
        #         var.set("Enable Notifications")
            
        #         # calling plyer Notification
        #         while True:
        #             plyer.notification.notify( title = "Covid19 cases of Telangana",
        #                                       message = frame_notify, app_icon = ICON,timeout = 20)
        #             time.sleep(self.t1)
    
        #         self.master.master.destroy()
    
             
        # # option menu for time duration
        # var = StringVar()
        # varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        # var.set("Enable Notifications")
        # notifyMenu = OptionMenu(self, var, *varList, command = notify)
        # notifyMenu.configure(bg = "black", fg = "White")
        # notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.TData(background, frame_text)
      
  
      
   # # City list on rightclick         
   #      def city_pop(event):
   #          m.tk_popup(event.x_root, event.y_root)
   #          m.grab_release()
            
   #      m = tk.Menu(background, tearoff = 0)
         
   #      m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Telangana"))
       
   #      background.bind("<Button-3>", city_pop)
      
      
                
   #  def notify_func(self,city,state):
   #      for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
   #          if "Telangana" in m:
   #              #print(CC, RC, DC)
   #              frame_notify_ = "Telangana => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
   #      print(self.t1)
   #      print(city, state)
   #      city_data = notify_app_city_data(city, state) 
   #      for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
   #          #print(m1)
   #          if city in m1:
   #              print(CC_, RC_, DC_)
   #              frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
   #      if  frame_city_text:
   #          if self.t1 != 0:
   #              messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
   #                                  "Details : " + frame_city_text)
   #              while True:
   #                  plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
   #                                            message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
   #                  time.sleep(self.t1)
            
       
   #              self.master.master.destroy()    
   #          else:
   #              messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def TData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Telangana", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                          font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Tamil_Nadu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tamil Nadu" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Tamil Nadu" in m:
                        print(CC, RC, DC)
                        frame_notify = "Tamil Nadu => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Tamil Nadu",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.TNData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Tamil_Nadu"))
     

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tamil Nadu" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Tamil Nadu=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def TNData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Tamil Nadu", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


        
class Tripura(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tripura" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Tripura" in m:
                        print(CC, RC, DC)
                        frame_notify = "Tripura => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Tripura",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.TRData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Tripura"))
    
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tripura" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Tripura => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def TRData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Tripura", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Uttar_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttar Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Uttar Pradesh" in m:
                        print(CC, RC, DC)
                        frame_notify = "Uttar Pradesh => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Uttar Pradesh",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.UPData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Uttar_Pradesh"))
       
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttar Pradesh" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Uttar Pradesh=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def UPData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Uttar Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Uttarakhand(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttarakhand" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "Uttarakhand" in m:
                        print(CC, RC, DC)
                        frame_notify = "Uttarakhand => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of Uttarakhand",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.UTData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","Uttarakhand"))
        
        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttarakhand" in m:
                #print(CC, RC, DC)
                frame_notify_ = "Uttarakhand=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def UTData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "Uttarakhand", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


        
class West_Bengal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.t1 = 0
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img


        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "West Bengal" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + f'{CC:n}' + "\n" + "Total Deaths : " + f'{DC:n}' + "\n" + "Recovered : " + f'{RC:n}'  
                    
      
        def notify(t):
            if "half hourly" in var.get():
                self.t1 = 1800
            if "hourly" in var.get():
                self.t1 = 3600
            if "4 hourly" in var.get():
                self.t1 = 14400
            if "8 hourly" in var.get():
                self.t1 = 28800
            if "12 hourly" in var.get():
                self.t1 = 43200
                
            response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
            if response == "yes":
                messagebox.showinfo("Notification Settings", "\nRIGHT CLICK on the vertices of app window to Select your City")
            else: 
                for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
                    if "West Bengal" in m:
                        print(CC, RC, DC)
                        frame_notify = "West Bengal => | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
                messagebox.showinfo("Notification details","Notification time span is : " + var.get() + "\nNotification Message : " + frame_notify)
    
                var.set("Enable Notifications")
            
                # calling plyer Notification
                while True:
                    plyer.notification.notify( title = "Covid19 cases of West Bengal",
                                              message = frame_notify, app_icon = ICON,timeout = 20)
                    time.sleep(self.t1)
    
                self.master.master.destroy()
    
             
        # option menu for time duration
        var = StringVar()
        varList = ["half hourly", "hourly", "4 hourly", "8 hourly", "12 hourly"]
        var.set("Enable Notifications")
        notifyMenu = OptionMenu(self, var, *varList, command = notify)
        notifyMenu.configure(bg = "black", fg = "White")
        notifyMenu.place(x=1, y=1)
        
            
        self.setWidget(background,controller)
        self.bannerName(background)
        self.WBData(background, frame_text)
      
  
      
   # City list on rightclick         
        def city_pop(event):
            m.tk_popup(event.x_root, event.y_root)
            m.grab_release()
            
        m = tk.Menu(background, tearoff = 0)
         
        m.add_command(label = 'cityname', command = lambda:self.notify_func("cityname","West_Bengal"))
       

        background.bind("<Button-3>", city_pop)
      
      
                
    def notify_func(self,city,state):
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "West Bengal" in m:
                #print(CC, RC, DC)
                frame_notify_ = "West Bengal=> | Total : " + f'{CC:n}' + " | Deaths : "  + f'{DC:n}' + " | Recovered : " + f'{RC:n}'
              
        print(self.t1)
        print(city, state)
        city_data = notify_app_city_data(city, state) 
        for m1, CC_, RC_, DC_ in zip(city_data.index, city_data["Confirmed cases"], city_data["Recovered cases"], city_data["Death toll"]):
            #print(m1)
            if city in m1:
                print(CC_, RC_, DC_)
                frame_city_text = city + " => Total Cases : " + f'{CC_:n}' + " | Total Deaths : " + f'{DC_:n}' +  " | Recovered : " + f'{RC_:n}'  
            
        if  frame_city_text:
            if self.t1 != 0:
                messagebox.showinfo("Notification Details","Notification Time span is : " + str(self.t1) + " seconds" + "\nState : " + state + "\n" + "City : " + city + "\n" +
                                    "Details : " + frame_city_text)
                while True:
                    plyer.notification.notify( title = "Covid19 cases of " + state + " ( " + city + " ) ",
                                              message = frame_notify_ +"\n" + frame_city_text, app_icon = ICON, timeout = 10)
                    time.sleep(self.t1)
            
       
                self.master.master.destroy()    
            else:
                messagebox.showerror("Error", "Please select Notification timespan")
       
         
             
    def setWidget(self, background,controller):
        load = PIL.Image.open(WORLD_IMG)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(background, image=render)
        img.image = render
        img.place(x=160, y=10)

 
    def bannerName(self, frame0_back):

        frame_0 = LabelFrame(frame0_back, padx=2, pady=2, bg='#336699')
        frame_0.place(x=30, y=90)
        f0_label = Label(frame_0, text=" Covid19 Tracker - INDIA ",
                         font=FRAME0_FONT, fg="White", bg = 'Black')
        f0_label.pack(side=RIGHT)

    def WBData(self, frame1_back, frame_text):
        
        frame_1 = LabelFrame(frame1_back, text = "West Bengal", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)




def main():

    #data = covid_data.Covid_tracker()
    app = CovidApp()
    app.mainloop()
  
    #notify_fun.mainloop()


if __name__ == '__main__':
    main()
