#!/usr/bin/env python
import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1', user='root', password='', db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cur = None

def connect(fn):
    def fnrepl(*args):
        with connection:
            cur = connection.cursor()
            return fn(*args, cur)
            connection.commit()
            cur.close()
    return fnrepl


@connect
def add_book(chatId, name, author, genre, link, description, cur):
    cur.execute("INSERT INTO `books` VALUES (NULL, '{0}','{1}', '{2}', '{3}', '{4}', '{5}', NULL)".format(chatId, name, author, genre, link, description))

    #Добавим книгу в прочитанное
@connect
def add_finished_book(chatId, cur):
        def adding(chatId, bookId):
            cur.execute("INSERT INTO 'user_statistic' VALUES ('{0}','{1}', NULL)".format(chatId, row['BOOK_ID']))
            return "Добавлено в прочитанные"

        cur.execute("SELECT * FROM `menu_position` WHERE `chatId` = {0} ".format(chatId))
        rows = cur.fetchall()
        cur.execute("SELECT * FROM `user_statistic` WHERE `chatId` = {0} ".format(chatId))
        statistic_rows = cur.fetchall()

        for row in rows:
            for stat_row in statistic_rows:
                if stat_row['BOOKID'] == row['BOOK_ID']:
                    return "Эта книга уже была добавлена"
            
        return adding(chatId, row['BOOK_ID'])

@connect    
def add_viewed_book(chatId, bookName, cur):
        cur.execute(" UPDATE `menu_position` SET `viewed_book` = '{0}' WHERE `chatId` = {1} ".format(bookName, chatId))
        return

@connect
def chek_user(chatId, cur):
    cur.execute("SELECT * FROM `menu_position` WHERE `chatId` = {0} ".format(chatId))
    rows = cur.fetchall()
    for row in rows:
        if row['CHATID'] == chatId:
           return True
        else:
           return False

    #Получаем случайную книгу
@connect
def get_random_book(chatId, slct_genre, cur):

        if slct_genre != None:
            where = "WHERE genre = '{0}'".format(slct_genre)
        else:
            where = None

        order_by = slct_genre

        cur.execute("SELECT * FROM `books`{0} ORDER BY RAND() LIMIT 1".format(where))
        rows = cur.fetchall()            
        for row in rows:
           add_viewed_book(chatId, row['BOOK_NAME'])
           return "📚" + row['AUTHOR'] + "\n🤹‍♂️" + row['BOOK_DESCRIPTION'] + "\n🎭" + row['BOOK_NAME'] + "\n🔗" + row['GENRE'] + "\n📃" + row['LINK']

@connect
def set_menu_position(chatId, position, cur):
    if chek_user(chatId) == True:
        cur.execute(" UPDATE `menu_position` SET `position` = '{0}' WHERE `chatId` = {1} ".format(position, chatId))
        return
    else:
        cur.execute("INSERT INTO `menu_position` VALUES ('{0}','{1}', NULL, NULL, NULL)".format(chatId, position))
        return

@connect
def get_menu_position(chatId, cur):

        cur.execute("SELECT * FROM `menu_position` WHERE `chatId` = {0} ".format(chatId))
        rows = cur.fetchall()
        for row in rows:
            return row['POSITION']

   
@connect
def get_statistic(chatId, cur):
        read_book = None

        cur.execute("SELECT * FROM `books` WHERE `chatId` = {0} ".format(chatId))
        added_books_rows = cur.fetchall()
        cur.execute("SELECT * FROM `user_statistic` WHERE `chatId` = {0} ".format(chatId))
        finished_books_rows = cur.fetchall()
        cur.execute("SELECT * FROM `menu_position` WHERE `chatId` = {0} ".format(chatId))
        rows = cur.fetchall()
        for row in rows:
            read_book = row['VIEWED_BOOK']
        #cur.execute("SELECT * FROM `books` WHERE `BOOK_NAME` = {0} ".format(read_book))
        #book = cur.fetchall()
        for r in added_books_rows:
            concat = '📚Добавлено книг: {0}\n📗Прочитано книг: {1}\n📖Последняя просмотренная: {2}'.format( len(added_books_rows), len(finished_books_rows), r['BOOK_NAME'])
        return concat

    #Получаем список жанров
@connect
def get_all_genre(cur):

        cur.execute("SELECT `genre` FROM `books`")
        rows = cur.fetchall()
        lst = []
        for row in rows:
            if str(row).replace("(", "").replace(")", "").replace(",", "").replace("'", "") not in lst:
                lst.append( str(row).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
            else:
                continue
        return lst