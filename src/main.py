from database import Database
# from gui import App, SplashFrame, PlayerEntryFrame
from gui.SplashFrame import SplashFrame
from gui.PlayerEntryFrame import PlayerEntryFrame
from gui.GameActionFrame import GameActionFrame
from game import App


def main():
    d = Database()
    d.connect()

    game = App()

    splash = SplashFrame(game)
    player_entry = PlayerEntryFrame(game, d)
    game_action = GameActionFrame(game, d)

    game.mainloop()

    d.close()

if __name__ == "__main__":
    main()