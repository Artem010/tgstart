import sys,os
sys.path.insert(0, os.getcwd() + '/tgstart2/bots/')
import config
import telebot
import sqlite3
import json
import dbAll

bot = telebot.TeleBot(config.token)
cDir = os.getcwd() + '/tgstart2/bots/' + config.user_id + "/" + config.bot_id

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    user_profile = bot.get_user_profile_photos(message.from_user.id);
    # print()
    if(user_profile.total_count > 0):
        file_id= user_profile.photos[0][0].file_id
        file_info = bot.get_file(file_id);
        file_path = file_info.file_path
    else:
        file_path = "None"

    dbAll.addUSerDB(config, str(message.chat.id), str(message.chat.username),str(message.chat.first_name),str(message.chat.last_name), file_path);
    bot.send_message(message.chat.id, 'User saved')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    dbAll.addMsgsDB(config)


if __name__ == '__main__':
     bot.polling(none_stop=True, interval=1)
