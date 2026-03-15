from Database.database import Database
from game import App
from Logging.logger import debug_message

import sys


debug = False
debug_splash_scene = False
debug_player_entry_scene = False
debug_play_action_scene = False


def main():
    d = Database()
    d.connect()

    debug_flags = {
        "Debug": debug,
        "SplashScene": debug_splash_scene,
        "PlayerEntryScene": debug_player_entry_scene,
        "PlayActionScene": debug_play_action_scene
    }

    app = App(d, debug_flags)
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
        print("2. Remove player from database using name.")
        print("3. Remove player from database using ID.")
        print("4. Get All Players")
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
                d.remove_player_from_name(n)
            case "3":
                id = int(input("What ID do you want to remove?: "))
                d.remove_player_from_id(id)
            case "4":
                print(d.get_players())
    
    d.close()
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "db":
                debug_database()
            case "debug":
                debug = True

                if len(sys.argv) > 2:
                    match sys.argv[2]:
                        case "SplashScene":
                            debug_message("Debugging Splash Scene")
                            debug_splash_scene = True
                        case "PlayerEntryScene":
                            debug_message("Debugging Player Entry Scene")
                            debug_player_entry_scene = True
                        case "PlayActionScene":
                            debug_message("Debugging Play Action Scene")
                            debug_play_action_scene = True
                        case _:
                            debug_message("Invalid Argument(s)! Running normally...")
                main()
    else:
        main()