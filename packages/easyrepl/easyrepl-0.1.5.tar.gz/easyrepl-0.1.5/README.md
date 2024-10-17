# Easy REPL
A simple python class for creating Read Evaluate Print Line (REPL) interfaces.

## Requirements

This module requires Python 3.7 or higher. 

Additionally this library makes use of the [GNU readline Interface](https://docs.python.org/3/library/readline.html), so it will only work on Unix based systems.

## Usage

This module exposes the `REPL` class which can be used to quickly create a REPL interface. REPL will read in a line of user input via a custom input function that allows you to edit the text by moving the cursor with the arrow keys, as well as view the history of previous inputs.

```python
from easyrepl import REPL

for line in REPL():
    # do something with line
    print(line)
```

which will create a simple echoing REPL interface that repeats any line you type into it.

```bash
>>> hello
hello
>>> world
world
>>>
```

The input allows common terminal shortcuts like:
- **Ctrl-D**: exit REPL
- **Ctrl-L**: clear screen
- **Ctrl-R**: search history
- **Left/Right Arrow**: move cursor left/right
- **Up/Down Arrow**: previous/next history
- **Ctrl-A**: move cursor to beginning of line
- **Ctrl-E**: move cursor to end of line
- **Alt-B**: move cursor backward one word
- **Alt-F**: move cursor forward one word
- **Ctrl-K**: delete from cursor to end of line
- **Ctrl-U**: delete from cursor to beginning of line
- **Ctrl-W**: delete from cursor to beginning of word
- **Alt-D**: delete from cursor to end of word
- **Ctrl-C**: no operation
- etc.


Additionally, multi-line input can be achieved by starting a line with triple quotes (`"""` or `'''`), and ending the final line with a matching triple quote. Triple quotes in the middle of a line will have no effect.


```
>>> """
... This is a multi-line input
... that will continue until
... the user enters three quotes
... at the end of a line
... """
This is a multi-line input
that will continue until
the user enters three quotes
at the end of a line
>>>
```

Note that a single newline will be stripped from the beginning and end of the input if present.