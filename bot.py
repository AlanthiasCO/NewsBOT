import discord
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import wikipedia
from GoogleNews import GoogleNews
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')

def cotacao():
    response = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL,EUR-BRL,BTC-BRL')
    json_data = json.loads(response.text)
    return json_data

def get_news(search):
    googlenews = GoogleNews()
    googlenews.set_lang('pt')
    googlenews.search(search)
    result = googlenews.result()
    return result[:5]

def get_info(search):
    wikipedia.set_lang('pt')
    result = wikipedia.summary(search, sentences=2)
    return result

def get_qr_code(link):
    qr_url = f'https://api.qrserver.com/v1/create-qr-code/?data={link}&size=200x200'
    return qr_url


def get_weather(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather'
    contry = 'BR'
    result = requests.get(base_url, params={"q": "{},{}".format(city, contry),
                                   "appid": API_KEY,
                                   "units": "metric",
                                   "lang": "pt_br"})
    data = result.json()
    if data['cod'] == '404':
        return 'Cidade não encontrada.', None
    else:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        return f'Em {city} está {weather}. A temperatura é de {temp}°C, mas parece que está {feels_like}°C.', (weather, temp, feels_like)
         
         
def create_weather_image(city, weather, temp, feels_like):
    img = Image.new('RGB', (250, 150), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    
    font_path = "arial.ttf"
    font = ImageFont.truetype(font_path, 18)
    text = f'{city}\n{weather}\nTemperatura: {temp}°C\nSensação térmica: {feels_like}°C'
    d.text((10,20), text, font=font, fill=(255, 255, 255))
    
    img_path = f'{city}_weather.png'
    img.save(img_path)
    return img_path         

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$start'):
            await message.channel.send(
            'Olá, eu sou o NewsBOT! :smile:\n'
            'Estou aqui para te ajudar com algumas coisas.\n'
            '\nLista de comandos disponíveis:\n'
            '$info <termo> - Mostra informações sobre o termo pesquisado. Fonte: Wikipédia. \n'
            '$news <termo> - Mostra as últimas notícias sobre o termo pesquisado. :newspaper2: \n'
            '$cotacao - Mostra a cotação atual do dólar. :moneybag: \n'
            '$conversao <quantidade> <moeda_origem> <moeda_destino> - Converte a quantidade de uma moeda para outra. :moneybag: \n'
            '$qrcode <link> - Mostra o QR Code do link fornecido.\n'
            '$clima <cidade> - Mostra o clima atual da cidade. :white_sun_rain_cloud: \n'
            )
        
        elif message.content.startswith('$clear'):
            if message.author.id == message.guild.owner_id:
                await message.channel.purge(limit=100)  # Limite de 100 mensagens
            else:
                await message.channel.send('Você não tem permissão para usar este comando.')        
        
        elif message.content.startswith('$info'):
            search_term = message.content[len('$info '):].strip()
            if search_term:
                await message.channel.send(get_info(search_term))
            else:
                await message.channel.send('Por favor, forneça um termo de pesquisa após o comando $info.')
        
        elif message.content.startswith('$news'):
            search_term = message.content[len('$news '):].strip()
            if search_term:
                news = get_news(search_term)
                for n in news:
                    await message.channel.send(
                        f'{n["title"]}\n{n["link"]}\n{n["media"]}\n{n["date"]}\n\n'
                    )
            else:
                await message.channel.send('Por favor, forneça um termo de pesquisa após o comando $news.')
        
        elif message.content.startswith('$cotacao'):
            data = cotacao()
            await message.channel.send(
                f'USD: {data["USD"]["high"]}\n'
            )
            
        elif message.content.startswith('$conversao'):
            parts = message.content.split()
            if len(parts) == 4:
                amount = float(parts[1])
                from_currency = parts[2].upper()
                to_currency = parts[3].upper()
                data = cotacao()
                if from_currency == 'BRL' and to_currency == 'USD':
                    rate = 1 / float(data["USD"]["high"])
                    converted_amount = amount * rate
                    await message.channel.send(f'{amount} BRL é igual a {converted_amount:.2f} USD')
                elif from_currency == 'USD' and to_currency == 'BRL':
                    rate = float(data["USD"]["high"])
                    converted_amount = amount * rate
                    await message.channel.send(f'{amount} USD é igual a {converted_amount:.2f} BRL')
                else:
                    await message.channel.send('Conversão não suportada. Use BRL para USD ou USD para BRL.')
            else:
                await message.channel.send('Uso: $conversao <quantidade> <moeda_origem> <moeda_destino>')
        
        elif message.content.startswith('$qrcode'):
            link = message.content[len('$qrcode '):].strip()
            if link:
                qr_code_url = get_qr_code(link)
                await message.channel.send(qr_code_url)
            else:
                await message.channel.send('Por favor, forneça um link após o comando $qrcode.')

        elif message.content.startswith('$clima'):
            city = message.content.split('$clima ')[1]
            weather_text, weather_data = get_weather(city)
            if weather_data:
                weather, temp, feels_like = weather_data
                img_path = create_weather_image(city, weather, temp, feels_like)
                await message.channel.send(file=discord.File(img_path))
            else:
                await message.channel.send(weather_text)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(DISCORD_TOKEN) # Replace with your own token