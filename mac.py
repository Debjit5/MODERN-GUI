from tkinter import *
from tkinter import ttk,messagebox,filedialog
import tkinter as tk
import platform
import psutil

#Brightness
import screen_brightness_control as pct

#Audio
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

#Weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

#Clock
from time import strftime

#Calender
from tkcalendar import *

#Google
import pyautogui

import subprocess
import webbrowser as wb
import random

root=Tk()
root.title("Modern GUI")
root.geometry("850x500+300+170")
root.resizable(False,False)
root.config(bg="#292e2e")

#icon
image_icon=PhotoImage(file="Image/icon.png")
root.iconphoto(False,image_icon)

#Body Frame
body=Frame(root,width=900,height=600,bg="#d6d6d6")
body.pack(padx=20,pady=20)

#Left Frame
lhs=Frame(body,width=310,height=435,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
lhs.place(x=10,y=10)

#logo
photo=PhotoImage(file="Image/laptop.png")
myimage=Label(lhs,image=photo,background="#f4f5f5")
myimage.place(x=2,y=20)

my_system=platform.uname()

l1=Label(lhs,text=my_system.node,bg="#f4f5f5",font=("Acumin Variable Concept",14,'bold'),justify='center')
l1.place(x=20,y=200)

l2=Label(lhs,text=f"Version:{my_system.version}",bg="#f4f5f5",font=("Acumin Variable Concept",7,),justify='center')
l2.place(x=20,y=225)

l3=Label(lhs,text=f"System:{my_system.system}",bg="#f4f5f5",font=("Acumin Variable Concept",14,),justify='center')
l3.place(x=20,y=250)

l4=Label(lhs,text=f"Machine:{my_system.machine}",bg="#f4f5f5",font=("Acumin Variable Concept",14,),justify='center')
l4.place(x=20,y=285)

l5=Label(lhs,text=f"Ram Installed:{round(psutil.virtual_memory().total/1000000000,2)} GB",bg="#f4f5f5",font=("Acumin Variable Concept",15,),justify='center')
l5.place(x=20,y=320)

l6=Label(lhs,text=f"Processor:{my_system.processor}",bg="#f4f5f5",font=("Acumin Variable Concept",5),justify='center')
l6.place(x=20,y=350)



#Right Top Frame
rhs=Frame(body,width=470,height=230,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
rhs.place(x=330,y=10)

system=Label(rhs,text='System',font=("Acumin Variable Concept",15),bg='#f4f5f5')
system.place(x=10,y=10)

#Battery

def convertTime(seconds):
    minutes,seconds=divmod(seconds,60)
    hours,minutes=divmod(minutes,60)
    return "%d:%02d:%02d"% (hours,minutes,seconds)
def none():
    global battery_png
    global battery_label
    battery=psutil.sensors_battery()
    percent=battery.percent
    time=convertTime(battery.secsleft)

    lbl.config(text=f"{percent}%")
    lbl_plug.config(text=f'Plug in:{str(battery.power_plugged)}')
    lbl_time.config(text=f'{time} remaining')

    battery_label=Label(rhs,background="#f4f5f5")
    battery_label.place(x=15,y=50)

    lbl.after(1000,none)

    if battery.power_plugged==True:
        battery_png=PhotoImage(file="Image/charging.png")
        battery_label.config(image=battery_png)
    else:
        battery_png=PhotoImage(file="Image/battery.png")
        battery_label.config(image=battery_png)

lbl=Label(rhs,font=("Acumin Variable Concept",36,'bold'),bg='#f4f5f5')
lbl.place(x=200,y=30)

lbl_plug=Label(rhs,font=("Acumin Variable Concept",10),bg="#f4f5f5")
lbl_plug.place(x=20,y=100)

lbl_time=Label(rhs,font=("Acumin Variable Concept",15),bg="#f4f5f5")
lbl_time.place(x=200,y=100)

none()

#Speaker

lbl_speaker=Label(rhs,text="Speaker",font=('arial',10,'bold'),bg="#f4f5f5")
lbl_speaker.place(x=10,y=150)
volumn_value=tk.DoubleVar()

def get_current_volumn_value():
    return '{: .2f}'.format(volumn_value.get())
def volumn_changed(event):
    device=AudioUtilities.GetSpeakers()
    interface=device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volumn=cast(interface,POINTER(IAudioEndpointVolume))
    volumn.SetMasterVolumeLevel(-float(get_current_volumn_value()),None)


style=ttk.Style()
style.configure("TScale")

volumn=ttk.Scale(rhs,from_=60,to=0,orient='horizontal',command=volumn_changed,variable=volumn_value)
volumn.place(x=90,y=150)
volumn.set(20)

#Brightness
lbl_brightness=Label(rhs,text="Brightness",font=('arial',10,'bold'),bg="#f4f5f5")
lbl_brightness.place(x=10,y=190)

current_value=tk.DoubleVar()

def get_current_value():
    return '{: .2f}'.format(current_value.get())
def brightness_changed(event):
    pct.set_brightness(get_current_value())

brightness=ttk.Scale(rhs,from_=0,to=100,orient='horizontal',command=brightness_changed,variable=current_value)
brightness.place(x=90,y=190)


#Right Bottom Frame
rhb=Frame(body,width=470,height=190,bg="#f4f5f5",highlightbackground="#adacb1",highlightthickness=1)
rhb.place(x=330,y=255)

#App func()

def weather():
    app1=Toplevel()
    app1.geometry('850x500+300+170')
    app1.title('Weather')
    app1.configure(bg='#f4f5f5')
    app1.resizable(False,False)

    ##icon
    image_icon=PhotoImage(file='Image/App1.png')
    app1.iconphoto(False,image_icon)

    def getweather():
        try:
            city=textfield.get()

            geolocator=Nominatim(user_agent="geoapiExercises")
            location=geolocator.geocode(city)
            obj=TimezoneFinder()
            result=obj.timezone_at(lng=location.longitude,lat=location.latitude)

            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I:%M:%p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")

            ###weather api
            api= "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=646824f2b7b86caffec1d0b16ea77f79"

            json_data=requests.get(api).json()
            condition=json_data['weather'][0]['main']
            description=json_data['weather'][0]['description']
            temp=int(json_data['main']['temp']-273.15)
            pressure=json_data['main']['pressure']
            humidity=json_data['main']['humidity']
            wind=json_data['wind']['speed']

            t.config(text=(temp,"°"))
            c.config(text=(condition,"|","FEELS","LIKE",temp,"°"))

            w.config(text=wind)
            h.config(text=humidity)
            d.config(text=description)
            p.config(text=pressure)

        except Exception as e:
            messagebox.showerror("Weather App","Invalid Entry!")

    ##search box
    Search_image=PhotoImage(file="Image/search.png")
    myimage=Label(app1,image=Search_image,bg='#f4f5f5')
    myimage.place(x=20,y=20)

    textfield=tk.Entry(app1,justify='center',width=17,font=('poppins',25,'bold'),bg='#404040',border=0,fg='white')
    textfield.place(x=50,y=36)
    textfield.focus()
    
    Search_icon=PhotoImage(file='Image/search_icon.png')
    myimage_icon=Button(app1,image=Search_icon,borderwidth=0,cursor='hand2',bg='#404040',command=getweather)
    myimage_icon.place(x=400,y=34)

    #logo
    Logo_image=PhotoImage(file='Image/logo.png')
    Logo=Label(app1,image=Logo_image,bg="#f4f5f5")
    Logo.place(x=150,y=100)

    #bottom box
    Frame_image=PhotoImage(file="Image/box.png")
    frame_myimage=Label(app1,image=Frame_image,bg="#f4f5f5")
    frame_myimage.pack(padx=5,pady=5,side='bottom')

    #time
    name=Label(app1,font=('arial',10,'bold'),bg="#f4f5f5")
    name.place(x=30,y=100)
    clock=Label(app1,font=('Helvetica',16),bg="#f4f5f5")
    clock.place(x=30,y=130)

    #label
    label1=Label(app1,text="WIND",font=("Helvatica",15,"bold"),fg="white",bg="#1ab5ef")
    label1.place(x=120,y=400)

    label2=Label(app1,text="HUMIDITY",font=("Helvatica",15,"bold"),fg="white",bg="#1ab5ef")
    label2.place(x=250,y=400)

    label3=Label(app1,text="DESCRIPTION",font=("Helvatica",15,"bold"),fg="white",bg="#1ab5ef")
    label3.place(x=430,y=400)

    label4=Label(app1,text="PRESSURE",font=("Helvatica",15,"bold"),fg="white",bg="#1ab5ef")
    label4.place(x=650,y=400)

    t=Label(app1,font=('arial',64,'bold'),fg="#ee666d",bg="#f4f5f5")
    t.place(x=400,y=150)
    c=Label(app1,font=('arial',15,'bold'),bg='#f4f5f5')
    c.place(x=400,y=260)

    w=Label(app1,text="...",font=('arial',16,'bold'),bg="#1ab5ef")
    w.place(x=120,y=430)
    h=Label(app1,text="...",font=('arial',16,'bold'),bg="#1ab5ef")
    h.place(x=280,y=430)
    d=Label(app1,text="...",font=('arial',16,'bold'),bg="#1ab5ef")
    d.place(x=450,y=430)
    p=Label(app1,text="...",font=('arial',16,'bold'),bg="#1ab5ef")
    p.place(x=670,y=430)



    app1.mainloop()

def clock():
    app2=Toplevel()
    app2.geometry("850x110+300+10")
    app2.title('Clock')
    app2.configure(bg="#292e2e")
    app2.resizable(False,False)

    ##icon
    image_icon=PhotoImage(file="Image/App2.png")
    app2.iconphoto(False,image_icon)

    def clk():
        text=strftime('%H:%M:%S %p')
        lbl.config(text=text)
        lbl.after(1000,clk)
    
    lbl=Label(app2,font=('digital-7',50,'bold'),width=20,bg="#f4f5f5",fg="#292e2e")
    lbl.pack(anchor="center",pady=20)
    clk()

    app2.mainloop()

def calender():
    app3=Toplevel()
    app3.geometry("300x300+10+10")
    app3.title('Calender')
    app3.config(bg="#292e2e")
    app3.resizable(False,False)

    ##icon
    image_icon=PhotoImage(file="Image/App3.png")
    app3.iconphoto(False,image_icon)

    mycal=Calendar(app3,setmode='day',date_pattern='d/m/yy')
    mycal.pack(padx=15,pady=35)

    app3.mainloop()

##mode#####
button_mode=True

def mode():
    global button_mode

    if button_mode:
        lhs.config(bg="#292e2e")
        myimage.config(bg="#292e2e")
        l1.config(bg="#292e2e",fg="#d6d6d6")
        l2.config(bg="#292e2e",fg="#d6d6d6")
        l3.config(bg="#292e2e",fg="#d6d6d6")
        l4.config(bg="#292e2e",fg="#d6d6d6")
        l5.config(bg="#292e2e",fg="#d6d6d6")
        l6.config(bg="#292e2e",fg="#d6d6d6")

        rhb.config(bg="#292e2e")
        app1.config(bg="#292e2e")
        app2.config(bg="#292e2e")
        app3.config(bg="#292e2e")
        app4.config(bg="#292e2e")
        app5.config(bg="#292e2e")
        app6.config(bg="#292e2e")
        app7.config(bg="#292e2e")
        app8.config(bg="#292e2e")
        app9.config(bg="#292e2e")
        app10.config(bg="#292e2e")
        apps.config(bg="#292e2e",fg="#d6d6d6")

        button_mode=False

    else:
        lhs.config(bg="#f4f5f5")
        myimage.config(bg="#f4f5f5")
        l1.config(bg="#f4f5f5",fg="#292e2e")
        l2.config(bg="#f4f5f5",fg="#292e2e")
        l3.config(bg="#f4f5f5",fg="#292e2e")
        l4.config(bg="#f4f5f5",fg="#292e2e")
        l5.config(bg="#f4f5f5",fg="#292e2e")
        l6.config(bg="#f4f5f5",fg="#292e2e")

        rhb.config(bg="#f4f5f5")
        app1.config(bg="#f4f5f5")
        app2.config(bg="#f4f5f5")
        app3.config(bg="#f4f5f5")
        app4.config(bg="#f4f5f5")
        app5.config(bg="#f4f5f5")
        app6.config(bg="#f4f5f5")
        app7.config(bg="#f4f5f5")
        app8.config(bg="#f4f5f5")
        app9.config(bg="#f4f5f5")
        app10.config(bg="#f4f5f5")
        apps.config(bg="#f4f5f5",fg="#292e2e")

        button_mode=True

#Game

def game():
    app5=Toplevel()
    app5.geometry("300x500+1170+170")
    app5.title("Ludo")
    app5.config(bg="#dee2e5")
    app5.resizable(False,False)

    ##icon
    image_icon=PhotoImage(file="Image/App5.png")
    app5.iconphoto(False,image_icon)

    ludo_img=PhotoImage(file="Image/ludo back.png")
    Label(app5,image=ludo_img).pack()

    label=Label(app5,text='',font=("times",130))
    
    def roll():
        dice=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
        label.configure(text=f'{random.choice(dice)}{random.choice(dice)}',fg="#29232e")
        label.pack()

    btn_image=PhotoImage(file="Image/ludo button.png")
    btn=Button(app5,image=btn_image,bg="#dee2e5",command=roll)
    btn.pack(padx=10,pady=10)

    app5.mainloop()

#ScreenShort

def screenshort():
    root.iconify()

    myscreenshort=pyautogui.screenshot()
    file_path=filedialog.asksaveasfilename(defaultextension='.png')
    myscreenshort.save(file_path)

#file Opening

def file():
    subprocess.Popen(r'explorer /select,"C:\Users\USER\Desktop\Tkinter Learning\Projects\Modern GUI"')

#Browser
def crome():
    wb.register('crome',None)
    wb.open('https://www.google.com/')

#Close Window

def close_windows():
    root.destroy()

def close_apps():
    pass

#App Buttons
apps=Label(rhb,text="Apps",font=('Acumin Variable Concept',15),bg='#f4f5f5')
apps.place(x=10,y=10)

app1_image=PhotoImage(file='Image/App1.png')
app1=Button(rhb,image=app1_image,bd=0,command=weather)
app1.place(x=15,y=50)

app2_image=PhotoImage(file='Image/App2.png')
app2=Button(rhb,image=app2_image,bd=0,command=clock)
app2.place(x=100,y=50)

app3_image=PhotoImage(file='Image/App3.png')
app3=Button(rhb,image=app3_image,bd=0,command=calender)
app3.place(x=185,y=50)

app4_image=PhotoImage(file='Image/App4.png')
app4=Button(rhb,image=app4_image,bd=0,command=mode)
app4.place(x=270,y=50)

app5_image=PhotoImage(file='Image/App5.png')
app5=Button(rhb,image=app5_image,bd=0,command=game)
app5.place(x=355,y=50)

app6_image=PhotoImage(file='Image/App6.png')
app6=Button(rhb,image=app6_image,bd=0,command=screenshort)
app6.place(x=15,y=120)

app7_image=PhotoImage(file='Image/App7.png')
app7=Button(rhb,image=app7_image,bd=0,command=file)
app7.place(x=100,y=120)

app8_image=PhotoImage(file='Image/App8.png')
app8=Button(rhb,image=app8_image,bd=0,command=crome)
app8.place(x=185,y=120)

app9_image=PhotoImage(file='Image/App9.png')
app9=Button(rhb,image=app9_image,bd=0,command=close_apps)
app9.place(x=270,y=120)

app10_image=PhotoImage(file='Image/App10.png')
app10=Button(rhb,image=app10_image,bd=0,command=close_windows)
app10.place(x=355,y=120)


root.mainloop()