import ipinfo
from forecastiopy import *
from datetime import datetime, timedelta
import tkinter as tk

#ipinfo initialization and finding current latitude & longitude
ipinfo_access_token = 'bb7867c9bfe0b1'
handler = ipinfo.getHandler(ipinfo_access_token)
details = handler.getDetails()
lat = details.latitude
long = details.longitude
loc_city = details.city
#Forcast.io initialization
API_KEY_FORCASTIO = "4444fd1464bb71f413ee76e4267a74cb"
fio = ForecastIO.ForecastIO(API_KEY_FORCASTIO,units=ForecastIO.ForecastIO.UNITS_US,lang=ForecastIO.ForecastIO.LANG_ENGLISH,latitude=lat,longitude=long)
currently = FIOCurrently.FIOCurrently(fio)
hourly = FIOHourly.FIOHourly(fio)
daily = FIODaily.FIODaily(fio)
minutely = FIOMinutely.FIOMinutely(fio)
calls = int(fio.x_forecast_api_calls)
#time from forcastio in unix and datetime
ut = currently.time
unix_time = ('unix time:', ut)
date_time = str(datetime.fromtimestamp(ut).strftime('%Y-%m-%d %I:%M:%S'))
print(date_time)
print(currently.summary)
END = tk.END
INSERT = tk.INSERT
#api cutoff
while calls > 1000:
    print("Too many API calls today, please check back tommorow")
    break
#functions/classes for tkinter
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        
class Summary(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Summary",width='1000',height='1')
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,"Currently: "+str(minutely.summary)+"\nTemperature: "+str(currently.temperature)+"°F"+"\nFeels like: "+str(currently.apparentTemperature)+"°F"+"\nHumidity: "+str(format(currently.humidity,'.0%'))+"\nToday: "+str(hourly.summary)+"\nTomorrow: "+str(daily.summary))
       label.pack(side='top', fill='x')
       textbox.pack(side='left')

class Minutely(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Minutely Information")
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'This tab is a work in progress and will be fleshed out in future commits to the repository')
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')

class Hourly(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Hourly Information")
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'This tab is a work in progress and will be fleshed out in future commits to the repository')
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')

class Daily(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Daily Information")
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'This tab is a work in progress and will be fleshed out in future commits to the repository')
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')
       
class Alerts(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        if fio.has_alerts() == 'True':
            print("Need to write the code for this")
        else:
            no_alerts = tk.Label(self, text="No alerts to display")
            no_alerts.pack(side="top", fill="both", expand=True)
           
class search_local(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 1")
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'This tab is a work in progress and will be fleshed out in future commits to the repository\nThe plan is for it to contain a way to search for a location and access the weather data of that location')
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')
#tkinter window
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Summary(self)
        p2 = Minutely(self)
        p3 = Hourly(self)
        p4 = Daily(self)
        p5 = Alerts(self)
        p6 = search_local(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        

        b1 = tk.Button(buttonframe, text="Summary", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Minutely", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Hourly", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Daily", command=p4.lift)
        b5 = tk.Button(buttonframe, text="Alerts", command=p5.lift)
        b6 = tk.Button(buttonframe, text="Search", command=p6.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
        b6.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
            
