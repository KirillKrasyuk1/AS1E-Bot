import sqlite3


class Database:
    def __init__(self, file_db):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()


    def add_user(self, user_id):
       with self.connection:
           # return self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id, ))
           return self.cursor.execute(f'INSERT INTO users (user_id) VALUES ({user_id})')

    def is_user_exist(self, user_id):
        with self.connection:
            response =  self.cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id, )).fetchall()
            return bool(len(response))

    def add_time(self, time, user_id):
        with self.connection:
            # return self.cursor.execute(f'UPDATE users SET (time) = ({time}) WHERE (user_id) = ({user_id});')
            return self.cursor.execute('UPDATE users SET (time) = (?) WHERE (user_id) = (?)', (time, user_id,))

    def add_city(self, city, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET (city) = (?) WHERE (user_id) = (?)', (city, user_id,))

