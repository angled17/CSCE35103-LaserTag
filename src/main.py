from Database.database import Database
from game import App

import sys


def main():
    d = Database()
    d.connect()

    app = App(d)
    app.mainloop()

    d.close()


def debug_database():
    d = Database()
    d.connect()

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
    
    d.close()
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "db":
                debug_database()
    else:
        main()