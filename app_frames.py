import tkinter as tk
from Indian_states import state_name
from nameCorrection import name_correction
from states_data import merged


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        # scroll_bar = tk.Scrollbar(container) 
        # scroll_bar.pack( side = "right", fill = "y" )
        
        container.pack(side="top", fill="both", expand = True)
       
        
        
        menu = tk.Menu(self)
        self.config(menu=menu)

        # create the file object)
        file = tk.Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        print(state_name)
        file.add_command(label="Andaman and Nikobar Islands", command=lambda: self.show_frame(AN))
        file.add_command(label="Andhra Pradesh", command=lambda: self.show_frame(AP))
        file.add_command(label="Arunachal Pradesh", command=lambda: self.show_frame(AR))
        file.add_command(label="Assam", command=lambda: self.show_frame(AS))
        file.add_command(label="Bihar", command=lambda: self.show_frame(BR))
        file.add_command(label="Chandigarh", command=lambda: self.show_frame(CH))
        file.add_command(label="Chhattisgarh", command=lambda: self.show_frame(CT))
        file.add_command(label="Delhi", command=lambda: self.show_frame(DL))
        file.add_command(label="Dadra and Nagar Haveli and Daman and Diu", command=lambda: self.show_frame(DN))
        file.add_command(label="Goa", command=lambda: self.show_frame(GA))
        file.add_command(label="Gujarat", command=lambda: self.show_frame(GJ))
        file.add_command(label="Himachal Pradesh", command=lambda: self.show_frame(HP))
        file.add_command(label="Haryana", command=lambda: self.show_frame(HR))
        file.add_command(label="Jharkhand", command=lambda: self.show_frame(JH))
        file.add_command(label="Jammu and Kashmir", command=lambda: self.show_frame(JK))
        file.add_command(label="Karnataka", command=lambda: self.show_frame(KA))
        file.add_command(label="Kerala", command=lambda: self.show_frame(KL))
        file.add_command(label="Ladakh", command=lambda: self.show_frame(LA))
        file.add_command(label="Maharashtra", command=lambda: self.show_frame(MH))
        file.add_command(label="Meghalaya", command=lambda: self.show_frame(ML))
        file.add_command(label="Manipur", command=lambda: self.show_frame(MN))
        file.add_command(label="Madhya Pradesh", command=lambda: self.show_frame(MP))
        file.add_command(label="Mizoram", command=lambda: self.show_frame(MZ))
        file.add_command(label="Nagaland", command=lambda: self.show_frame(NL))
        file.add_command(label="Odisha", command=lambda: self.show_frame(OR))
        file.add_command(label="Punjab", command=lambda: self.show_frame(PB))
        file.add_command(label="Puducherry", command=lambda: self.show_frame(PY))
        file.add_command(label="Rajasthan", command=lambda: self.show_frame(RJ))
        file.add_command(label="Sikkim", command=lambda: self.show_frame(SK))
        file.add_command(label="Telangana", command=lambda: self.show_frame(TG))
        file.add_command(label="Tamil Nadu", command=lambda: self.show_frame(TN))
        file.add_command(label="Tripura", command=lambda: self.show_frame(TR))
        file.add_command(label="Uttar Pradesh", command=lambda: self.show_frame(UP))
        file.add_command(label="Uttarakhand", command=lambda: self.show_frame(UT))
        file.add_command(label="West Bengal", command=lambda: self.show_frame(WB))

 

#India(Total cases) TT





        #added "file" to our menu
        menu.add_cascade(label="Select State", menu=file)

        # create the file object)
        # edit = tk.Menu(menu)

        # # adds a command to the menu option, calling it exit, and the
        # # command it runs on event is client_exit
        # edit.add_command(label="30 mins")
        # edit.add_command(label="1 hr")
        # edit.add_command(label="3 hrs")
        # edit.add_command(label="8 hrs")
        # edit.add_command(label="12 hrs")
        # edit.add_command(label="24 hrs")

        # #added "file" to our menu
        # menu.add_cascade(label="Notify time", menu=edit)

    
    

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in(TT,MH, AP):
                
        # for F in (TT, AN, AP, AR, AS, BR, CH, CT, DL, DN, GA, GJ, HP, HR, 
        #           JH, JK, KA, KL, LA, MH, ML, MN, MP, MZ, NL, OR, PB, PY, RJ, SK,
        #           TG, TN, TR, UP, UT, WB):

            frame = F(container, self)

            self.frames[F] = frame
            #frame.pack(fill ="both")

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TT)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    def client_state(self):
            exit()

        
class TT(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="India", font=LARGE_FONT)
        label.grid(row = 0, column =0, ipadx =10, ipady=10)
        
        label = tk.Label(self, text="Confirmed cases"  + "\n", font=LARGE_FONT)
        label.grid(row = 2, column =0, ipadx =10, ipady=10)
                
        label = tk.Label(self, text="Recovered cases" +"\n", font=LARGE_FONT)
        label.grid(row = 4 , column = 0, ipadx =10, ipady=10)
                
        label = tk.Label(self, text="Death toll" + "\n", font=LARGE_FONT)
        label.grid(row = 6, column =0, ipadx =10, ipady=10)
        
        # label1 = tk.Label(self, text = "State\n")
        # label1.grid(row = 0, column=0)
        # label1 = tk.Label(self, text = "Confirmed cases\n")
        # label1.grid(row = 0, column=4)
        # label1 = tk.Label(self, text = "Recovered cases\n")
        # label1.grid(row = 0, column=8)
        # label1 = tk.Label(self, text = "Death toll\n")
        # label1.grid(row = 0, column=12)
                           
        # for i, index_st in enumerate(merged.index):
        #     globals()['label_{}'.format(i)] = tk.Label(self, text = index_st + "\n")
        #     globals()['label_{}'.format(i)].grid(row= i+1,column = 0 ,ipadx =70)
            
        # for i, conf_case in enumerate(merged['Confirmed cases']):
        #     globals()['label_C{}'.format(i)] = tk.Label(self, text = str(conf_case) + "\n")
        #     globals()['label_C{}'.format(i)].grid(row= i+1,column =4,ipadx = 70)
            
        # for i, conf_case in enumerate(merged['Recovered cases']):
        #     globals()['label_R{}'.format(i)] = tk.Label(self, text = str(conf_case) + "\n")
        #     globals()['label_R{}'.format(i)].grid(row= i+1,column =8,ipadx = 70)
        
        # for i, conf_case in enumerate(merged['Death toll']):
        #     globals()['label_D{}'.format(i)] = tk.Label(self, text = str(conf_case) + "\n")
        #     globals()['label_D{}'.format(i)].grid(row= i+1, column =12,ipadx = 70)
        for m,n,p,q in zip(merged.index, merged["Confirmed cases"], merged["Recovered cases"], merged["Death toll"]):
            if "India" in m:
                print(n, p,q)
                label = tk.Label(self, text= str(n) + "\n", font=LARGE_FONT)
                label.grid(row = 2, column =1, ipadx =10, ipady=10)
                
                label = tk.Label(self, text=str(p) +"\n", font=LARGE_FONT)
                label.grid(row = 4 , column = 1, ipadx =10, ipady=10)
                
                label = tk.Label(self, text=str(q) + "\n", font=LARGE_FONT)
                label.grid(row = 6, column =1, ipadx =10, ipady=10)
        
          




        # add scroll bar for state and city and duration

class MH(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(TT))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(AP))
        button2.pack()


class AP(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(TT))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(MH))
        button2.pack()


app = SeaofBTCapp()
app.mainloop()