import psycopg
from logger import log


class Database:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg.connect("dbname=photon user=student")
        self.cur = self.conn.cursor()
        log("Connected to database successfully!")

    def close(self):
        self.cur.close()
        self.conn.close()
        log("Closed database successfully!")

    # Adds a player to the "players" table in the "photon" database
    # Returns True if the name was successfully added to the database
    # Returns False if the name was not added to the database
    def add_player(self, name: str) -> bool:
        current_names = []
        current_ids = []
        max_id = None

        self.cur.execute("SELECT codename FROM players")
        result = self.cur.fetchall()

        # Adds the names the list
        for entry in result:
            current_names.append(entry[0])

        # Checks if name is in current names. Returns False if it is.
        if name in current_names:
            log(f'"{name}" is already being used! Try another name.')
            return False
        
        self.cur.execute("SELECT id FROM players")
        result = self.cur.fetchall()

        # Adds ids into list
        for entry in result:
            current_ids.append(entry[0])
        
        # Stores max ID
        max_id = max(current_ids)
        
        # Insert into players
        self.cur.execute("INSERT INTO players (id, codename) VALUES (%s, %s)", (max_id + 1, name))
        self.conn.commit()
        log(f"Added ID: {max_id + 1} | Player: {name} to the database!")
        
        return True
    

    # Removes a player from the "players" table in the "photon" database
    def remove_player(self, name: str) -> bool:
        pass


if __name__ == "__main__":
    db = Database()
    db.connect()

    db.add_player("lol")

    db.close()