import os
import sys

if os.name != "nt":
    import select
    import termios
    import tty
else:
    import msvcrt
    

def cls(title=None):
    """Clear the screen and optionally print a title."""
    if os.name != "nt":
        os.system("clear")
    else:
        os.system("cls")
    if title is not None:
        print(title)

def _get_key_linux():
    """Get a single keypress from the user on Linux/Unix."""
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                key = sys.stdin.read(1)
                if key == '\x1b':  # Arrow keys are sent as escape sequences
                    key += sys.stdin.read(2)  # Read the next two characters
                return key
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def _get_key():
    """Cross-platform key detection."""
    if os.name != "nt":
        return _get_key_linux()
    else:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys in Windows
                key = msvcrt.getch()
                return key.decode()
            return key.decode()
        return None

def _interpret_key(key):
    """Interpret the keypress and convert it into action."""
    if key in ['H', '\x1b[A']:  # Up arrow in Windows or Linux
        return "up"
    elif key in ['P', '\x1b[B']:  # Down arrow in Windows or Linux
        return "down"
    elif key == '\r':  # Enter key
        return "enter"
    return None

def menu(*text, title=None, desc=None, index=False, char="»", loc="l", align=True):
    try:
        if len(text) == 1 and type(text[0]) != str:
            text = list(text[0])
        else:
            text = list(text)
        
        if index:
            for y, x in enumerate(text):
                text[y] = f"{y+1}. {x}"

        if align:
            max_len = max(len(x) for x in text)
            for y, x in enumerate(text):
                text[y] = f"{' '*(len(char)+1)}{x}{' '*(max_len-len(x))}"

        nn = 0  # Default selection
        cls(title)
        for y, x in enumerate(text):
            if y == nn:
                if loc.lower() == "lr" or loc.lower() == "rl":
                    print(f"{char} {x[len(char)+1:]} {char}")
                elif loc.lower() == "r":
                    print(f"{x[len(char)+1:]} {char}")
                else:
                    print(f"{char} {x}")
            else:
                if loc.lower() == "r" and align:
                    print(x[len(char) + 1:])
                else:
                    print(x)
        
        if desc is not None:
            print(desc)

        while True:
            key = _get_key()
            if key:
                action = _interpret_key(key)
                if action == "up":
                    if nn > 0:
                        nn -= 1
                    cls(title)
                    for y, x in enumerate(text):
                        if y == nn:
                            if loc.lower() == "lr" or loc.lower() == "rl":
                                print(f"{char} {x[len(char)+1:]} {char}")
                            elif loc.lower() == "r":
                                print(f"{x[len(char)+1:]} {char}")
                            else:
                                print(f"{char} {x}")
                        else:
                            if loc.lower() == "r" and align:
                                print(x[len(char) + 1:])
                            else:
                                print(x)
                    if desc is not None:
                        print(desc)
                elif action == "down":
                    if nn < len(text) - 1:
                        nn += 1
                    cls(title)
                    for y, x in enumerate(text):
                        if y == nn:
                            if loc.lower() == "lr" or loc.lower() == "rl":
                                print(f"{char} {x[len(char)+1:]} {char}")
                            elif loc.lower() == "r":
                                print(f"{x[len(char)+1:]} {char}")
                            else:
                                print(f"{char} {x}")
                        else:
                            if loc.lower() == "r" and align:
                                print(x[len(char) + 1:])
                            else:
                                print(x)
                    if desc is not None:
                        print(desc)
                elif action == "enter":
                    break

    except Exception as e:
        raise e
    
    return nn
