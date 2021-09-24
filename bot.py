#Imported Libs
from os import name
import requests
import json
from datetime import datetime
import time
from requests.api import get
import telebot
from telebot.types import Chat, Message


bot = telebot.TeleBot('API_KEY')

def get_index():
    url = 'https://api.alternative.me/'
    endpoint = 'fng/'
    r = requests.get(url + endpoint)
    data = r.json()
    name = data['name']
    value = data['data'][0]['value']
    value_classification = data['data'][0]['value_classification']
    timestamp = data['data'][0]['timestamp']
    time_until_update = data['data'][0]['time_until_update']
    return data

get_index()

class Index:
    def __init__(self):
        self.value = []
        self.value_classification = []
        self.timestamp = []
        self.time_until_update = []
    #Assigning Values
    def store_values(self,data):
         for i in range (1):
            self.value.append(data['data'][i]['value'])
            self.value_classification.append(data['data'][i]['value_classification'])
            self.timestamp.append(data['data'][i]['timestamp'])
            self.time_until_update.append(data['data'][i]['time_until_update'])

    #List of Values   
    def get_values(self):
        file = open('fear_greed.txt', '+w')
        file.write('#NotFinancialAdvice\n'
                    'Fear and Greed Index \n')
        for i in range(1):
            timestamp = self.timestamp[i]
            update = self.time_until_update[i]
            update_time = (int(update))
            date_time = datetime.fromtimestamp(int(timestamp))
            d = date_time.strftime("%m/%d/%Y")
            u = time.strftime("%H hours, %M minutes, %S seconds", time.gmtime(update_time))
            file.write(f"Value: ({self.value[i]})\nCurrent Status: {self.value_classification[i]}\n{d}\nThe next update will happen in:\n{u}\n")
        file.close()
    #Next Update
    def get_Update(self):
        file = open('update.txt', '+w')
        file.write('Next Update:\n'
                )
        for i in range(1):
            update = self.time_until_update[i]
            update_time = (int(update))
            u = time.strftime("%H hours, %M minutes, %S seconds", time.gmtime(update_time))
            file.write(f"The next update will happen in:\n{u}\n")
        file.close()


if __name__ == '__main__':
    print("Loading...")

#Message Commands
@bot.message_handler(commands=['status'])
def get_recent(message):    
    index = Index()
    data = get_index()
    index.store_values(data)
    index.get_values()
    
    with open('fear_greed.txt', 'r') as file:
        lines = file.read()
    
    bot.send_message(message.chat.id, lines)

@bot.message_handler(commands=['update'])
def get_recent(message):    
    index = Index()
    data = get_index()
    index.store_values(data)
    index.get_Update()
    
    with open('update.txt', 'r') as file:
        lines = file.read()
    
    bot.send_message(message.chat.id, lines)


@bot.message_handler(commands='start')
def start_bot(message):
    bot.send_message(message.chat.id,'The bot has started!\n' +
    '/status - Allows you to check the current status of the current Crypto Market!\n' +
    '/update - Will inform you when The Fear and Greed Index values will change.')

bot.polling()
