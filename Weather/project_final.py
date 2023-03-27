import requests
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from geonamescache import GeonamesCache
from dotenv import load_dotenv
import os

load_dotenv()

# create an instance of the GeonamesCache class
gc = GeonamesCache()

# get a dictionary of all cities in the world
cities = gc.get_cities()

def get_weather(city_name):
    api_key = os.getenv('API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    data = response.json()

    if data["cod"] != "404":
        weather = data["main"]
        temperature = weather["temp"]
        humidity = weather["humidity"]
        pressure = weather["pressure"]
        report = data["weather"][0]["description"]
        icon_name = data["weather"][0]["icon"]
        return temperature, humidity, pressure, report, icon_name
    else:
        return None

def update_weather():
    city_name = city_var.get()
    result = get_weather(city_name)
    if result is not None:
        temperature, humidity, pressure, report, icon_name = result
        temperature_label.config(text=f"Temperature: {((temperature)- 273.15):.2f} °C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        report_label.config(text=f"Report: {report}")
        icon_path = f"icons/{icon_name}.png"
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        icon_label.config(image=icon_image)
        icon_label.image = icon_image  # keep a reference to prevent garbage collection
    else:
        temperature_label.config(text="City not found")
        humidity_label.config(text="")
        pressure_label.config(text="")
        report_label.config(text="")
        icon_label.config(image="")

# Create the main window
window = tk.Tk()
window.title("Weather App")

# Add a label widget
label = tk.Label(window, text="Select a city:")
label.pack()

# Add a dropdown list widget
cities_names = sorted([city['name'] for city in cities.values()])
city_var = tk.StringVar()
city_dropdown = ttk.Combobox(window, textvariable=city_var, values=cities_names)
city_dropdown.pack()
city_dropdown.current(0)

# Add a button widget
button = tk.Button(window, text="Get Weather", command=update_weather)
button.pack()

# Add weather information labels
temperature_label = tk.Label(window ,background='#D3D3D3', text="")
temperature_label.pack()
humidity_label = tk.Label(window ,background='#D3D3D3', text="")
humidity_label.pack()
pressure_label = tk.Label(window ,background='#D3D3D3', text="")
pressure_label.pack()
report_label = tk.Label(window ,background='#D3D3D3', text="")
report_label.pack()

# Add weather icon
icon_label = tk.Label(window,background='#D3D3D3', image="")
icon_label.pack()

# Start the main event loop
window.configure(bg='#D3D3D3')
window.geometry("400x400")
window.mainloop()
