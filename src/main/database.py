import sqlite3, os

from utils import get_temp_folder

class RMDB:
    def __init__(self, db_name=os.path.join(get_temp_folder(), 'database.db')):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS rms (
                            id INTEGER PRIMARY KEY,
                            number TEXT NOT NULL,
                            draw TEXT NOT NULL,
                            aplication TEXT NOT NULL,
                            local TEXT NOT NULL,
                            destiny TEXT NOT NULL,
                            revision INTEGER NOT NULL)''')
        self.conn.commit()

    def create(self, number, draw, aplication, local, destiny, revision):
        self.cur.execute(
            "INSERT INTO rms (number, draw, aplication, local, destiny, revision) VALUES (?, ?, ?, ?, ?, ?)", 
            (number, draw, aplication, local, destiny, revision))
        self.conn.commit()

    def list(self):
        self.cur.execute("SELECT * FROM rms")
        return self.cur.fetchall()

    def get(self, id):
        self.cur.execute("SELECT * FROM rms WHERE id=?", (id,))
        return self.cur.fetchone()

    def get_by_draw(self, draw):
        self.cur.execute("SELECT * FROM rms WHERE draw=?", (draw,))
        return self.cur.fetchone()

    def update(self, id, number, draw, aplication, local, destiny, revision):
        self.cur.execute(
            "UPDATE rms SET number=?, draw=?, aplication=?, local=?, destiny=?, revision=? WHERE id=?", 
            (number, draw, aplication, local, destiny, revision, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM rms WHERE id=?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

# Example usage:
# user_db = UserDB()
# user_db.create_user("Alice", "alice@example.com")
# print(user_db.list_users())
# user_db.update_user(1, "Alice Smith", "alice.smith@example.com")
# print(user_db.get_user(1))
# user_db.delete_user(1)
# user_db.close()
