#!/usr/bin/env python
import pymysql.cursors 

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='1234',                             
                             db='simplehr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def add_finished_book(chatId):
        def adding(chatId, bookId):
            cur.execute("INSERT INTO 'user_statistic' VALUES ('{0}','{1}', NULL)".format(chatId, row[2]))
            con.commit()
            return "Добавлено в прочитанные"

        cur = con.cursor()
        cur.execute("SELECT * FROM `menu_position` WHERE `chatId` = {0} ".format(chatId))
        rows = cur.fetchall()
        cur.execute("SELECT * FROM `user_statistic` WHERE `chatId` = {0} ".format(chatId))
        statistic_rows = cur.fetchall()

        for row in rows:
            for stat_row in statistic_rows:
                if stat_row[1] == row[2]:
                    return "Эта книга уже была добавлена"
            
        return adding(chatId, row[2])


