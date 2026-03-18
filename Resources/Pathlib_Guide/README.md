```yaml
id: pathlib_handout_001
title: Pathlib Survival Guide
course: programming_with_python
audience: beginner_programmers
purpose: help students navigate directories safely using pathlib
topics:
  - pathlib basics
  - safe path construction
  - locating project folders
  - existence checks
  - directory traversal
  - small exercises
notes:
  - no exception handling required
  - designed for students who frequently run code from the wrong directory
  - encourages defensive path checks
```

# Python `pathlib` Survival Guide  
### Finding Files Without Breaking Your Program

Python programs frequently need to access files such as:

- data files
- configuration files
- images
- logs
- output directories

The problem: **programs are often executed from different directories**, which can break file paths.

The `pathlib` module provides **safe, readable tools** to navigate directories and locate files.

---

# 1. Importing `Path`

Always start with:

```python
from pathlib import Path
```

The `Path` class represents a **filesystem path** (file or directory).

---

# 2. Where Is Your Program Running?

The **Current Working Directory (CWD)** is the folder where Python was launched.

```python
cwd = Path.cwd()
print(cwd)
```

Example output:

```
/Users/student/project
```

This matters because **relative paths start here**.

---

# 3. Building Paths Safely

Never build paths with string concatenation like this:

```python
# BAD
filename = "data/" + "survey.csv"
```

Use `Path` joining with `/`.

```python
data_dir = Path.cwd() / "data"
file_path = data_dir / "survey.csv"

print(file_path)
```

Output:

```
.../data/survey.csv
```

