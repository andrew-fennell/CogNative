from colorama import Fore

def colorize(text, type):
    """
    Print text in color.
    
    Colors:
        success - Green\n
        warning - Yellow\n
        error   - Red\n
        path    - Cyan\n
    """
    colors = {
        'success': Fore.LIGHTGREEN_EX,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'path': Fore.CYAN
    }
    
    return f"{colors[type]}{str(text)}{Fore.RESET}"
