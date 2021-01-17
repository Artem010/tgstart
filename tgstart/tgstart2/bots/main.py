import config
import telebot
import os, json


import datetime

bot = telebot.TeleBot(config.token)
cDir = os.getcwd() + '/tgstart2/bots/' + config.user_id + "/" + config.bot_id

with open(cDir+"/stat.json", "r") as read_file:
    data = json.load(read_file)
msgs = int(data['msgs'])
# print(data['msgopen(cDir+"open(cDir+"s'])

print(msgs)
def updStat():
    global msgs
    msgs += 2
    with open(cDir+"/stat.json", "w") as write_file:
        json.dump({'msgs':msgs}, write_file)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    updStat();


if __name__ == '__main__':
     bot.polling(none_stop=True, interval=1)
