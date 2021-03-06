import ipinfo
from forecastiopy import *
from datetime import datetime, timedelta
import tkinter as tk
from geopy import geocoders
from geopy.geocoders import GoogleV3
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
print(lat,",",long)
END = tk.END
INSERT = tk.INSERT
def hourly_time(time):
    date_time = str(datetime.fromtimestamp(time).strftime('%I %p'))
    return date_time.lstrip('0')
#api cutoff
while calls > 1000:
    print("Too many API calls today, please check back tommorow")
    break
#Wind bearing to direction
class Wind():
    def current():
        windbearing = currently.windBearing
        if windbearing == 0 or windbearing == 360:
            windbearing = "North"
        elif windbearing == 90:
            windbearing = "East"
        elif windbearing == 180:
            windbearing = "South"
        elif windbearing == 270:
            windbearing = "West"
        elif 0 < windbearing < 90:
            windbearing = "Northeast"
        elif 90 < windbearing < 180:
            windbearing = "Southeast"
        elif 190 < windbearing < 270:
            windbearing = "Southwest"
        else:
            windbearing = "NorthWest"
        return windbearing
    def hourly(data):
        windbearing = data[13][1]
        if windbearing == 0 or windbearing == 360:
            windbearing = "North"
        elif windbearing == 90:
            windbearing = "East"
        elif windbearing == 180:
            windbearing = "South"
        elif windbearing == 270:
            windbearing = "West"
        elif 0 < windbearing < 90:
            windbearing = "Northeast"
        elif 90 < windbearing < 180:
            windbearing = "Southeast"
        elif 190 < windbearing < 270:
            windbearing = "Southwest"
        else:
            windbearing = "NorthWest"
        return windbearing
#Nearest storm bearing to direction
class nearest_storm():
    def current():
        try: 
            stormbearing = currently.nearestStormBearing
            if stormbearing == 0 or stormbearing == 360:
                stormbearing = "North of your current location"
            elif stormbearing == 90:
                stormbearing = "East of your current location"
            elif stormbearing == 180:
                stormbearing = "South of your current location"
            elif stormbearing == 270:
                stormbearing = "West of your current location"
            elif 0 < stormbearing < 90:
                stormbearing = "Northeast of your current location"
            elif 90 < stormbearing < 180:
                stormbearing = "Southeast of your current location"
            elif 190 < stormbearing < 270:
                stormbearing = "Southwest of your current location"
            else:
                stormbearing = "NorthWest of your current location"
            return str(currently.nearestStormDistance)+" Miles "+stormbearing
        except NameError:
            return str(currently.nearestStormDistance)+" miles from your current location"
#Location+search
def location_search(loc):
    geolocator = GoogleV3(api_key="AIzaSyCWvcKQMAFSZCMw1Fll5Dz_bmh90KAoUYs")
    try:
        location = geolocator.geocode(loc,timeout=10)
        location = [location.latitude, location.longitude]
        return location
    except AttributeError:
        print("problem with data")
    
    return location
#weather data accessors
def summary_data():
    return ("Currently: "+str(minutely.summary)+
           "\nTemperature: "+str(currently.temperature)+"°F"+
           "\nFeels Like: "+str(currently.apparentTemperature)+"°F"+
           "\nChance of Rain: "+str(format(currently.precipProbability*100,'.0%'))+
           "\nHumidity: "+str(format(currently.humidity,'.0%'))+
           "\nWind Speed: "+str(currently.windSpeed)+"mph"+
           "\nWind Direction: "+Wind.current()+
           "\nNearest Storm: "+nearest_storm.current()+
           "\nToday: "+str(hourly.summary)+
           "\nThis Week: "+str(daily.summary))
def hourly_data(textbox):
    data = [i for i in hourly.data]
    
    for num in range(0,len(hourly.data)):
        data2 = [i for i in data[num].items()]
        time = hourly_time(int(data2[0][1]))
        print(time)
        if time == '12 AM':
            textbox.insert(tk.END, '----------------------New Day----------------------'+
                           '\n\nWeather for '+str(time)+
                           '\nSummary: '+str(data2[1][1])+
                           '\nTemperature: '+str(data2[6][1])+
                           '\nFeels Like: '+str(data2[7][1])+
                           '\nChance of Rain: '+str(int(data2[4][1])*100)+
                           '\nHumidity: '+str(data2[9][1])+
                           '\nWind Speed: '+str(data2[11][1])+'mph'+
                           "\nWind Direction: "+Wind.hourly(data2)+'\n\n')
        else:
            textbox.insert(tk.END,'Weather for '+str(time)+
                           '\nSummary: '+str(data2[1][1])+
                           '\nTemperature: '+str(data2[6][1])+
                           '\nFeels Like: '+str(data2[7][1])+
                           '\nChance of Rain: '+str(int(data2[4][1])*100)+
                           '\nHumidity: '+str(data2[9][1])+
                           '\nWind Speed: '+str(data2[11][1])+'mph'+
                           "\nWind Direction: "+Wind.hourly(data2)+'\n\n')
                       
    
#functions/classes for tkinter
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        
class Summary(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Summary for "+loc_city,width='1000',height='1')
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,summary_data())
       label.pack(side='top', fill='x')
       textbox.pack(side='left')

class Minutely(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Minutely Information for "+loc_city)
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'This tab is a work in progress and will be fleshed out in future commits to the repository')
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')

class Hourly(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Hourly Information for "+loc_city)
       textbox = tk.Text(self, width='1000',height='20')
       hourly_data(textbox)
       label.pack(side="top", fill="both", expand=True)
       textbox.pack(side='left')

class Daily(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Daily Information for "+loc_city)
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
       #label = tk.Label(self, text="Search")
       textbox = tk.Text(self, width='1000',height='20')
       textbox.insert(tk.END,'Type in name of city and press search')
       e = tk.Entry(self, width='17')
       e.pack()
       e.focus_set()
      # def search():
        #   location = location_search(e.get())
       #b = tk.Button(self, text="search", width='17',command=search())
       #b.pack()
       #label.pack(side="top", fill="both", expand=True)
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
    root.title("Weather App")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("500x390")
    root.mainloop()
            
