import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        
    def set_activity(self, user_id, activity ):
        with self.connection:
            return self.cursor.execute("UPDATE users SET activity = ? WHERE user_id = ?",(activity,user_id,))
        
    def set_ignore(self, user_id, ignore ):
        with self.connection:
            return self.cursor.execute("UPDATE users SET ignore = ? WHERE user_id = ?",(ignore,user_id,))
        
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))
    
    def get_user_activity(self,user_id):
        with self.connection:
            return self.cursor.execute("SELECT activity  FROM users WHERE user_id = ?",(user_id,)).fetchmany(1)