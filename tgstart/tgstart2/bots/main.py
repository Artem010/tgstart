import config
import telebot
import sqlite3
import os, json


import datetime


pathDB = os.getcwd() + '/db.sqlite3'
bot = telebot.TeleBot(config.token)
cDir = os.getcwd() + '/tgstart2/bots/' + config.user_id + "/" + config.bot_id

# custom def

def getDate():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y")

def addUSerDB(tg_id, username, first_name, last_name, pathAvatar):
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")


        sqlite_select_query = """SELECT tg_id from users_botuser where bot_name_id = ? and tg_id =?"""
        cursor.execute(sqlite_select_query, (config.bot_id, tg_id))
        records = cursor.fetchone()
        # Если в таблице нет пользователя с таким id у данного бота с bot_name_id, то добавляем нового
        if(records == None ):
            now = datetime.datetime.now()
            cDate = now.strftime("%d-%m-%Y %H:%M")

            sqlite_insert_query = """INSERT INTO users_botuser
                                    (username, first_name, last_name, tg_id, pathAvatar, bot_name_id, dateReg)
                                    VALUES (?, ?, ?, ?, ?, ?, ?);"""

            data_tuple  = (username,first_name, last_name,tg_id,pathAvatar,config.bot_id,cDate)

            count = cursor.execute(sqlite_insert_query, data_tuple)
            sqlite_connection.commit()
            print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
            cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def addMsgsDB():
    try:
        sqlite_connection = sqlite3.connect(pathDB)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from users_messages where bot_name_id = ? and date = ? """
        cDate = getDate()
        cursor.execute(sqlite_select_query, (config.bot_id,cDate))
        records = cursor.fetchall()
        if(len(records) > 0 ):
            count = records[0][1] + 2
            sql_update_query = """Update users_messages set count = ? where bot_name_id = ?"""
            cursor.execute(sql_update_query, (count, config.bot_id))
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()
        else:
            sqlite_insert_query = """INSERT INTO users_messages
                                    (count,date, bot_name_id)
                                    VALUES (?, ?, ?);"""

            data_tuple  = (2, cDate, config.bot_id)
            count = cursor.execute(sqlite_insert_query, data_tuple)
            sqlite_connection.commit()
            print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
            cursor.close()


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

# custom def






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
    # print('https://api.telegram.org/file/bot'+config.token+'/'+file_info.file_path)

    # downloaded_file = bot.download_file(file_info.file_path)
    # bot.send_photo(message.chat.id, downloaded_file);


    addUSerDB(str(message.chat.id), str(message.chat.username),str(message.chat.first_name),str(message.chat.last_name), file_path);
    bot.send_message(message.chat.id, 'User saved')




@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    addMsgsDB()


if __name__ == '__main__':
     bot.polling(none_stop=True, interval=1)
