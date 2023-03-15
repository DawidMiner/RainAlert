import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = "212ea56229a76b2f4d286a214ee96ac4"
account_sid = 'AC0cbae5f7f4acee3308abd9de1dc12d95'
auth_token = '72ba33df68d01ad02e218eb90ed3faad'

parameters = {
    "lat": 52.170490,
    "lon": 23.095970,
    "exclude": "current,minutely,daily,alerts",
    "appid": api_key
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
weather = response.json()

weather_slice = weather['hourly'][:12]

will_rain = False

for weather_data in weather_slice:
    weather_conditions = weather_data['weather'][0]['id']
    if int(weather_conditions) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(username=account_sid, password=auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella!",
        from_='+18596482463',
        to="+48721553011"
    )