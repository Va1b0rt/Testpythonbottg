from flask import Flask, request, jsonify
import telebot, time
import gettoken

server = Flask('main')
bot = telebot.TeleBot(gettoken.token())
bot.remove_webhook()
time.sleep(2)
bot.set_webhook(url="https://185.43.5.36:8443", certificate=open('/Testpythonbottg/cert/rootCA.crt', 'r'))

@server.route("/", methods=['POST'])
def getMessage():
  r = request.get_json()
  if "message" in r.keys():
    chat_id = r["message"]["chat"]["id"]
    if "text" in r["message"]:
      text_mess = r["message"]["text"]
    else:
      bot.send_message(chat_id=chat_id, text="Problem", parse_mode='HTML')
      return "ok", 200

  if text_mess == '/start':
    bot.send_message(chat_id=chat_id, text="Hi WebHook")
    return "ok", 200

#if name == "main":
server.run(host="185.43.5.36", port=int(os.environ.get('8443', '443')), ssl_context=('/Testpythonbottg/cert/rootCA.crt', '/Testpythonbottg/cert/rootCA.key'))