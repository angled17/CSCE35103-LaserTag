import psycopg
from logger import general_message


class Database:
    def __init__(self):
        self.conn = None
        self.cur = None

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
            general_message(f'"{name}" is already being used!')
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
        general_message(f"Added ID: {max_id + 1} | Player: {name} to the database!")
        
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
            general_message(f'"{name}" is not in the database!')
            return False
        
        self.cur.execute("DELETE FROM players WHERE codename = (%s) RETURNING id", (name,))
        
        # Stores ID of removed player
        result = self.cur.fetchall()[0][0]
        self.conn.commit()

        general_message(f"Removed ID: {result} | Player: {name} from the database!")

        return True


def debug_database(d: Database):
    running = True

    while running:
        print("--------------------")
        print("What do you want to do?")
        print("1. Add player to database.")
        print("2. Remove player from database.")
        print("q. Quit")
        print("> ", end="")

        response = input()

        match response.lower():
            case "q":
                running = False
            case "1":
                n = input("What name do you want to add to the database?: ")
                d.add_player(n)
            case "2":
                n = input("What name do you want to remove?: ")
                d.remove_player(n)



if __name__ == "__main__":
    db = Database()
    db.connect()

    debug_database(db)

    db.close()