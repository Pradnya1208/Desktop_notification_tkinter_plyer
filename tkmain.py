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


from Indian_states import state_name
from nameCorrection import name_correction
from states_data import merged

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
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
        
        frame_1 = LabelFrame(frame1_back, text = "Covid19 Cases in India", font = FRAME1_FONT, padx=5, pady=10, bg= 'Black', fg ="Red")
        frame_1.place(x=60, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", padx = 10, pady = 10, justify = LEFT)
        f1_label.pack(side=LEFT)
        
    

class Maharashtra(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
        self.run(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("Desktop Notification settings", "Do you want a city specific Covid19 Notifications?")
        if response == "yes":
            messagebox.showinfo("", "Right click on main window to select a City ")
        else:
            pass
            #call plyer function
         
             
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Maharashtra" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Maharashtra", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
    def popup(self, frame0_back): 
        self.popup_menu = tk.Menu(frame0_back, 
                                       tearoff = 0) 
      
        self.popup_menu.add_command(label = "say hi", 
                                    command = lambda:self.hey("hi")) 
      
        self.popup_menu.add_command(label = "say hello", 
                                    command = lambda:self.hey("hello")) 
        self.popup_menu.add_separator() 
        self.popup_menu.add_command(label = "say bye", 
                                command = lambda:self.hey("bye")) 
   
    #display menu on right click 
    def do_popup(self,event): 
        try: 
            self.popup_menu.tk_popup(event.x_root, 
                                 event.y_root) 
        finally: 
            self.popup_menu.grab_release() 
   
    def hey(self,s): 
        self.configure(text = s) 
      
    def run(self,frame0_back): 
        self.popup(frame0_back) 
        self.bind("<Button-3>",self.do_popup) 
   
        
       
class Andaman_and_Nikobar_Islands(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            rt = Tk()
            rt.iconbitmap(ICON)
            rt.title("Select City")  
            l = Label(rt, text = "test").pack()
           
           
        else:
            pass
            #call plyer function
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Andaman and Nikobar Islands" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Andaman and Nikobar Islands", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        

                
class Andhra_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Andhra Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Andhra Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
       
class Arunachal_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Arunachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Arunachal Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Assam(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
 
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Assam" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Assam", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)



class Bihar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
 
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Bihar" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Bihar", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)    
 
    
class Chandigarh(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
  
          
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chandigarh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Chandigarh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Chhattisgarh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
      
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chandigarh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Chhattisgarh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Delhi(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
    
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Chandigarh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Delhi", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
         
class Dadra_and_Nagar_Haveli_and_Daman_and_Diu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
     
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Dadra and Nagar Haveli and Daman and Diu" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Dadra,Nagar Haveli,Daman,Diu", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = CENTER)
        f1_label.pack(side=LEFT)


class Goa(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
 
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Goa" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Goa", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)       
        

class Gujarat(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
  
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Gujarat" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Gujarat", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

        
class Himachal_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
    
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Himachal Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Himachal Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Haryana(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
    
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Haryana" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Haryana", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
class Jharkhand(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
  
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jharkhand" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Jharkhand", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Jammu_and_Kashmir(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
   
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Jammu and Kashmir" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Jammu and Kashmir", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Karnataka(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Karnataka" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Karnataka", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
class Kerala(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
    
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Kerala" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Kerala", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Ladakh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
    
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Ladakh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Ladakh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Meghalaya(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
      
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Meghalaya" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Meghalaya", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Manipur(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Manipur" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Manipur", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Madhya_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Madhya Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Madhya Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Mizoram(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
      
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Mizoram" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Mizoram", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)


class Nagaland(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Madhya Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Nagaland", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Odisha(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
       
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Odisha" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Odisha", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Punjab(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Punjab" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Punjab", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Puducherry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
       
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Puducherry" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Puducherry", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Rajasthan(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Rajasthan" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Rajasthan", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Sikkim(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Sikkim" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Sikkim", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Telangana(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Telangana" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Telangana", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Tamil_Nadu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
     
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tamil Nadu" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Tamil Nadu", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
class Tripura(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
      
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Tripura" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Tripura", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Uttar_Pradesh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
  
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttar Pradesh" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Uttar Pradesh", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)

class Uttarakhand(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
   
   
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "Uttarakhand" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
        frame_1 = LabelFrame(frame1_back, text = "Uttarakhand", font = FRAME1_FONT, padx =30, pady =10, bg= 'Black', fg ="Red")
        frame_1.place(x=55, y=150)

        f1_label = Label(frame_1, text=frame_text,
                         font = FRAME1_1, fg="White", bg = "black", justify = LEFT)
        f1_label.pack(side=LEFT)
        
class West_Bengal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = tk.PhotoImage(file=IMAGE_PATH)
        background = tk.Label(self, image=img)
        background.pack(fill=BOTH, expand=1)
        background.image = img

        notify = tk.Button(self, text="Enable Notification", bg="black", fg="White",font = NOTIFY_F, 
                           padx = 5, pady = 5,command=self.notify)
        notify.place(x=1,y=1)
   
        def change_on_hover(event):
            notify['bg'] = 'red'

        def return_to_normal(event):
            notify['bg'] = "black"
            
        notify.bind('<Enter>', change_on_hover)
        notify.bind('<Leave>', return_to_normal)
        

        self.setWidget(background,controller)
        self.MHData(background)
        self.bannerName(background)
   
       
    def notify(self):
       
        response = messagebox.askquestion("messag box", "Hello world!")
        if response == "yes":
            notify_fun = tk.Tk()
        else:
            pass
            #call plyer function
         
    
            
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

    def MHData(self, frame1_back):
        
        
        for m, CC, RC, DC in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "West Bengal" in m:
                #print(CC, RC, DC)
                frame_text = "Total Cases : " + str(CC) + "\n" + "Total Deaths : " + str(DC) + "\n" + "Recovered : " + str(RC)  
                
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
