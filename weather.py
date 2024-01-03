########################################################################################################################
# @author Arusha Patil
# @date 01-03-2024
# @summary a basic weather forecasting program to practice RESTful API calls and JSON response analysis
# Returns a description of the weather in a given location (submitted via IP address or city name) and whether it's colder or hotter today than yesterday.
########################################################################################################################

import requests
import re
from datetime import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
DAY_IN_SECONDS = 86400

#######################################################
# Function takes in a city name and makes requests to Open Weather Map API for weather description and temperature
#######################################################
def get_weather_description(city_name):
    api_key = 'bcc9c21b2abe789448851e0fad6cd0a2'
    api_endpoint = 'https://api.openweathermap.org/data/2.5/weather'
    query_params = {'q': city_name, 'appid': api_key, 'units': 'metric'}

    response = requests.get(api_endpoint, params=query_params) #  For today
    yesterday = int(datetime.now().timestamp()) - DAY_IN_SECONDS
    query_params = {'q': city_name, 'dt' : yesterday, 'appid': api_key, 'units': 'metric'}
    response_ys = requests.get(api_endpoint, params=query_params) #  For yesterdaay
    if response.status_code == 200:
        if response_ys.status_code == 200:
            ys_data = response_ys.json()
        else: 
            print(f'Error: {response_ys.status_code} - {response_ys.text}')
            return 1
        data = response.json()
        temp = round(data['main']['temp']*1.8 + 32, 1)
        if (data['main']['temp'] > ys_data['main']['temp']):
            resp = (f"At {temp}°F, it is hotter than it was yesterday.")
        else:
            resp = (f"At {temp}°F, it is colder than it was yesterday.")
        # Handle response data
        weather = data['weather'][0]['description']
        return(f"Expect {weather} in {city_name}. {resp}")
    else:
        # Handle errors
        print(f'Error: {response.status_code} - {response.text}')
        return 1

#######################################################
# Function takes in an IP address (optional) and returns the city corresponding to that IP address
#######################################################
def get_location(ip_address):
    api_key = 'ipb_live_PrcCQEmgKwQ7aSDpInzQly0C6OI2SaMyP35GUAh6'
    api_endpoint = 'https://api.ipbase.com/v2/info?apikey=ipb_live_PrcCQEmgKwQ7aSDpInzQly0C6OI2SaMyP35GUAh6&ip=1.1.1.1'
    query_params = {'apiKey': api_key}
    
    if ip_address:
        print(f'IP Address Given')
        query_params['ip'] = ip_address

    response = requests.get(api_endpoint, params=query_params)

    if response.status_code == 200: #  Successful resquestion
        data = response.json()
        try:
            location_data = data['data']['location']
            city_name = location_data['city']['name']
            return city_name
        except KeyError as e:
            print(f'Error: {e}')
            return 1
    else:
        # Handle errors
        print(f'Error: {response.status_code} - {response.text}')
        return 1

#######################################################
# Graphics User Interface via kivy
#######################################################
class WeatherApp(App):
    def build(self):
        self.title = "Weather Forecasting App"
        self.layout = BoxLayout(orientation="vertical")

        self.input_label = Label(text="Enter city or IP address:")
        self.layout.add_widget(self.input_label)

        self.input_field = TextInput(multiline=False)
        self.layout.add_widget(self.input_field)

        self.submit_button = Button(text="Get Weather")
        self.submit_button.bind(on_press=self.get_weather)
        self.layout.add_widget(self.submit_button)

        self.location_button = Button(text="Use Current Location")
        self.location_button.bind(on_press=self.get_location_weather)
        self.layout.add_widget(self.location_button)

        self.weather_label = Label(text="")
        self.layout.add_widget(self.weather_label)

        return self.layout

    def get_weather(self, instance):
        input_value = self.input_field.text
        if isIP(input_value):
            loc = get_location(input_value)
        else:
            loc = input_value
        wd = get_weather_description(loc)
        self.weather_label.text = wd

    def get_location_weather(self, instance):
        loc = get_location(None)
        wd = get_weather_description(loc)
        self.weather_label.text = wd

IP_ADDRESS_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def isIP(input):
    if IP_ADDRESS_REGEX.match(input):
        return True
    return False

if __name__ == '__main__':
    WeatherApp().run()