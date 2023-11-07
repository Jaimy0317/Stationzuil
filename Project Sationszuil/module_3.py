import tkinter as tk
from tkinter import ttk
import requests
import psycopg2

# Stations latitude and longitude data
station_data = {
    "Amsterdam": {"lat": "52.379189", "lon": "4.899431"},
    "Arnhem": {"lat": "51.9848863", "lon": "5.8990061"},
    "Nijmegen": {"lat": "51.843742", "lon": "5.8537626"}
}

# Function to fetch the data from the openweather API
def fetch_data(url):
    try:
        return requests.get(url).json()
    except Exception as e:
        return {"error": str(e)}

# Function to update weather information in the GUI 
def update_weather():
    selected_station = station_combobox.get()
    station = station_data.get(selected_station, {})
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={station['lat']}&lon={station['lon']}&appid=a0b59265aa9a652d60813de10cbe5fc9"
    weather_data = fetch_data(url)
    weather_label.config(text=f"Temperature: {int(weather_data['main']['temp'] - 273.15)}°C" if "main" in weather_data and "temp" in weather_data["main"] else "Weather data not available")

# Function to update messages from the database in the GUI
def update_messages():
    selected_station = station_combobox.get()
    try:
        connection = psycopg2.connect(dbname="Stationzuil", user="postgres", password="Dibbel12", host="20.117.103.104", port="5432")
        cursor = connection.cursor()
        cursor.execute("SELECT user_name, message FROM messages WHERE station = %s AND approved = true ORDER BY date_time DESC LIMIT 5", (selected_station,))
        messages = cursor.fetchall()
        connection.close()
        messages_text_widget.config(state=tk.NORMAL)
        messages_text_widget.delete("1.0", "end")
        messages_text_widget.insert("1.0", "No approved messages available for this station." if not messages else "\n".join([f"User Name: {message[0]}\nMessage: {message[1]}\n\n" for message in messages]))
        messages_text_widget.config(state=tk.DISABLED)
    except Exception as e:
        messages_text_widget.config(state=tk.NORMAL)
        messages_text_widget.delete("1.0", "end")
        messages_text_widget.insert("1.0", f"An error occurred: {str(e)}")
        messages_text_widget.config(state=tk.DISABLED)


# Function to update facilities information in the GUI
def update_facilities():
    selected_station = station_combobox.get()
    try:
        connection = psycopg2.connect(dbname="Stationzuil", user="postgres", password="Dibbel12", host="20.117.103.104", port="5432")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM station_service WHERE station_city = %s", (selected_station,))
        facilities_data = cursor.fetchone()
        connection.close()
        facilities = ["OV-bike", "Elevator", "Toilet", "P+R"]
        facilities_info = [facility for facility in facilities if facilities_data[facilities.index(facility) + 2]]
        facilities_label.config(text="Facilities: " + ", ".join(facilities_info) if facilities_info else "No facilities available for this station.")
    except Exception as e:
        facilities_label.config(text=f"Facilities data retrieval error: {str(e)}")

# This creates the main GUI window 
root = tk.Tk()
root.title("Stationshalscherm")
root.geometry("500x350")

# Creates the center frame of the GUI
center_frame = tk.Frame(root, bg="light blue")
center_frame.pack(expand=True, fill="both")

# Station selection combobox which allows the user to choose from different stations
station_combobox_frame = tk.Frame(center_frame)
station_combobox_frame.pack(pady=(10, 0))
station_combobox = ttk.Combobox(station_combobox_frame, state="readonly", values=["Amsterdam", "Arnhem", "Nijmegen"])
station_combobox.current(0)
station_combobox.pack()

# A weather label where the temperature gets displayed in
weather_label_frame = tk.Frame(center_frame)
weather_label_frame.pack(padx=10, pady=10, anchor="sw", side="left")
weather_label = tk.Label(weather_label_frame, text="", wraplength=300)
weather_label.pack()

# A facilities label wehre the facilities get displayed in
facilities_label_frame = tk.Frame(center_frame)
facilities_label_frame.pack(padx=10, pady=10, anchor="se", side="right")
facilities_label = tk.Label(facilities_label_frame, text="", wraplength=300)
facilities_label.pack()

# A text widget where the user messages get displayed in
messages_text_widget = tk.Text(center_frame, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
messages_text_widget.pack(padx=(25, 0), pady=(50, 0))

# Function to update data when a new station is selected
def on_station_select(event):
    update_weather()
    update_messages()
    update_facilities()

station_combobox.bind("<<ComboboxSelected>>", on_station_select)

# Initializes the GUI by updating data
on_station_select(None)

# Runs the Tkinter main loop
root.mainloop()