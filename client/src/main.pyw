import sys, traceback
from interface import mainUI
from util.db.database import Database
import time
def main():
    Database()  # initialize database and create tables if they don't exist
    time.sleep(2)  #  waits till db is intiilzied
    Database().close()  # close the connection since we don't need it right now, we will open it when we need to use it
    # The first command line arugument passes the entire URL that activated the application
    # so we can use that to trigger the application to open and do something with the URL data.
    print("URL:", sys.argv[1:])

    try:
        mUI = mainUI()
        mUI.runUI()
    except KeyboardInterrupt as err:
        traceback.print_exc()
        print(err)
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
