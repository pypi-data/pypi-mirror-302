"""
Color escape code class
"""

# pylint: disable=too-few-public-methods
# pylint: disable=protected-access


class Colors:
    """Class for ANSI color codes, used to output colored and formatted text on supported terminals.

    source: https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007

    This class provides various ANSI escape codes for colors and text formatting,
    enabling the addition of color or visual changes to text on compatible terminals.
    It checks `sys.stdout.isatty()` to determine whether to enable these escape codes
    when not outputting to a terminal.
    On Windows systems, if running in a terminal is detected, the `SetConsoleMode`
    function is used to enable VT mode for supporting ANSI escape codes.

    Attributes:
        BLACK, RED, GREEN, BROWN, BLUE, PURPLE, CYAN, LIGHT_GRAY,
        DARK_GRAY, LIGHT_RED, LIGHT_GREEN, YELLOW, LIGHT_BLUE,
        LIGHT_PURPLE, LIGHT_CYAN, LIGHT_WHITE, BOLD, FAINT, ITALIC,
        UNDERLINE, BLINK, NEGATIVE, CROSSED, RESET
    """

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    RESET = "\033[0m"

    @classmethod
    def _create_class_methods(cls):
        """Dynamically create class methods for each color and formatting option."""
        for attr_name in dir(cls):
            # Only process attributes that are color codes (uppercase, no underscore)
            if attr_name.isupper() and not attr_name.startswith("_"):
                # Get the color code
                color_code = getattr(cls, attr_name)

                # Define a class method that wraps text with the color code
                def color_method(cls, text, color_code=color_code):
                    return f"{color_code}{text}{cls.RESET}"

                # Attach the method to the class with a lowercase name
                setattr(cls, attr_name.lower(), classmethod(color_method))

    # Cancel SGR codes if not writing to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # Set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32


# Dynamically create the class methods when the class is defined
Colors._create_class_methods()

if __name__ == "__main__":
    for i in dir(Colors):
        if i[0:1] != "_" and i != "RESET":
            print(f"{i:>16} {getattr(Colors, i) + i + Colors.RESET}")

    SAMPLE_TEXT = """Welcome to The World of Color Escape Code."""
    print(f"{Colors.BOLD}{Colors.PURPLE}{Colors.NEGATIVE}{SAMPLE_TEXT}{Colors.RESET}")
