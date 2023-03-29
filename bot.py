import telebot
import sql_fnc
import sql_query
from config import TOKEN
from classes import User

    
bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("get_foto", "Загрузить мои фото"),
        telebot.types.BotCommand("get_video", "Загрузить мои видео"),
        telebot.types.BotCommand("get_document", "Загрузить мои документы")
    ],)

user = User(bot)

def main():

    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        bot.send_message(chat_id=message.from_user.id, text="""
Бот предназначен для сохранения фото, видео, документов
в базу данных Sqlite и выгрузки обратно из базы по коммандам
По сути это шаблон тг бота  части сохранения данных

/start - записывает данные пользователя в БД

/get_foto - выгружает все фото + id сообщения в разрезе пользователя из БД

/get_video - выгружает все видео + id сообщения  в разрезе пользователя из БД

/get_document - выгружает все документы + id сообщения в разрезе пользователя из БД
""")
        user.save_user(message=message)



    @bot.message_handler(content_types=['photo', 'video', 'document'])
    def cont_fnc(message):
        print(message)
        if message.content_type == 'photo':
            user.save_photo(message=message)
        elif message.content_type == 'document':
            user.save_document(message=message)
        elif message.content_type == 'video':
            user.save_video(message=message)


    @bot.message_handler(commands=['get_foto', 'get_video', 'get_document'])
    def commands_fnc(message):
        if message.text == '/get_foto':
            res = user.get_photo(message=message)

            for i in res:
                msg_id = i[0]
                user.bot.send_photo(message.from_user.id, photo=i[1], caption=f'msg_id = {msg_id}')

        elif message.text == '/get_video':
            res = user.get_video(message=message)

            for i in res:
                msg_id = i[0]
                user.bot.send_video(message.from_user.id, video=i[1], caption=f'msg_id = {msg_id}')

        elif message.text == '/get_document':
            res = user.get_document(message=message)
            print(f"res {res}")
            for i in res:
                msg_id = i[0]
                user.bot.send_document(message.from_user.id, document=i[1], caption=f'msg_id = {msg_id}')

    bot.infinity_polling()
if __name__ == "__main__":
    main()