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

# print(msgs)
def updStat():
    global msgs
    msgs += 2

    with open(cDir+"/stat.json", "r") as read_file:
        data = json.load(read_file)

    data['msgs'] =msgs

    with open(cDir+"/stat.json", "w") as write_file:
        json.dump(data, write_file)

def add_user(id, username, first_name, last_name, pathAvatar):

    with open(cDir+"/stat.json", "r") as read_file:
        data = json.load(read_file)

    now = datetime.datetime.now()
    cDate = now.strftime("%d-%m-%Y %H:%M")

    user = {
        'username':username,
        'first_name':first_name,
        'last_name':last_name,
        'tg_id':id,
        'pathAvatar': pathAvatar,
        'dateReg': cDate
        }

    data['users'].append(user)

    with open(cDir+"/stat.json", "w") as write_file:
        json.dump(data, write_file)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    user_profile = bot.get_user_profile_photos(message.from_user.id);
    file_id= user_profile.photos[0][0].file_id
    file_info = bot.get_file(file_id);
    # print('https://api.telegram.org/file/bot'+config.token+'/'+file_info.file_path)

    # downloaded_file = bot.download_file(file_info.file_path)
    # bot.send_photo(message.chat.id, downloaded_file);


    add_user(str(message.chat.id), str(message.chat.username),str(message.chat.first_name),str(message.chat.last_name), file_info.file_path);
    bot.send_message(message.chat.id, 'User saved')




@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    updStat();


if __name__ == '__main__':
     bot.polling(none_stop=True, interval=1)
