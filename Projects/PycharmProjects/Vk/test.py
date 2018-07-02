import vk
#global token
#session = vk.AuthSession('6618701', '79686098859', '1835645', scope='wall, messages')
#session = vk.AuthSession(access_token = token )
#vk_api = vk.API(session)

#print(vk_api.users.get(user_id=151069916, fields='online, last_seen', v = 5.80))
import urllib
from urllib.request import urlopen
import vkbot
import sqlite3
import Registration
import time
import telebot
import os
import re

import json
tokenT = "587800331:AAHxyJwy4p7k61iMqtF17HfQ9pV2mh0hqXw"
bot = telebot.TeleBot(tokenT)
#print(bot.get_me())





@bot.message_handler(commands=['start'])
def a(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row("Обновить сообщения")
    bot.send_message(message.chat.id, "Нажмите на эту кнопку для обновления непрочитанных сообщений", reply_markup=user_markup)

    if Registration.start(message) == "0":
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти",
                                                        url="https://oauth.vk.com/authorize?client_id=6618701&display=page&redirect_uri=https://oauth.vk.com/blank.html&display=page&scope=messages,offline&response_type=code&v=5.80")
        keyboard.add(url_button)
        bot.send_message(message.chat.id,
                         "Здраствуйте. Перейдите по ссылке и разрешите приложению читать ваши сообщения",
                         reply_markup=keyboard)
        bot.send_message(message.chat.id, "Введите полученную по этому адресу ссылку")
    else:
        pass


@bot.message_handler(commands=['chats'])
def chat(message):#выводит список последних чатов

    #tokenVK =
    #name = []

    name = vkbot.chats(Registration.start(message))
    keyboard = telebot.types.InlineKeyboardMarkup()
    #callback_button = telebot.types.InlineKeyboardButton(text='Нажмите что бы перейти к чату', callback_data="test")
    i = 0
    for a in name:
        callback_button = telebot.types.InlineKeyboardButton(text=a , callback_data=name[a])
        keyboard.add(callback_button)
        i+=1

    bot.send_message(message.chat.id, "Выберите чат", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:


        #print(call.data)
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        #print(call.data)

        conn = sqlite3.connect("vk.db")
        cursor = conn.cursor()

        #a = str(call.data)
        # a = [(token,idT)]
        # cursor.execute(a)

        cursor.execute('UPDATE users SET chat=? WHERE id_in_telegram=?', (str(call.data), str(call.message.chat.id)))
        conn.commit()
        #cursor.executemany("INSERT INTO users(chat) VALUES (?)", [call.data])
        #bot.answer_callback_query(call.id, text="Чат выбран")

        obnov(call.message.chat.id)





@bot.message_handler(content_types=['text'])
def handle_start(message):



    #cursor.execute(sql, [(str(message.chat.id))])
    # print(len(cursor.fetchall()[:]))
    tokenVK = Registration.start(message)
    if  tokenVK == '0':
        a = message.text.split('/')
        b = 'https://oauth.vk.com/'.split('/')
        if a[0:2] == b[0:2]:
            Registration.start1(message)
            print('0')
    else:
        if message.text == "Обновить сообщения":
            obnov(message.chat.id)
                #bot.send_message(token[1], name_users['first_name'] + ' ' + name_users['last_name'] + ":  " + a['body'])

        else:
            #obnov(message.chat.id)
            import  vk
            import vkbot
            token = vkbot.token(message.chat.id)
            session = vk.AuthSession(access_token=token[0])
            vk_api = vk.API(session)
        #bot.send_message(message.from_user.id, "Сообщения обновляются", reply_markup=user_markup)

            vk_api.messages.send(peer_id=token[1], message=message.text, v=5.38)


        #
def obnov(message):

    token = vkbot.token(message)
    session = vk.AuthSession(access_token=token[0])
    vk_api = vk.API(session)
    data = vk_api.messages.getHistory(offset=-200, count=200, start_message_id=-1, peer_id=token[1], v=5.38)
    for a in reversed(data['items']):
        # print(a)
        # print(a['user_id'])

        name_users = vk_api.users.get(user_ids=a['user_id'], fields='first_name,last_name', v=5.80)[0]
        # print(name_users['first_name'] + ' ' + name_users['last_name'])
        bot.send_message(message,
                         name_users['first_name'] + ' ' + name_users['last_name'] + ":  " + a['body'])
        vk_api.messages.markAsRead(peer_id =token[1], v = 5.38 )
        # print(a['body'])


@bot.message_handler(content_types=[''])
def handle_start(message):
    pass


#while True:
#    try:
bot.polling(none_stop=True, interval=0)

#    except Exception as e:
#        print(e)
#        time.sleep(5)