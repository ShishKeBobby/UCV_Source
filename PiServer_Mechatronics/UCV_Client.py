#UCV_Client code

import socket
from tkinter import *
import tkinter.messagebox
import threading
import time
import pygame
import csv

top = Tk()
top.config(bg="gray")

width, height = top.winfo_screenwidth(), top.winfo_screenheight()
top.geometry('%dx%d+0+0' % (width,height))

top.title("Unmanned Companion Vehicle(UCV)")
top.configure(bg="gold")


class Looping(object):
    def __init__(self):

        self.header1 = Label(top, text="Unmanned Companion Vehicle(UCV) Base Station",font="Cambria 26 bold", bg="gold", fg="red", borderwidth=5)
        self.header1.grid(sticky=E + W)
        self.header1.place(anchor="c", relx=.5, rely=.4)
        self.start_button = Button(top, text="START",font="Cambria 16",command=self.getthread1)
        self.start_button.place(anchor="c", relx=.5, rely=.5)

        self.isRunning = True
        self.manual = False
        self.v = 0

        # for file saving
        self.timestr = time.strftime("%Y_%m_%d-%H_%M_%S")

        myData=[["MPosLat", "MPosLon", "SPosLat", "SPosLon", "Heading", "MHeading", "SHeading", "ImgDist", "RStick", "LStick"]]
        myFile = open("UCV_log_" + self.timestr + ".csv", 'a', newline='')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(myData)



    def getthread1(self):
        # for threading
        l.isRunning = True
        t = threading.Thread(target=l.connection)
        t.start()


    def radio(self):

        self.v = v.get()
        self.check_label.configure(text="User override: Manual mode ")

        if self.v == 1:
            testWrite = writeClient()
            testWrite.setMessage("setUserOverride", "1")
            print("sent user override 1")
            pygame.init()

            # Initialize the joysticks
            pygame.joystick.init()
            # Game Loop
            done = False

            if self.v == 1:
                # while done==False:

                # Event processing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

                # Get count of joysticks
                joystick_count = pygame.joystick.get_count()

                # For each joystick:
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()

                    # Get the name from the OS for the controller/joystick
                    # name = joystick.get_name()
                    # Usually axis run in pairs, up/down for one, and left/right for the other.
                    axes = joystick.get_numaxes()
                    self.check_label.configure(text="User override:manual mode ")

                    print("getting joystick values")
                    axis1 = joystick.get_axis(1)
                    axis3 = joystick.get_axis(3)
                    print(axis1, axis3)
                    print("printing axes")
                    testWrite.setMessage('setLStick', str(axis1))
                    testWrite.setMessage('setRStick', str(axis3))
                    # self.getvalues()

                    top.after(100, lambda: self.radio())

                    # pygame.quit()

        if self.v == 2:
            pygame.quit()
            pygame.joystick.init()
            axis3 = 0
            axis0 = 0
            self.check_label.configure(text="Auto Mode ")
            testWrite = writeClient()
            testWrite.setMessage("setUserOverride", "0")
            print("sent user override 0")

    def connection(self):
        try:
            header = Label(top, text="Unmanned Companion Vehicle Base Station", font="Cambria 26 bold underline",
                           bg="gold", fg="red", borderwidth=5)
            header.grid(sticky=E + W)
            header.place(anchor="c", relx=.5, rely=.05)
            self.header1.destroy()
            self.start_button.destroy()


            # GPS coordinates
            coordframe = Frame(top, borderwidth=5, relief='groove')
            coordframe.place(relx=.2, rely=.4)
            gps_mlabel = Label(coordframe, text='MASTER COORDINATES', font="Cambria 16 underline bold")
            gps_mlabel.grid(columnspan=2)
            m_lat_name = Label(coordframe, text="Latitude            :",font="10")
            m_lat_name.grid(row=1, column=0, sticky="W")
            self.m_lat = Label(coordframe)
            self.m_lat.grid(row=1, column=1, sticky="W")
            m_lon_name = Label(coordframe, text="Longitude         :",font="10")
            m_lon_name.grid(row=2, column=0, sticky="W")
            self.m_lon = Label(coordframe)
            self.m_lon.grid(row=2, column=1,sticky="W")
            ucvlabel = Label(coordframe, text='UCV COORDINATES', font="Cambria 16 underline bold")
            ucvlabel.grid(columnspan=2)
            s_lat_name = Label(coordframe, text="Latitude            :",font="10")
            s_lat_name.grid(row=4, column=0, sticky="W")
            self.s_lat = Label(coordframe)
            self.s_lat.grid(row=4, column=1, sticky="W")
            s_lon_name = Label(coordframe, text="Longitude         :",font="10")
            s_lon_name.grid(row=5, column=0, sticky="W")
            self.s_lon = Label(coordframe)
            self.s_lon.grid(row=5, column=1,sticky="W")
            self.check_label = Label(top,font="Cambria 16 bold",fg="red")
            #self.check_label.pack(side=TOP)
            self.check_label.place(anchor="c", relx=.5, rely=.1)

            # UCV Directions
            stickFrame = Frame(top, borderwidth=5, relief='groove')
            stickFrame.place(relx=.8, rely=.4)
            stickLabel = Label(stickFrame, text="UCV DIRECTION",font="Cambria 16 underline bold")
            stickLabel.grid(columnspan=2, sticky="EW")
            RstickLabel = Label(stickFrame, text="Right: ",font="10")
            RstickLabel.grid(row=1, column=0, sticky="W")
            self.Rstick = Label(stickFrame, text=" ")
            self.Rstick.grid(row=1, column=1, sticky="W")
            LstickLabel = Label(stickFrame, text="Left: ",font="10")
            LstickLabel.grid(row=2, column=0, sticky="W")
            self.Lstick = Label(stickFrame, text="")
            self.Lstick.grid(row=2, column=1, sticky="W")

            # Headings
            headingFrame = Frame(top, borderwidth=5, relief='groove')
            headingFrame.place(relx=.4, rely=.4)
            hLabel = Label(headingFrame, text="HEADINGS",font="Cambria 16 underline bold")
            hLabel.grid(columnspan=2, sticky="EW")
            StoM = Label(headingFrame, text="From Slave to Master                      :",font="10")
            StoM.grid(row=1, column=0, sticky='W')
            self.StoM_value = Label(headingFrame, text=" ")
            self.StoM_value.grid(row=1, column=2, sticky='W')
            S_N = Label(headingFrame, text="Slave heading from North                 :",font="10")
            S_N.grid(row=2, column=0, sticky='W')
            self.S_N_value = Label(headingFrame, text="  ")
            self.S_N_value.grid(row=2, column=2, sticky='W')
            M_N = Label(headingFrame, text="Master heading from North               :",font="10")
            M_N.grid(row=3, column=0, sticky='W')
            self.M_N_value = Label(headingFrame, text="    ")
            self.M_N_value.grid(row=3, column=2, sticky='W')
            img_dist = Label(headingFrame, text="Image Processing distance(meters)  :",font="10")
            img_dist.grid(row=4, column=0, sticky='W')
            self.img_distance = Label(headingFrame, text="  ")
            self.img_distance.grid(row=4, column=2, sticky='W')
            img_heading = Label(headingFrame, text="Image Processing heading(pixels)     :",font="10")
            img_heading.grid(row=5, column=0, sticky='W')
            self.img_head = Label(headingFrame, text=" ")
            self.img_head.grid(row=5, column=2, sticky='W')

            # Radiobuttons
            sideFrame = Frame(top, borderwidth=5, relief="groove")  # creating a frame at the side
            sideFrame.place(relx=.42, rely=.15)  # placing in a desired position in the window, no need to pack
            global v
            v = IntVar()
            radio_label = Label(sideFrame, text="Select the mode",font="Cambria 16 underline bold")
            radio_label.grid(columnspan=2)
            manualRadiobutton = Radiobutton(sideFrame, text="Manual control mode",font="10", variable=v, value=1,
                                            command=self.radio)
            autoRadiobutton = Radiobutton(sideFrame, text="Auto control mode     ",font="10", variable=v, value=2,
                                          command=self.radio)

            manualRadiobutton.grid(columnspan=2)  # arranging the radio buttons in grid form
            autoRadiobutton.grid(columnspan=2)  # sticky means placing on West or East or North or South
            self.check_label.configure(text="Select the mode")  # Selection

            while True:

                self.getvalues()

        except ConnectionRefusedError:
            tkinter.messagebox.showinfo("Server is not active              ")
            tkinter.messagebox.showinfo("Closing the window.Try again                 ")
            top.quit()
        return ()

    def getvalues(self):
        myClient = readClient()

        myClient.readData("getMPosLat")
        MPosLat =myClient.data
        self.m_lat.configure(text=MPosLat)

        myClient.readData("getMPosLon")
        MPosLon =myClient.data
        self.m_lon.configure(text=MPosLon)

        myClient.readData('getSPosLat')
        SPosLat =myClient.data
        self.s_lat.configure(text=SPosLat)

        myClient.readData('getSPosLon')
        SPosLon = myClient.data
        self.s_lon.configure(text=SPosLon)

        # getting heading

        myClient.readData('getHeading')
        Heading = myClient.data
        self.StoM_value.configure(text=Heading)

        myClient.readData('getMHeading')
        MHeading=myClient.data
        self.S_N_value.configure(text=MHeading)

        myClient.readData('getSHeading')
        SHeading = myClient.data
        self.M_N_value.configure(text=SHeading)

        myClient.readData('getImgDist')
        imgdata = myClient.data
        data1 = imgdata.split(",")
        print(data1)
        ImgDist = data1[0]
        ImgHead = data1[1]
        self.img_distance.configure(text=ImgDist)

        # myClient.readData('getImgHeading')
        # ImgHead = myClient.data
        self.img_head.configure(text=ImgHead)

        # getting displaying and saving Right and Left stick values
        myClient.readData('getRStick')
        RStick =myClient.data
        self.Rstick.configure(text=RStick)

        myClient.readData('getLStick')
        LStick =myClient.data
        self.Lstick.configure(text=LStick)


        myData=[[MPosLat,MPosLon,SPosLat,SPosLon,Heading,MHeading,SHeading,ImgDist,RStick,LStick]]
        myFile = open("UCV_log" + self.timestr + "_.csv", 'a',newline='')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(myData)


class readClient:
    def readData(self, command):
        host = '192.168.0.102'
        port = 9080  # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        s.sendto(command.encode(), (host, port))
        self.data = s.recv(1024).decode()
        s.close()
        return self.data


class writeClient:
    def setMessage(self, command, message):
        # host = socket.gethostname()
        host = '192.168.0.102'
        port = 9080
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        # send command to set appropriate if else condition
        s.sendto(command.encode(), (host, port))
        time.sleep(.1)
        s.sendto(message.encode(), (host, port))
        s.close()


l = Looping()

top.mainloop()

