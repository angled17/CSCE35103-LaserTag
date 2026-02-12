from database import Database
from gui import App, SplashFrame, PlayerEntryFrame
from tkinter.ttk import Style

def main():
    d = Database()
    d.connect()

    game = App()

    splash = SplashFrame(game)
    player_entry = PlayerEntryFrame(game, d)

    game.mainloop()

    d.close()

if __name__ == "__main__":
    main()