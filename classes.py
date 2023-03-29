import sql_fnc, sql_query

class User():
    """
    класс сохраняет/получает данные пользвателя 
    """
    def __init__(self, bot):
        self.bot = bot
        
    def save_user(self, message):
        self.userId = int(message.from_user.id)
        self.username = message.from_user.username
        self.first_name = message.from_user.first_name
        self.reg_time = int(message.date)
        con = sql_fnc.create_connection('users.db')
        res = sql_fnc.execute_query(con, sql_query.find_user, params=[self.userId])
        if res is None:

            sql_fnc.execute_query(con, sql_query.create_users_table, params=[])
            sql_fnc.execute_query(con, sql_query.save_user, params=[self.userId, self.username, self.first_name, self.reg_time])
        con.close()

    def save_photo(self, message):
        self.foto = message.photo[len(message.photo) - 1].file_id
        file_info = self.bot.get_file(self.foto)
        photo = self.bot.download_file(file_info.file_path)
        con = sql_fnc.create_connection('users.db')
        sql_fnc.execute_query(con, sql_query.create_photo_table, params=[])
        sql_fnc.execute_query(con, sql_query.up_foto, params=[message.from_user.id, photo, message.id])
        con.close()
        return photo
    
    def save_video(self, message):
        self.video = message.video.file_id
        file_info = self.bot.get_file(self.video)
        video = self.bot.download_file(file_info.file_path)
        con = sql_fnc.create_connection('users.db')
        sql_fnc.execute_query(con, sql_query.create_video_table, params=[])
        sql_fnc.execute_query(con, sql_query.up_video, params=[message.from_user.id, video, message.id])
        con.close()
        return video
    
    def save_document(self, message):
        self.document = message.document.file_id
        file_info = self.bot.get_file(self.document)
        document = self.bot.download_file(file_info.file_path)
        con = sql_fnc.create_connection('users.db')
        sql_fnc.execute_query(con, sql_query.create_document_table, params=[])
        sql_fnc.execute_query(con, sql_query.up_document, params=[message.from_user.id, document, message.id])
        con.close()
        return document
    
    def get_photo(self, message):
        con = sql_fnc.create_connection('users.db')
        res = sql_fnc.execute_query_select(con, sql_query.get_foto, params=[message.from_user.id])
        con.close()
        return res
    
    def get_video(self, message):
        con = sql_fnc.create_connection('users.db')
        res = sql_fnc.execute_query_select(con, sql_query.get_video, params=[message.from_user.id])
        con.close()
        return res
    
    def get_document(self, message):
        con = sql_fnc.create_connection('users.db')
        res = sql_fnc.execute_query_select(con, sql_query.get_document, params=[message.from_user.id])
        con.close()
        return res