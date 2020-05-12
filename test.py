#!/usr/bin/env python

import telebot
import sqlite3 as sql
import time

menu = (('add_book_name', 'add_author','add_book_genre', 'add_book_lnk', 'add_book_description', 'display_info'), ('get_random_book'))
menu_position = None

name = None
author = None
genre = None
link = None
description = None

bot = telebot.TeleBot('534247055:AAGkXwOFST2ATDcKqNF8g-aT0r9gY-yjgyE')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Добавить книгу', 'Прислать случайную книгу')

con = sql.connect('test.db', check_same_thread = False)

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `books` (`ID` INTEGER PRIMARY KEY, `chatId` INT, `name` STRING, `author` STRING, `genre` STRING , `link` STRING, `description` STRING, `book_rating` INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS `user_statistic` (`chatId` INT, `bookId` INT, `book_rating` INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS `menu_position` (`chatId` INT, `position` STRING, `viewed_book` STRING)")

    def add_finished_book(chatId):

        def adding(chatId, bookId):
            cur.execute(f"INSERT INTO `user_statistic` VALUES ('{chatId}','{row[2]}', NULL, NULL)")
            con.commit()
            return "Добавлено в прочитанные"

        cur = con.cursor()
        cur.execute(f"SELECT * FROM `menu_position` WHERE `chatId` = {chatId} ")
        rows = cur.fetchall()
        cur.execute(f"SELECT * FROM `user_statistic` WHERE `chatId` = {chatId} ")
        statistic_rows = cur.fetchall()

        for row in rows:
            for stat_row in statistic_rows:
                if stat_row[1] == row[2]:
                    return "Эта книга уже была добавлена"
            
        return adding(chatId, row[2])

    def add_viewed_book(chatId, bookId):
        cur = con.cursor()
        cur.execute(f" UPDATE `menu_position` SET `viewed_book` = '{bookId}' WHERE `chatId` = {chatId} ")
        con.commit()
        return

    def chek_user(chatId):
            cur = con.cursor()
            cur.execute(f"SELECT * FROM `menu_position` WHERE `chatId` = {chatId} ")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == chatId:
                    return True
                else:
                    return False

#Получаем случайную книгу
    def get_random_book(chatId):
        cur = con.cursor()
        cur.execute("SELECT * FROM `books` ORDER BY RANDOM() LIMIT 1")
        rows = cur.fetchall()            
        for row in rows:
           add_viewed_book(chatId, row[0])
           return "📚" + row[2] + "\n🤹‍♂️" + row[3] + "\n🎭" + row[4] + "\n🔗" + row[5] + "\n📃" + row[6]

    def get_menu_position(chatId):
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `menu_position` WHERE `chatId` = {chatId} ")
        rows = cur.fetchall()
        for row in rows:
            return row[1]

    def set_menu_position(chatId, position):
        if chek_user(chatId) == True:
            cur = con.cursor()
            cur.execute(f" UPDATE `menu_position` SET `position` = '{position}' WHERE `chatId` = {chatId} ")
            con.commit()
            return
        else:
            cur = con.cursor()
            cur.execute(f"INSERT INTO `menu_position` VALUES ('{chatId}','{position}', NULL)")
            con.commit()
            return

    def get_statistic(chatId):
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `books` WHERE `chatId` = {chatId} ")
        added_books_rows = cur.fetchall()
        cur.execute(f"SELECT * FROM `user_statistic` WHERE `chatId` = {chatId} ")
        finished_books_rows = cur.fetchall()
        cur.execute(f"SELECT * FROM `menu_position` WHERE `chatId` = {chatId} ")
        rows = cur.fetchall()
        for row in rows:
            read_book = row[2]
        cur.execute(f"SELECT * FROM `books` WHERE `ID` = {read_book} ")
        book = cur.fetchall()
        for r in book:
            r[2]
        concat = '📚Добавлено книг: {0}\n📗Прочитано книг: {1}\n📖Последняя просмотренная: {2}'.format( len(added_books_rows), len(finished_books_rows), r[2])
        return concat

    #Получаем список жанров
    def get_all_genre():
        cur = con.cursor()
        cur.execute(f"SELECT `genre` FROM `books`")
        rows = cur.fetchall()
        lst = []
        for row in rows:
            if row not in lst:
                lst.append(str(row).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
            else:
                continue
        return lst

    genre_lst = get_all_genre()

    def poll():
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

        if get_menu_position(message.chat.id) == menu[0][0] and message.text != 'Отмена':
            name = message.text
            set_menu_position(message.chat.id, menu[0][1]) 
            bot.send_message(message.chat.id, 'Укажите автора')

        elif get_menu_position(message.chat.id) == menu[0][1] and message.text != 'Отмена':
            author = message.text
            set_menu_position(message.chat.id, menu[0][2]) 
            bot.send_message(message.chat.id, 'Укажите жанр книги')

        elif get_menu_position(message.chat.id) == menu[0][2] and message.text != 'Отмена':
            genre = message.text
            set_menu_position(message.chat.id, menu[0][3]) 
            bot.send_message(message.chat.id, 'Отправьте ссылку на страницу с книгой')

        elif get_menu_position(message.chat.id) == menu[0][3] and message.text != 'Отмена':
            link = message.text
            set_menu_position(message.chat.id, menu[0][4]) 
            bot.send_message(message.chat.id, 'Опишите книгу. Постарайтесь сделать описание коротким и ёмким. ')

        elif get_menu_position(message.chat.id) == menu[0][4] and message.text != 'Отмена':
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard1.row('Добавить', 'Начать с начала')
            set_menu_position(message.chat.id, menu[0][5]) 
            description = message.text
            bot.send_message(message.chat.id, 'Название: {0}\nАвтор: {1}\nЖанр: {2}\nСсылка: {3}\nОписание: {4}\n'.format(name, author , genre, link, description), reply_markup=keyboard1)

        elif get_menu_position(message.chat.id) == menu[0][5] and message.text != 'Отмена':

            if message.text == 'Добавить':  
                   keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
                   keyboard1.row('Добавить книгу', 'Прислать случайную книгу')
                   keyboard1.row('Статистика')
                   cur = con.cursor()
                   cur.execute(f"INSERT INTO `books` VALUES (NULL ,'{message.chat.id}','{name}', '{author}', '{genre}', '{link}', '{description}', NULL)")
                   con.commit()
                   set_menu_position(message.chat.id, None)
                   bot.send_message(message.chat.id, 'Добавлено. Благодарю за пополнение коллекции.', reply_markup=keyboard1)
                   menu_position = None

            elif message.text == 'Начать с начала':
                set_menu_position(message.chat.id, menu[0][0]) 
                keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard1.row('Отмена')
                bot.send_message(message.chat.id, 'Введите название книги', reply_markup=keyboard1)

        elif message.text == 'Добавить книгу':
            set_menu_position(message.chat.id, menu[0][0]) 
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard1.row('Отмена')
            bot.send_message(message.chat.id, 'Введите название книги', reply_markup=keyboard1)

        elif message.text == 'Прислать случайную книгу':
            set_menu_position(message.chat.id, menu[1][0])
            bot.send_message(message.chat.id, get_random_book(message.chat.id) , reply_markup=inline_keyboard())
            
        elif get_menu_position(message.chat.id) == menu[1][0] and message.text == 'Прочитано':
              bot.send_message(message.chat.id,add_finished_book(message.chat.id))           
              
        elif get_menu_position(message.chat.id) == menu[1][0] and message.text == 'Назад':
            back_menu(message.chat.id)

        elif message.text == 'Отмена':
            back_menu(message.chat.id)

        elif message.text == 'Статистика':
            msg = get_statistic(message.chat.id)
            bot.send_message(message.chat.id, msg )

    con.commit()
    cur.close()
    
    @bot.callback_query_handler(func=lambda call: True)
    def process_callback_kb1btn1(call):
        if call.data == 'was_read':
            bot.answer_callback_query(callback_query_id=call.id, text=add_finished_book(call.message.chat.id), show_alert=True)
        elif call.data == 'next':
            bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text=get_random_book(call.message.chat.id))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=inline_keyboard())
        elif call.data == 'menu':
            back_menu(call.message.chat.id)
        elif call.data == 'genre':
            kbrd = ganre_keyboard(get_all_genre())
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=kbrd)
        elif call.data in genre_lst:
            
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
        set_menu_position(chatId, None)
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard1.row('Добавить книгу', 'Прислать случайную книгу')
        keyboard1.row('Статистика')
        bot.send_message(chatId,"Вы вернулись в меню", reply_markup=keyboard1)
poll()