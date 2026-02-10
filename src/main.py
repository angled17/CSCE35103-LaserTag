from database import Database
from gui import Game

def main():
    d = Database()
    g = Game(d)


if __name__ == "__main__":
    main()