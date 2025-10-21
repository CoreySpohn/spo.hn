+++
title = 'Colorful Python Logging'
date = 2024-08-19T12:14:46-04:00
draft = false
summary = "How I do logging in Python"
+++

# Goal
Create a logger for a python library that results in terminal output like this:
![Logger colors]( /images/logger.png )
The library `yippy` has its own color, the logger has different colors for `INFO`, `WARNING`, `ERROR`, etc statements, and the logger's level can be set by the user on a per-library basis. To do this we will use ANSI escape codes and a custom logger built with the standard Python `logging` library.
## ANSI escape codes
An ANSI escape code is a sequence of characters used to control the formatting, color, and other output options on text terminals that support ANSI standards. These codes are used to add color, move the cursor, and alter text appearance in terminal outputs.
### Format of an ANSI Escape Code
An ANSI escape code typically starts with the **escape character** (`\033` or `\x1b`) followed by a **bracket** (`[`), and then a series of numerical values that specify the formatting options, followed by an ending character such as `m` for text formatting.

For coloring, the code looks something like this:
```
\033[<code>m
```
- **`\033`**: The escape character that signals the terminal to interpret the following characters as a special instruction.
- **`[`**: Indicates the beginning of the sequence.
- **`<code>`**: Numeric codes that determine the text color or style (e.g., bold, underlined).
- **`m`**: Marks the end of the code and applies the formatting.
#### Example of Common Codes
- **Foreground (Text) Colors:**
    - Black: `\033[30m`
    - Red: `\033[31m`
    - Green: `\033[32m`
    - Yellow: `\033[33m`
- **Background Colors** (similar to text colors but starting with 40–47):
    - Red Background: `\033[41m`
- **Reset/Normal Text**:
    - To reset formatting: `\033[0m`
#### Example in Code
```python
print("\033[31mThis text is red!\033[0m")
```
This will display the text "This text is red!" in red, and then reset the color back to normal with `\033[0m`.
### Further information
The best resource I've found is this graphic: [ANSI Escape Codes · GitHub](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797?permalink_comment_id=4619910#gistcomment-4619910)
## Logger.py
My typical logger.py file looks like this:
```python
"""Logging module."""

import logging

lib_name = "yippy"
# See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797 for
# info on the color codes
lib_color = "229"


# ANSI escape sequences for colors
class ColorCodes:
    """ANSI escape sequences for colors."""

    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    LIB = f"\033[38;5;{lib_color}m"


# Custom formatter to add colors
class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages."""

    COLORS = {
        logging.DEBUG: ColorCodes.BLUE,
        logging.INFO: ColorCodes.GREEN,
        logging.WARNING: ColorCodes.YELLOW,
        logging.ERROR: ColorCodes.RED,
        logging.CRITICAL: ColorCodes.MAGENTA,
    }

    def format(self, record: logging.LogRecord):
        """Format the log message with colors."""
        log = super().format(record)
        color = self.COLORS.get(record.levelno, ColorCodes.WHITE)
        return f"{ColorCodes.LIB}\033[48;5;16m[{lib_name}]\033[0m {color}{log}"


logger = logging.getLogger(f"{lib_name}")

shell_handler = logging.StreamHandler()
file_handler = logging.FileHandler("debug.log")

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

shell_fmt = "%(levelname)s [%(asctime)s] \033[0m%(message)s"
file_fmt = (
    f"[{lib_name}] %(levelname)s %(asctime)s [%(filename)s:"
    "%(funcName)s:%(lineno)d] %(message)s"
)
shell_formatter = ColorFormatter(shell_fmt)
file_formatter = logging.Formatter(file_fmt)

shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)

logger.propagate = True
```
The colors can be adjusted by changing the ColorCodes class, the ColorFormatter class applies the colors to the messages (and identifies the library with the custom "LIB" color), and the code at the end creates a shell logger and a log file (if you're dumping to a debug.log file or something). The format of the log messages is different for the shell and log file, as seen in the `shell_fmt` and `file_fmt` strings. The `file_fmt` includes more debug information such as the filename, function name, and line number of the log statement. For example, are the log statements in debug.log from the same call as in the screenshot at the start of this tutorial
```text
[yippy] INFO 2024-08-19 11:25:26,964 [coronagraph.py:__init__:67] Creating LUVOIR-B-VC6_timeseries coronagraph
[yippy] WARNING 2024-08-19 11:25:26,966 [header.py:extract_unit:111] Using default unit for D: m. Could not extract unit from comment: "circumscribed diameter D of the primary mirror"
[yippy] DEBUG 2024-08-19 11:25:26,966 [header.py:extract_unit:108] Extracted micron from "central wavelength of the bandpass in microns" for LAMBDA
[yippy] DEBUG 2024-08-19 11:25:26,966 [header.py:extract_unit:108] Extracted micron from "shortest wavelength of the bandpass in microns" for MINLAM
[yippy] DEBUG 2024-08-19 11:25:26,966 [header.py:extract_unit:108] Extracted micron from "shortest wavelength of the bandpass in microns" for MAXLAM
[yippy] DEBUG 2024-08-19 11:25:26,966 [header.py:extract_unit:108] Extracted mas from "RMS jitter per axis in mas" for JITTER
[yippy] DEBUG 2024-08-19 11:25:26,967 [header.py:extract_unit:108] Extracted pm from "wfe calculated in pm" for WFE
[yippy] INFO 2024-08-19 11:25:27,015 [offax_base.py:__init__:114] LUVOIR-B-VC6_timeseries is radially symmetric
[yippy] INFO 2024-08-19 11:25:27,015 [coronagraph.py:__init__:95] Created LUVOIR-B-VC6_timeseries
```
### Using the logger
In your library you'll want to modify the logger (e.g. change `lib_name`, `lib_color`, `shell_fmt`, and `file_fmt`) and save it as something like `logger.py` and add the necessary info to the relevant `__init__.py` files to make it importable. I typically have it saved as `src/package_name/logger.py` 
 so that in my files I can run 
```python
from yippy.logger import logger
```
#### Adding log statements
After importing your `logger` you can add statements like
```python
logger.info(f"Creating {coro.name} coronagraph")
logger.debug(f'Extracted {unit} from "{comment}" for {key}')
logger.warning(f"Unhandled header fields: {unhandled_keys}")
```
#### Please make it shut up
Say you're working on a project that relies on your library, but you don't want to get a million `INFO` statements in your terminal from your library. In your project script/driver file you can import the logger from your overly-talkative library and shut it up with
```python
import logging

yippy_logger = logging.getLogger("yippy")
yippy_logger.setLevel(logging.WARNING)
```
This also can be done by a library, so for example if my `coronagraphoto` library relies on `yippy` but doesn't need the `INFO` statements I can run `yippy_logger.setLevel(logging.WARNING)` at the point that `coronagraphoto` needs to use `yippy`. That can then be overruled by the driver script as well. 

# TL;DR
1. Copy the `logger.py` code to your library (e.g. `src/my_library/logger.py`)
2. Adjust the `lib_color` (choose one of [these colors](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797?permalink_comment_id=4619910#gistcomment-4619910)) and `lib_name` (to your library's name)
3. Change your `src/my_library/__init__.py` file to include `logger` in `__all__` and add a line `from .logger import logger`
4. Import the logger in your library files (`from my_library.logger import logger`)
5. Add log statements to your code (`logger.info("This is an info message")`)
