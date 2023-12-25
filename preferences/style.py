from termcolor import colored
# this only exists to make syntax easier in other code.

# Colors
def blue(msg):
    msg = colored(msg, 'blue')
    return msg


def green(msg):
    msg = colored(msg, 'green')
    return msg


def yellow(msg):
    msg = colored(msg, 'yellow')
    return msg


def red(msg):
    msg = colored(msg, 'red')
    return msg


def magenta(msg):
    msg = colored(msg, 'magenta')
    return msg


def dark_grey(msg):
    msg = colored(msg, 'dark_grey')
    return msg


# Styles
def bold(msg):
    msg = colored(msg, attrs=['bold'])
    return msg


def dark(msg):
    msg = colored(msg, attrs=['dark'])
    return msg


def clear_line(): # use after: print("content", end='\r')
    clear = '\x1b[2K'
    print(end=clear)


def logo():
    logo_art = '''

██████╗ ██╗   ██╗██████╗ ██╗   ██╗████████╗██╗     ███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██║   ██║╚══██╔══╝██║     ██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║   ██║   ██║     █████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██╔══██╗██║   ██║   ██║   ██║     ██╔══╝  ██╔══██╗
██║        ██║   ██████╔╝╚██████╔╝   ██║   ███████╗███████╗██║  ██║
╚═╝        ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝'''
    logo_art = blue(logo_art)
    return logo_art

def hr():
    hr = "\n───────────────────────────────────────────────────────────────────\n"
    hr = blue(hr)
    return hr

def test():
    Option = input("Please run 'butler.py'\nPress 'Enter' to run a color test... ")
    print(logo())
    print(blue("This message is Blue"))
    print(green("This message is Green"))
    print(yellow("This message is Yellow"))
    print(red("This message is Red"))
    print(magenta("This message is Magenta"))
    print(dark_grey("This message is Dark Grey"))
    print(dark("This message is Dark"))

if __name__ == '__main__':
    test()