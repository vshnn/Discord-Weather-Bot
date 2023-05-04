import discord
import requests
import json
import os
import dotenv


dotenv.load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members=True
intents.message_content=True

client = discord.Client(intents=intents)

API_KEY = os.getenv('KEY')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    if message.content.startswith('!weather'):
        
        city = message.content.split(' ')[1]
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = json.loads(response.text)
        if data['cod'] == '404':
            await message.channel.send('City not found. Please try again.')
        else:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            conditions = data['weather'][0]['description']
            await message.channel.send(f'The current weather in {city} is {temp}°C, {humidity}% humidity, {wind_speed} m/s wind speed, and {conditions}.')

    if message.content.startswith('!forecast'):
        try:
            city = message.content.split(' ')[1]
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            data = json.loads(response.text)

            forecast = ''
            for i in range(0, len(data['list']), 8):
                date_time = data['list'][i]['dt_txt']
                temp = data['list'][i]['main']['temp']
                conditions = data['list'][i]['weather'][0]['description']
                forecast += f'{date_time}: {temp}°C with {conditions}\n'

            await message.channel.send(forecast)
        except:
            await message.channel.send('Unable to fetch weather forecast. Please check the spelling of the city and try again.')


@client.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(os.getenv('TOKEN'))
