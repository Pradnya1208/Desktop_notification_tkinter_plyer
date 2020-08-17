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
import datetime
import time
from bs4 import BeautifulSoup
import requests
import tkmain

filename = "covid.txt"


class Covid_tracker():
    def __init__(self, covid_d = ''):
        self.covid_d = covid_d


    def covid_parser(self, start_time):
        url = "https://www.worldometers.info/coronavirus/"
        Cases_world = []

        covid_world = requests.get(url)
        soup_world = BeautifulSoup(covid_world.content, 'html.parser')
        Cases_world += soup_world.find_all("div", class_="maincounter-number")

        self.covid_d = "Total Cases: " + (
            (str(Cases_world[0]).split(">")[2]).split("<")[0]) + "\n" + "Total Deaths : " + (
                      (str(Cases_world[1]).split(">")[2]).split("<")[0]) + "\n" + "Recovered : " + (
                      (str(Cases_world[2]).split(">")[2]).split("<")[0])

        f = open('covid.txt', 'w')
        f.write(start_time + "\n" + self.covid_d)
        f.close()

    def covid_textdata(self):
        i = 0
        with open(filename, 'r') as filehandle:
            for line in filehandle:
                if i == 0:
                    self.covid_d += ''
                else:
                    self.covid_d += line
                i += 1

    def data_refresh(self):
        refresh_time = '23:00:00'
        format = "%b %d %Y at %I:%M%p"
        start_time = datetime.datetime.now().strftime(format)

        with open(filename, "r") as file:
            first_line = file.readline()

        if first_line:
            date_time_str = first_line  # previous data loading time
            print("date_time_str" + date_time_str)
            date_time_str = date_time_str.replace("\n", '')

            end_time = datetime.datetime.strptime(date_time_str, format)
            print('start time:' + start_time)
            print('end time:' + str(end_time))

            total_time = datetime.datetime.strptime(start_time, format) - datetime.datetime.strptime(date_time_str, format)

            print(total_time)

            if total_time.days >= 1:
                print("Time to refresh.....")
                self.covid_parser(start_time)

            else:
                print("comparing hours....")

                if ',' in str(total_time):
                    t = (str(total_time).split(',')[1]).replace(' ', '')
                    t1 = datetime.datetime.strptime(t, '%H:%M:%S')
                    print(t)
                else:
                    t = str(total_time)
                    t1 = datetime.datetime.strptime(t, '%H:%M:%S')

                t2 = datetime.datetime.strptime(refresh_time, '%H:%M:%S')

                if t1.time() > t2.time():
                    print("Its time to refresh...")
                    self.covid_parser(start_time)
                else:
                    print("Hang in there....")
                    self.covid_textdata()
        else:
            self.covid_parser(start_time)
# print ((str(Cases_world[0]).split(">")[2]).split("<")[0])


covid= Covid_tracker()
covid.data_refresh()

