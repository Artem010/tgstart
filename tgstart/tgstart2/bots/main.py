import config
import telebot
import os


import datetime

bot = telebot.TeleBot(config.token)

msgs = 0
cDir = os.getcwd() + '/tgstart2/bots/' + config.user_id + "/" + config.bot_id
print(cDir)

def updStat():
    global msgs
    msgs += 2

    text_config = open(cDir+"/stat.py", "w")
    # text_config.write("count = '" +str(msgs)+"'")
    text_config.write(str(msgs))

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    updStat();


if __name__ == '__main__':
     bot.polling(none_stop=True, interval=1)
