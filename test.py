#!/usr/bin/env python

import telebot
import sqlite3 as sql
import time
#import latinizator
import gettoken
import dbWorker

menu = (('add_book_name', 'add_author','add_book_genre', 'add_book_lnk', 'add_book_description', 'display_info'), ('get_random_book'))
menu_position = None

#cur.execute("CREATE TABLE IF NOT EXISTS `books` (`chatId` INT, `name` STRING, `author` STRING, `genre` STRING , `link` STRING, `description` STRING, `book_rating` INT)")
#cur.execute("CREATE TABLE IF NOT EXISTS `user_statistic` (`chatId` INT, `bookId` INT, `book_rating` INT)")
#cur.execute("CREATE TABLE IF NOT EXISTS `menu_position` (`chatId` INT, `position` STRING, `viewed_book` STRING, `select_genre` STRING)")

name = None
author = None
genre = None
link = None
description = None
select_genre = None


bot = telebot.TeleBot(gettoken.token())

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Добавить книгу', 'Прислать случайную книгу')

   

genre_lst = dbWorker.get_all_genre()

def poll():
        print('Start polling...')
        try:
            bot.polling(none_stop=True)
        except ConnectionError:
            print("Telebot Exception: ConnectionError 'Удаленный хост принудительно разорвал существующее подключение'")
            print("Перезапускаем...")
            time.sleep(10)
            poll()
        except telebot.apihelper.ApiException:
            print("Telebot Exception: Bad Request 'Запрос к API Telegram не выполнен. Сервер вернул HTTP 400'")
            print("Перезапускаем...")
            time.sleep(10)
            poll()


@bot.message_handler(commands=['start'])
def start_message(message):
        bot.send_message(message.chat.id, 'Привет!\nЭтот бот предназначен для обмена ссылками на аудиокниги в открытом доступе.\nНадеюсь, что ты сможешь найти для себя тут что-нибудь интересное.\nИ буду очень благодарен, если ты добавишь ссылку на свою любимую аудиокнигу.', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):

        global menu_position
        global name
        global author
        global genre
        global link
        global description
        global keyboard1
        global cur

        global select_genre

        if dbWorker.get_menu_position(message.chat.id) == menu[0][0]: #and message.text != 'Отмена':
            name = message.text
            dbWorker.set_menu_position(message.chat.id, menu[0][1]) 
            bot.send_message(message.chat.id, 'Укажите автора')

        elif dbWorker.get_menu_position(message.chat.id) == menu[0][1] and message.text != 'Отмена':
            author = message.text
            dbWorker.set_menu_position(message.chat.id, menu[0][2]) 
            bot.send_message(message.chat.id, 'Укажите жанр книги')

        elif dbWorker.get_menu_position(message.chat.id) == menu[0][2] and message.text != 'Отмена':
            genre = message.text
            dbWorker.set_menu_position(message.chat.id, menu[0][3]) 
            bot.send_message(message.chat.id, 'Отправьте ссылку на страницу с книгой')

        elif dbWorker.get_menu_position(message.chat.id) == menu[0][3] and message.text != 'Отмена':
            link = message.text
            dbWorker.set_menu_position(message.chat.id, menu[0][4]) 
            bot.send_message(message.chat.id, 'Опишите книгу. Постарайтесь сделать описание коротким и ёмким. ')

        elif dbWorker.get_menu_position(message.chat.id) == menu[0][4] and message.text != 'Отмена':
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard1.row('Добавить', 'Начать с начала')
            dbWorker.set_menu_position(message.chat.id, menu[0][5]) 
            description = message.text
            bot.send_message(message.chat.id, 'Название: {0}\nАвтор: {1}\nЖанр: {2}\nСсылка: {3}\nОписание: {4}\n'.format(name, author , genre, link, description), reply_markup=keyboard1)

        elif dbWorker.get_menu_position(message.chat.id) == menu[0][5] and message.text != 'Отмена':

            if message.text == 'Добавить':  
                   keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
                   keyboard1.row('Добавить книгу', 'Прислать случайную книгу')
                   keyboard1.row('Статистика')
                   
                   dbWorker.add_book(message.chat.id, name, author, genre, link, description)
                   
                   dbWorker.set_menu_position(message.chat.id, None)
                   bot.send_message(message.chat.id, 'Добавлено. Благодарю за пополнение коллекции.', reply_markup=keyboard1)
                   menu_position = None

            elif message.text == 'Начать с начала':
                dbWorker.set_menu_position(message.chat.id, menu[0][0]) 
                keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard1.row('Отмена')
                bot.send_message(message.chat.id, 'Введите название книги', reply_markup=keyboard1)

        elif message.text == 'Добавить книгу':
            dbWorker.set_menu_position(message.chat.id, menu[0][0]) 
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard1.row('Отмена')
            bot.send_message(message.chat.id, 'Введите название книги', reply_markup=keyboard1)

        elif message.text == 'Прислать случайную книгу':
            dbWorker.set_menu_position(message.chat.id, menu[1][0])
            bot.send_message(message.chat.id, dbWorker.get_random_book(message.chat.id, select_genre) , reply_markup=inline_keyboard())
            
        elif dbWorker.get_menu_position(message.chat.id) == menu[1][0] and message.text == 'Прочитано':
              bot.send_message(message.chat.id, dbWorker.add_finished_book(message.chat.id))           
              
        elif dbWorker.get_menu_position(message.chat.id) == menu[1][0] and message.text == 'Назад':
            back_menu(message.chat.id)

        elif message.text == 'Отмена':
            back_menu(message.chat.id)

        elif message.text == 'Статистика':
            msg = dbWorker.get_statistic(message.chat.id)
            bot.send_message(message.chat.id, msg )


    
@bot.callback_query_handler(func=lambda call: True)
def process_callback_kb1btn1(call):
        global select_genre
        if call.data == 'was_read':
            bot.answer_callback_query(callback_query_id=call.id, text=dbWorker.add_finished_book(call.message.chat.id), show_alert=True)
        elif call.data == 'next':
            bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text=dbWorker.get_random_book(call.message.chat.id, select_genre))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=inline_keyboard(select_genre))
        elif call.data == 'menu':
            back_menu(call.message.chat.id)
        elif call.data == 'genre':
            kbrd = ganre_keyboard(dbWorker.get_all_genre())
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=kbrd)
        elif call.data in genre_lst:
            select_genre = call.data
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=inline_keyboard(call.data))

def ganre_keyboard(lst):
        kb = telebot.types.InlineKeyboardMarkup()
        for l in lst:
            kb.row(telebot.types.InlineKeyboardButton('{0}'.format(l).replace("(", "").replace(")", "").replace(",", "") , callback_data=str(l)))
        return kb


def inline_keyboard(gnr = None):
        if gnr == None:
            gnre = 'Все жанры'
        else:
            gnre = gnr

        inline_kb1 = telebot.types.InlineKeyboardMarkup() 
        inline_kb1.add(telebot.types.InlineKeyboardButton('Прочитано', callback_data='was_read'), telebot.types.InlineKeyboardButton('>>>', callback_data='next'))
        inline_kb1.row(telebot.types.InlineKeyboardButton('Жанр: {0}'.format(gnre), callback_data='genre'))
        inline_kb1.row(telebot.types.InlineKeyboardButton('Вернуться в меню', callback_data='menu'))
        return inline_kb1

def back_menu(chatId):
        dbWorker.set_menu_position(chatId, None)
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard1.row('Добавить книгу', 'Прислать случайную книгу')
        keyboard1.row('Статистика')
        bot.send_message(chatId,"Вы вернулись в меню", reply_markup=keyboard1)
poll()