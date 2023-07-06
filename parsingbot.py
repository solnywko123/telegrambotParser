from bs4 import BeautifulSoup as bs
import requests
import telebot
import json
from datetime import datetime
import sys
# ---------------------------------------------------------ТЕЛЕГРАМ-----------------------------------------------------------------------------------------------------
token =  '6308404391:AAEGYOCjfO6EWxHJ9JrpM71VKn-PM0Y_Cxk'

bot = telebot.TeleBot(token)
# ------------------------------------------------для клавиатуры ReplyKeyboardMarkup-------------------------------------------------------------------------------------------------------
@bot.message_handler(func =lambda message: True)
def message_send(message):
    if message.text == "/start":
        for i in range(1,len(parser_to_title(URL))):
            title = parser_to_title(URL)[i]
            result = ''.join(title)
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            buttons = [telebot.types.KeyboardButton(str(i)) for i in range(1,len(parser_to_title(URL)))]
            markup.add(*buttons)
            bot.send_message(message.chat.id, f"{i}.{result}", reply_markup=markup)
        bot.register_next_step_handler(message,reply_to_button)
       
        
            

def reply_to_button(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons =telebot.types.KeyboardButton('Description')
    buttons2 = telebot.types.KeyboardButton('Image')
    buttons3 = telebot.types.KeyboardButton('Quit')
    markup.add(buttons,buttons2,buttons3)
    global globalurl
    globalurl = message.text
    bot.send_message(message.chat.id, parser(html_get(URL))[int(message.text)]['image'])    
    message = bot.send_message(message.chat.id, 'Some title news you can see Description of this news and Photo', reply_markup=markup)
    bot.register_next_step_handler(message, message_send_second)
    
    

    
def message_send_second(message):
    if message.text == 'Description':
        bot.send_message(message.chat.id, parser(html_get(URL))[int(globalurl)]['title'])
    if message.text == 'Image':
        bot.send_message(message.chat.id, parser(html_get(URL))[int(globalurl)]['link'])
    if message.text == 'Quit':
        bot.send_message(message.chat.id, "До свидания")
        
        
    
    
    
    
        
    
        
    
     

        
        
        
        
        
        
# -----------------------------------------------------------ПАРСЕР------------------------------------------------------------------------------------------
def html_get(URL):
    r = requests.get(URL).text
    return r

    
def parser(html):
    
    data_book = {}
    
    soup = bs(html,'lxml')
    
    news_table = soup.find('div',class_ = 'Tag--articles').find_all('div', class_ = 'Tag--article')

    key = 1
     
    for list in news_table[:21]:
        
        title = list.find('a',class_ = 'ArticleItem--name').text.strip().replace('\n',' ').split(" ' ")
        
        link = list.find('img').get('src')
        
        image = list.find('a',class_ = 'ArticleItem--image').get('href')
# запись в словарь 
        data_book[key] = {
            
            'title' : title, 
            'link' : link,
            'image': image
        }   
        key+=1
        
    return data_book
        

def parser_to_title(url):
    
    html = requests.get(url).text
    
    soup = bs(html,'lxml')
    
    news_table = soup.find('div',class_ = 'Tag--articles').find_all('div', class_ = 'Tag--article')
     
    returned = []
    for list in news_table[:21]:
        title = list.find('a',class_ = 'ArticleItem--name').text.strip().replace('\n',' ').split(" ' ")
        returned.append(title)
    return returned
    
   
    

# ---------------------------------------------------------MAIN-------------------------------------------------------------------------------------


time=datetime.now().date()
URL = 'https://kaktus.media/?lable=8&date='+str(time)+'&order=time'
html = html_get(URL)


bot.polling()




