import sqlite3, os, csv

from utils import get_temp_folder

DB_PATH = os.path.join(get_temp_folder(), 'database.db')

class RMDB:
    def __init__(self, db_name=DB_PATH):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def to_dict(self, row):
        rm = {
                'id': row[0],
                'number': row[1],
                'draw': row[2],
                'local': row[3],
                'destiny': row[4],
                'revision': row[5],
                'date': row[6],
                'username': row[7],
            }

        return rm

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS rms (
                            id INTEGER PRIMARY KEY,
                            number TEXT NOT NULL,
                            draw TEXT NOT NULL,
                            local TEXT NOT NULL,
                            destiny TEXT NOT NULL,
                            revision INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            username TEXT NOT NULL)''')
        self.conn.commit()

    def create(self, number, draw, local, destiny, revision, date, username):
        self.cur.execute(
            "INSERT INTO rms (number, draw, local, destiny, revision, date, username) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (number, draw, local, destiny, revision, date, username))
        self.conn.commit()

    def list(self):
        self.cur.execute("SELECT * FROM rms")

        rows = self.cur.fetchall()
        rms = []

        if rows != None:
            for row in rows:
                rms.append(self.to_dict(row))
        
        return rms

    def get(self, id):
        self.cur.execute("SELECT * FROM rms WHERE id=?", (id,))
        return self.cur.fetchone()

    def get_by_draw(self, draw):
        self.cur.execute("SELECT * FROM rms WHERE draw=?", (draw,))

        row = self.cur.fetchone()

        if row:
            return self.to_dict(row)
        
        return None

    def update(self, id, number, draw, local, destiny, revision, date, username):
        self.cur.execute(
            "UPDATE rms SET number=?, draw=?, local=?, destiny=?, revision=?, date=?, username=? WHERE id=?", 
            (number, draw, local, destiny, revision, date, username, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM rms WHERE id=?", (id,))

        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def load_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file) 
            for row in reader:
                self.create(
                    row['number'],
                    row['draw'],
                    row['local'],
                    row['destiny'],
                    row['revision'],  # Make sure this aligns with your CSV data
                    row['date']      # Make sure this aligns with your CSV data
                )