Python automatically uses the correct separator (`/` or `\`) for the OS.

---

# 4. Important Path Attributes

```python
p = Path("data/survey.csv")

p.name       # survey.csv
p.stem       # survey
p.suffix     # .csv
p.parent     # data
```

Example:

```python
print(p.name)
print(p.parent)
```

---

# 5. Moving Through Directories

### Parent folder

```python
p = Path.cwd()

print(p.parent)
```

### Multiple levels up

```python
p.parents[0]   # same as parent
p.parents[1]   # two levels up
```

Example:

```
/project
/project/src
/project/src/module
```

If current directory is `module`:

```
parents[0] → src
parents[1] → project
```

---

# 6. Checking If Files or Folders Exist

Before using a path, **verify it exists**.

### Check directory

```python
data_dir = Path.cwd() / "data"

if data_dir.exists() and data_dir.is_dir():
    print("data folder found")
else:
    print("data folder missing")
```

---

### Check file

```python
csv_file = Path.cwd() / "data" / "survey.csv"

if csv_file.exists() and csv_file.is_file():
    print("File found")
else:
    print("File missing")
```

This prevents programs from crashing.

---

# 7. Creating Folders If Needed

```python
output = Path("output")

output.mkdir(exist_ok=True)
```

Create nested directories:

```python
output.mkdir(parents=True, exist_ok=True)
```

---

# 8. Listing Files in a Directory

### List everything

```python
for item in Path("data").iterdir():
    print(item)
```

---

### Find files with a pattern

Find CSV files:

```python
for file in Path("data").glob("*.csv"):
    print(file)
```

---

### Recursive search

Search entire directory tree:

```python
for file in Path.cwd().rglob("*.csv"):
    print(file)
```

---

# 9. Finding a Folder Even If You're in the Wrong Directory

Students often run code from the wrong folder.

Example structure:

```
project
│
├─ data
│   └─ survey.csv
│
└─ src
    └─ program.py
```

If the program runs from `src`, it must **find the data folder above it**.

### Function to search upward

```python
def find_up(start: Path, target: str, max_levels=10):
    current = start.resolve()

    for _ in range(max_levels + 1):
        candidate = current / target

        if candidate.is_dir():
            return candidate

        if current.parent == current:
            break

        current = current.parent

    return None
```

Use it:

```python
data_dir = find_up(Path.cwd(), "data")

if data_dir:
    print("Found data folder:", data_dir)
else:
    print("Data folder not found")
```

---

# 10. Finding the Project Root Using `.git`

Many projects are inside a Git repository.

Example structure:

```
project
│
├─ .git
├─ data
├─ src
└─ README.md
```

We can **walk upward until `.git` is found**.

```python
def find_git_root(start=None, max_levels=25):
    current = (start or Path.cwd()).resolve()

    for _ in range(max_levels + 1):

        if (current / ".git").is_dir():
            return current

        if current.parent == current:
            return None

        current = current.parent

    return None
```

Usage:

```python
root = find_git_root()

if root:
    data = root / "data" / "survey.csv"
    print(data)
else:
    print("Not inside a Git repository")
```

---

# 11. Reading and Writing Files

### Read text

```python
file = Path("notes.txt")

if file.is_file():
    text = file.read_text()
```

---

### Write text

```python
Path("output.txt").write_text("Hello world\n")
```

---

# 12. A Simple “Safe Path” Pattern

This pattern prevents many beginner errors.

```python
from pathlib import Path

root = Path.cwd()

data = root / "data"
file = data / "survey.csv"

if not data.is_dir():
    print("Missing data folder")

elif not file.is_file():
    print("Missing survey.csv")

else:
    print("File ready:", file)
```

---

# Exercises

## Exercise 1 — Locate a Data Folder

Write a program that:

1. Prints the current working directory.
2. Searches upward for a folder named `"data"`.
3. Prints the path if found.

---

## Exercise 2 — Count CSV Files

Write code that counts how many `.csv` files exist inside the `data` folder.

Hint:

```python
glob("*.csv")
```

---

## Exercise 3 — Recursive Search

Search the entire project and print all `.json` files.

Hint:

```python
rglob("*.json")
```

---

## Exercise 4 — File Report

Write a script that prints:

```
file name
file size
file extension
parent folder
```

Hint:

```
path.stat().st_size
```

---

# Key Takeaway

Using `pathlib` allows you to:

- build paths safely
- navigate directories easily
- verify files exist before using them
- search for project folders dynamically

This prevents many **common beginner file path errors**.

---

```yaml
id: pathlib_mistakes_handout_001
title: "10 Pathlib Mistakes Students[^1] Always Make"
course: programming_with_python
audience: beginner_programmers
purpose: highlight common filesystem/path mistakes and show the correct pathlib approach
topics:
  - cwd_vs_script_location
  - incorrect_string_paths
  - missing_exists_checks
  - glob_vs_rglob
  - parent_navigation
  - pathlib_vs_open
  - resolve_paths
  - extension_handling
  - directory_iteration
  - project_root_discovery
footnote: "[^1]: faculty as well"
tone: practical_with_mild_sarcasm
```

# 10 `pathlib` Mistakes Students[^1] Always Make

[^1]: faculty as well

File paths seem simple… until a program works perfectly on **your machine**, then instantly fails on **every student’s machine**, the lab computers, and the grading server.

Most of these problems come from misunderstanding **where Python thinks it is** and **how paths are constructed**.

Let's fix that.

---

# 1. Assuming Python Runs From the Script’s Folder

Students often assume this:

```python
file = Path("data/survey.csv")
```

They assume the program runs from:

```
project/
│
├── data/
│   └── survey.csv
└── script.py
```

But Python actually runs from the **current working directory**, which may be:

```
project/src/
```

### Correct Approach

Check the working directory.

```python
from pathlib import Path

print(Path.cwd())
```

Better yet, locate the project root dynamically.

---

# 2. Building Paths With Strings

Bad:

```python
path = "data/" + filename
```

This works until:

- Windows path separators appear
- extra slashes appear
- directories are nested

### Correct

```python
path = Path("data") / filename
```

This automatically handles path separators.

---

# 3. Not Checking If Files Exist

Students frequently write:

```python
data = Path("data/survey.csv")
text = data.read_text()
```

If the file is missing:

```
FileNotFoundError
```

### Safer

```python
data = Path("data/survey.csv")

if data.exists():
    text = data.read_text()
else:
    print("Missing file:", data)
```

Even better:

```python
if data.is_file():
```

---

# 4. Confusing Files and Directories

Students often test existence but forget the difference.

```python
p = Path("data")

if p.exists():
```

But `p` might be a **file or directory**.

### Correct

```python
p.is_dir()
p.is_file()
```

Example:

```python
if p.is_dir():
    print("Folder exists")
```

---

# 5. Forgetting `.parent`

Students sometimes manually trim strings:

```python
folder = str(path).split("/")
```

This is fragile and unnecessary.

### Correct

```python
p = Path("data/survey.csv")

print(p.parent)
```

Result:

```
data
```

---

# 6. Forgetting `.resolve()`

Relative paths can contain things like:

```
data/../data/file.csv
```

To normalize:

```python
p = Path("data/../data/file.csv")

print(p.resolve())
```

Result:

```
.../data/file.csv
```

---

# 7. Searching Only One Directory

Students often use:

```python
Path("data").glob("*.csv")
```

This only searches **one folder**.

### Recursive search

```python
Path("data").rglob("*.csv")
```

This searches **all subfolders**.

---

# 8. Iterating Directories the Hard Way

Students sometimes attempt:

```python
import os

for f in os.listdir("data"):
```

`pathlib` is cleaner.

### Correct

```python
for item in Path("data").iterdir():
    print(item)
```

---

# 9. Hardcoding Absolute Paths

Students sometimes write:

```python
file = Path("/Users/student/project/data/file.csv")
```

This works on **one machine only**.

### Correct

Use relative paths.

```python
file = Path.cwd() / "data" / "file.csv"
```

Even better: detect the project root.

---

# 10. Not Locating the Project Root

Large projects often look like this:

```
project
│
├── .git
├── data
├── src
│   └── script.py
└── README.md
```

If the script runs from `src`, the data folder is **above it**.

### Correct Approach

Search upward for `.git`.

```python
def find_git_root(start=None):
    from pathlib import Path

    current = (start or Path.cwd()).resolve()

    while True:

        if (current / ".git").is_dir():
            return current

        if current.parent == current:
            return None

        current = current.parent
```

Usage:

```python
root = find_git_root()

if root:
    data = root / "data"
    print("Project root:", root)
```

This works **no matter where the program runs**.

---

# Bonus Tip: Debug Paths Quickly

If your program cannot find a file, print the path.

```python
print("Looking for:", file)
```

Or print the absolute path.

```python
print(file.resolve())
```

You will immediately see the mistake.

---

# Final Advice

Use `pathlib` to:

- build paths safely
- navigate directories
- check existence
- search directories
- normalize paths

The goal is simple:

> **Your program should work even if the user runs it from the wrong directory.**

Because they will.

Every time.

