import sys

from interface import generateInterface


def main():
    # The first command line arugument passes the entire URL that activated the application
    # so we can use that to trigger the application to open and do something with the URL data.
    print("URL:", sys.argv[1:])

    generateInterface()


if __name__ == "__main__":
    main()
