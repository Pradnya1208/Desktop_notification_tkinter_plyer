#!/usr/bin/env python

from tkinter import Tk
import os
import subprocess
import platform
#from django.http import HttpResponse
from tkinter import messagebox
from tkinter import Tk, ttk, Toplevel
from PIL import ImageTk, ImageDraw
import PIL.Image
from tkinter import *
import sys
from bs4 import BeautifulSoup
import requests

<<<<<<< HEAD

#state=sys.argv[1]
=======
#if (sys.argv[1])
 #   state=sys.argv[1]
#else
state = "World"
>>>>>>> 04880f0... Added tkinter frames

IMAGE_PATH = '..//covid_t.jpg'
IMAGE_PATH1 = '..//back1.jpg'
WIDTH, HEIGHT = 650, 500
f1 = ("poppins", 25, "bold")
f2 = ("Helvetica", 24,"bold")
<<<<<<< HEAD
urls = ["https://www.worldometers.info/coronavirus/"]




def get_data(urls):
    Cases_world = []
    for url in urls:
       covid_world = requests.get(url)
       soup_world = BeautifulSoup(covid_world.content, 'html.parser')
       Cases_world += soup_world.find_all("div", class_="maincounter-number")


    covid_data = "Cases world over :" + ((str(Cases_world[0]).split(">")[2]).split("<")[0]) + "\n" + "Total Deaths are : " + ((str(Cases_world[1]).split(">")[2]).split("<")[0]) + "\n" + "Total recovered are : " + ((str(Cases_world[2]).split(">")[2]).split("<")[0])

=======
world_url = "https://www.worldometers.info/coronavirus/"




def covid_scraper(urls,location):
    data = []
    container_start_data = []
    covid_world = requests.get(urls)
    
    soup_world = BeautifulSoup(covid_world.content, 'html.parser')


    container = soup_world.find(id = "covid19-container")
    container_data = container.find("tbody")
    container_start = container_data.find("tr", class_ = "sorttop")

    data += container_data.find_all("td")  #TODO for City related data
    container_start_data += container_start.find_all("th")

    covid_data = location + "\n" + "Total Cases : " + container_start_data[1].text + "\n" + "Deaths : " + container_start_data[2].text+ "\n" + "Recovery : " + container_start_data[3].text + "\n" + "Active Cases : " + container_start_data[4].text
   
>>>>>>> 04880f0... Added tkinter frames
    return covid_data




<<<<<<< HEAD
=======

>>>>>>> 04880f0... Added tkinter frames
def resize(w,h,root):

    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
  
    x = (ws/2) - (w/3)
    y = (hs/2) - (h/2)
   
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))




def tk_window(data):
    root = Tk()
    resize(WIDTH,HEIGHT,root)
    root.attributes("-topmost", True)
<<<<<<< HEAD
    root.title("COVID19 DATA TRACKER")
    canvas=Canvas(root, width=WIDTH,height=HEIGHT)
    image=ImageTk.PhotoImage(PIL.Image.open(IMAGE_PATH))
    canvas.create_image(0,0,anchor=NW,image=image)
    canvas.pack()


    banner = ImageTk.PhotoImage(PIL.Image.open(IMAGE_PATH1).resize((100,100),PIL.Image.ANTIALIAS))
    bannerLabel = canvas.create_image(30,30,anchor=NW,image=banner)

    canvas.create_text(50,100,font= f2,fill='#fff',text=data,anchor=NW)
=======
    root.title("COVID19 DATA TRACKER :"+ state)

    #For background image
    #canvas=Canvas(root, width=WIDTH,height=HEIGHT)
    #image=ImageTk.PhotoImage(PIL.Image.open(IMAGE_PATH))
    #canvas.create_image(0,0,anchor=NW,image=image)
    #canvas.pack()


    #banner = ImageTk.PhotoImage(PIL.Image.open(IMAGE_PATH1).resize((100,100),PIL.Image.ANTIALIAS))
    #bannerLabel = canvas.create_image(30,30,anchor=NW,image=banner)

    #canvas.create_text(50,100,font= f2,fill='#fff',text=data,anchor=NW)
>>>>>>> 04880f0... Added tkinter frames
    root.mainloop()




def main():
<<<<<<< HEAD
    data = get_data(urls)
=======

    if state == "World":
        path = "https://en.wikipedia.org/wiki/COVID-19_pandemic"
    else:
        path = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_" + state
    data = covid_scraper(path, state)

>>>>>>> 04880f0... Added tkinter frames
    tk_window(data)


if __name__ == '__main__':
    main()

    




