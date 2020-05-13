import telebot

telebot.TeleBot.update_listener( listen = ' 0.0.0.0 ' ,
                       port = 8443 ,
                       url_path = ' 534247055:AAGkXwOFST2ATDcKqNF8g-aT0r9gY-yjgyE ' ,
                       key = ' cert/private.key ' ,
                       cert = ' cert/cert.pem ' ,
                       webhook_url = ' https://vlbtest.site:8443 / TOKEN ' )
