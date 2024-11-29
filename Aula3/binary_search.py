def getInput(bottow, top):
    n = int( top - int((top - bottow)/2))
    print("Your number is ", int(n), ", lower or higher? (yes (y), lower (l), higher (h))")
    x = input()
    if x in ("yes", "y"):
        correctNumber()
    if x in ("lower", "l"):
        getInput(bottow, n)
    if x in ("higher", "h"):
        getInput(n, top)
    else:
        print("awsner only with 'yes (y)', 'lower (l)' or 'higher (h)'")
        getInput(bottow, top)


def correctNumber():
    print("Play Again? (yes (y) or no (n))")
    x = input()
    if (x in ("yes", "y")):
        start()
    else:
        print(("Thanks for playing!"))
        exit()
    pass

def start():
    getInput(0, 100)

start()