# L1 · Your computer as a workshop

**Goal:** feel at home in the terminal, install the tools you'll use all course, and get the course files onto your computer.
**Time:** about 6–8 hours.

## Why the terminal?

The **terminal** is a window where you type commands instead of clicking. Engineers use it because it's fast, precise and repeatable: a command you typed once can be saved, shared, and run by a computer on its own. Nearly every tool in this course is started from the terminal.

### Open one

=== "Windows"

    Press the Start button, type **PowerShell**, and open **Windows PowerShell**. You'll see a line ending in `>`, such as `PS C:\Users\you>`. That's the **prompt**: the terminal is waiting for a command.

=== "macOS"

    Press ⌘ + Space, type **Terminal**, and press Enter. The prompt ends in `%` or `$`.

=== "Linux"

    Press Ctrl + Alt + T (on most distributions), or find **Terminal** in your apps. The prompt ends in `$`.

### Your first commands

Type each one and press Enter. These work the same in PowerShell, macOS and Linux:

| Command | What it does |
|---|---|
| `pwd` | **P**rint **w**orking **d**irectory: shows which folder you're in |
| `ls` | **L**i**s**t what's in this folder |
| `cd Documents` | **C**hange **d**irectory: move into the `Documents` folder |
| `cd ..` | Move up one level (`..` means "the folder above") |
| `cd ~` | Go to your home folder (`~` means home) |
| `mkdir practice` | **M**a**k**e a new **dir**ectory (folder) called `practice` |
| `cat notes.txt` | Print the contents of a text file |
| `clear` | Clear the screen |

Try this sequence and watch what each step prints:

```bash
cd ~
pwd
mkdir practice
cd practice
pwd
cd ..
ls
```

!!! tip "Two keys that save hours"
    **Tab** completes names: type `cd Doc` and press Tab. **Up arrow** brings back your previous command.

### Paths

A **path** is the address of a file or folder.

- `labs/launchpad/l1` is a **relative** path: it starts from wherever you are now.
- `/Users/ava/Projects` (macOS), `/home/ava/Projects` (Linux) or `C:\Users\ava\Projects` (Windows) is an **absolute** path: it starts from the top of the drive.
- Windows uses `\` between folders and macOS/Linux use `/`. **In this course we write `/`**: PowerShell and Python on Windows understand it too.
- Folder names with spaces need quotes: `cd "My Projects"`.

## Install your tools

You need three tools. Follow **step 1 of the [setup page](../setup/index.md#1-install-the-tools)** for your system, then come back.

- **Git** keeps the history of your work (L5 covers it properly).
- **Python** is the programming language of this course.
- **VS Code** is the editor where you'll write code.

Check them in a **new** terminal window:

=== "Windows"

    ```powershell
    git --version
    py -3.13 --version
    code --version
    ```

=== "macOS"

    ```bash
    git --version
    python3 --version
    code --version
    ```

    If `code` isn't found, open VS Code, press ⌘ + Shift + P, run **Shell Command: Install 'code' command in PATH**, then open a new terminal.

=== "Linux"

    ```bash
    git --version
    python3 --version
    code --version
    ```

Each prints a version number. "Not recognized" or "command not found" means the tool isn't installed, or the terminal was opened before installing. Close it, open a new one, and try again.

## Get the course files

Do **step 2 of the [setup page](../setup/index.md#2-get-the-course-files)**: it makes a `Projects` folder and **clones** (downloads) the course into it. You'll learn what cloning really does in L5. For now, it's one command to copy and paste.

Then do **step 3 ([Python environment](../setup/index.md#3-python-environment))**. It creates a *virtual environment*: a private set of Python add-ons for this course. You'll understand it fully in L4. Right now, remember one habit:

!!! warning "Every time you open a new terminal for the course"
    1. `cd` into the course folder.
    2. Activate the environment: `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (macOS/Linux).

    Your prompt then starts with `(.venv)`.

## A tour of VS Code

1. Open VS Code and choose **File → Open Folder…**, then pick the `FDE-Training` folder.
2. The left sidebar is the **Explorer**: the same files you see with `ls`.
3. Open the built-in terminal with **View → Terminal**. It starts in the course folder already. Activate the environment there.
4. Install the **Python** extension from Microsoft (Extensions icon on the left, search "Python"). It colours your code and points out mistakes as you type.

## Lab: the treasure hunt

A secret phrase is hidden in `labs/launchpad/l1/workshop/`, split across three files in different folders. Find it **using only the terminal**.

1. From the course folder:

    ```bash
    cd labs/launchpad/l1/workshop
    cat README.txt
    ```

2. Use `ls`, `cd <folder>`, `cd ..` and `cat <file>` to explore. Some folders are decoys.
3. When you have all three parts, go up one level to the `l1` folder (`cd ..`) and save your answer to a file:

    ```bash
    echo "PART1-PART2-PART3" > answers.txt
    ```

    (Replace `PART1-PART2-PART3` with the real phrase. `>` sends a command's output into a file.)

4. Still in the `l1` folder, make a notes folder and your first note:

    ```bash
    mkdir my-notes
    echo "Today I learned to use the terminal." > my-notes/first-note.txt
    ```

5. Go back to the course folder and run the checker:

    ```bash
    cd ../../..
    python labs/launchpad/l1/check_l1.py
    ```

    (`../../..` means "up three levels".) You're aiming for two `[x]` ticks.

??? success "What success looks like"
    ```text
    [x] Secret phrase found
    [x] my-notes/first-note.txt exists and has something in it

    L1 complete. You can find your way around a computer from the terminal!
    ```

??? failure "If something goes wrong"
    | You see | Fix |
    |---|---|
    | `python: command not found` or the Microsoft Store opens | Activate the environment first (see above); inside it, `python` always works |
    | `No such file or directory` / `Cannot find path` | You're in a different folder than you think. Run `pwd`, then `cd` to the right place |
    | The phrase isn't accepted | Three parts in order (1, 2, 3), joined with dashes, no spaces |

## Exercises

1. **Core.** Without the mouse, create `~/practice/week1/` and a file `plan.txt` inside it saying how many hours a week you'll study. Then print it with `cat`.
2. **Core.** Open the course folder in VS Code and find `labs/launchpad/l1/workshop/README.txt` in the Explorer. Change one word and save it, then `cat` it in the terminal to see your change. (Change it back afterwards.)
3. **Stretch.** Find out what `ls -l` (macOS/Linux) or `ls | Format-List` (PowerShell) shows that plain `ls` doesn't.

## Checkpoint

- [ ] I can open a terminal and know which folder I'm in
- [ ] I can move between folders with `cd`, list them with `ls` and read files with `cat`
- [ ] Git, Python and VS Code are installed, and the course files are on my computer
- [ ] I know how to activate the course's virtual environment
- [ ] The L1 checker shows two ticks
