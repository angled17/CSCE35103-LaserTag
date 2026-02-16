from database import Database
from game import App


def main():
    d = Database()
    d.connect()

    app = App(d)
    app.mainloop()

    d.close()

if __name__ == "__main__":
    main()