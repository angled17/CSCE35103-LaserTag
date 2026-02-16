import psycopg
from log.logger import general_message


class Database:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.error_message = ""

    def connect(self):
        self.conn = psycopg.connect("dbname=photon user=student")
        self.cur = self.conn.cursor()
        general_message("Connected to database successfully!")

    def close(self):
        self.cur.close()
        self.conn.close()
        general_message("Closed database successfully!")

    # Adds a player to the "players" table in the "photon" database
    # Returns True if the name was successfully added to the database
    # Returns False if the name was not added to the database
    def add_player(self, id: int, name: str) -> bool:
        current_names = []
        current_ids = []

        self.cur.execute("SELECT codename FROM players")
        result = self.cur.fetchall()

        # Adds the names the list
        for entry in result:
            current_names.append(entry[0])

        # Checks if name is in current names. Returns False if it is.
        if name in current_names:
            self.error_message = 'Name "{}" is already being used!'.format(name)
            general_message(self.error_message)
            return False
        
        self.cur.execute("SELECT id FROM players")
        result = self.cur.fetchall()

        # Adds ids into list
        for entry in result:
            current_ids.append(entry[0])

        # Checks if id is in current ids. Returns False if it is.
        if id in current_ids:
            self.error_message = 'ID "{}" is already being used!'.format(id)
            general_message(self.error_message)
            return False
        
        
        # Insert into players
        self.cur.execute("INSERT INTO players (id, codename) VALUES (%s, %s)", (id, name))
        self.conn.commit()
        general_message(f"Added ID: {id} | Player: {name} to the database!")
        
        self.error_message = ""
        return True
    

    # Removes a player from the "players" table in the "photon" database
    def remove_player(self, name: str) -> bool:
        current_names = []

        self.cur.execute("SELECT codename FROM players")
        result = self.cur.fetchall()

        # Adds the names the list
        for entry in result:
            current_names.append(entry[0])

        if name not in current_names:
            self.error_message = f'"{name}" is not in the database!'
            general_message(self.error_message)
            return False
        
        self.cur.execute("DELETE FROM players WHERE codename = (%s) RETURNING id", (name,))
        
        # Stores ID of removed player
        result = self.cur.fetchall()[0][0]
        self.conn.commit()

        general_message(f"Removed ID: {result} | Player: {name} from the database!")

        self.error_message = ""
        return True
    
    # Returns List [(id: int, codename: str), ...]
    def get_players(self) -> dict:
        players = {}

        self.cur.execute("SELECT * FROM players")
        result = self.cur.fetchall()

        for entry in result:
            players[entry[0]] = entry[1]

        self.error_message = ""
        return players
    

    def get_player_from_id(self, id: int) -> str:
        self.cur.execute("SELECT * FROM players")
        result = self.cur.fetchall()

        for entry in result:
            if entry[0] == id:
                return entry[1]

        self.error_message = 'ID "{}" not found in database.'.format(id)
        return ""
    

    def get_error_message(self) -> str:
        return self.error_message


def debug_database(d: Database):
    running = True

    while running:
        print("--------------------")
        print("What do you want to do?")
        print("1. Add player to database.")
        print("2. Remove player from database.")
        print("3. Get All Players")
        print("q. Quit")
        print("> ", end="")

        response = input()

        match response.lower():
            case "q":
                running = False
            case "1":
                id = int(input("What ID number do you want to add to the database?: "))
                name = input("What name do you want to add to the database?: ")
                d.add_player(id, name)
            case "2":
                n = input("What name do you want to remove?: ")
                d.remove_player(n)
            case "3":
                print(d.get_players())



if __name__ == "__main__":
    db = Database()
    db.connect()

    debug_database(db)

    db.close()