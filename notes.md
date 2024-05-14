1. service  CRUD (Create  Read   Update   Delete)
2. entity
```py
 class moviese:
    def __init__(self,naem,id):
        self.naem=naem
        self.id=id
```
3. sub menu

Stages in Branchin
- Feature branch
- Dev Branch (For developers)
- Staging Branch (for QA team)
- Master Branch (for customers)

Git - version control software

# Doing git in command
- `git init`  - initialize git in a project
- `git add .` - stage all the files
- `git add file1.txt file2.txt` - stage the particular files 
- `git reset` - remeove all the staged files
- `git commit -m "Message"` - to commit the changes with message
- `git status` - gives the current status of staged and commited files
    
    ```
    On branch 5/13/2024
    Your branch is up to date with 'origin/5/13/2024'.
    Untracked files:
    (use "git add <file>..." to include in what will be committed)
        notes.md
    nothing added to commit but untracked files present (use "git add" to track)
    ```
- `git status -s` - gives short version of status
- `git log` - gives information about the commits that have been made from recent to oldest