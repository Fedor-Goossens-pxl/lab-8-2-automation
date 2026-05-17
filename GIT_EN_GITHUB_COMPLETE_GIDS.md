# GIT EN GITHUB GIDS: REPOSITORY AANMAKEN EN PUSHEN

Fedor Goossens - 2SNEb - PXL

---

## DEEL 1: VOORBEREIDING

### Stap 1.1: Git installeren

Download en installeer Git:
```
https://git-scm.com
```

Verificatie in PowerShell:

```powershell
git --version
# Output: git version 2.xx.x
```

### Stap 1.2: Git configureren (eenmalig)

In PowerShell:

```powershell
git config --global user.name "Fedor Goossens"
git config --global user.email "fedor.goossens@student.pxl.be"
```

Verificatie:

```powershell
git config --global user.name
# Output: Fedor Goossens

git config --global user.email
# Output: fedor.goossens@student.pxl.be
```

### Stap 1.3: GitHub account

- GitHub account: https://github.com
- Username: fedor-goossens-pxl
- Email: fedor.goossens@student.pxl.be

---

## DEEL 2: LOKALE GIT REPOSITORY AANMAKEN

### Stap 2.1: Project folder aanmaken

In PowerShell:

```powershell
mkdir C:\Users\fedor\lab-8-2-automation
cd C:\Users\fedor\lab-8-2-automation
```

### Stap 2.2: Git repository initialiseren

```powershell
git init
```

Output verwacht:

```
Initialized empty Git repository in C:\Users\fedor\lab-8-2-automation\.git
```

Dit creëert een `.git` folder met alle Git configuratie.

### Stap 2.3: Check Git status

```powershell
git status
```

Output verwacht:

```
On branch master

No commits yet

nothing to commit
```

---

## DEEL 3: FILES TOEVOEGEN AAN REPOSITORY

### Stap 3.1: Maak bestanden aan

Plaats je Python scripts en configs in de folder:

```powershell
# Voorbeeld - je plaatst deze files:
# task36_netconf.py
# config-iosxe.xml
# README.md
```

### Stap 3.2: Check welke files ontracked zijn

```powershell
git status
```

Output verwacht:

```
On branch master
No commits yet
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        task36_netconf.py
        config-iosxe.xml
        README.md

nothing added to commit but untracked files present
```

### Stap 3.3: Voeg files toe aan staging area

Alle files toevoegen:

```powershell
git add .
```

Of individuele files:

```powershell
git add task36_netconf.py
git add config-iosxe.xml
git add README.md
```

### Stap 3.4: Check staging status

```powershell
git status
```

Output verwacht:

```
On branch master
No commits yet
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   task36_netconf.py
        new file:   config-iosxe.xml
        new file:   README.md
```

---

## DEEL 4: COMMITS MAKEN

### Stap 4.1: Maak eerste commit

```powershell
git commit -m "Initial commit - Task 36 NETCONF setup"
```

Output verwacht:

```
[master (root-commit) abc1234] Initial commit - Task 36 NETCONF setup
 3 files changed, 150 insertions(+)
 create mode 100644 task36_netconf.py
 create mode 100644 config-iosxe.xml
 create mode 100644 README.md
```

### Stap 4.2: Check commit history

```powershell
git log
```

Output verwacht:

```
commit abc1234def5678 (HEAD -> master)
Author: Fedor Goossens <fedor.goossens@student.pxl.be>
Date:   Sun May 17 17:30:00 2026 +0200

    Initial commit - Task 36 NETCONF setup
```

Of korter:

```powershell
git log --oneline
```

Output verwacht:

```
abc1234 Initial commit - Task 36 NETCONF setup
```

---

## DEEL 5: GITHUB REPOSITORY AANMAKEN

### Stap 5.1: Maak repository aan op GitHub.com

1. Log in op https://github.com
2. Klik "+" menu → "New repository"
3. **Repository name:** `lab-8-2-automation`
4. **Description:** "LAB 8.2 IOS-XE Automation with NETCONF and RESTCONF"
5. **Public** (optioneel - kan ook Private)
6. **DO NOT** initialize with README (want je hebt al één)
7. Klik "Create repository"

GitHub geeft je deze URL:
```
https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
```

---

## DEEL 6: LOKALE REPO VERBINDEN MET GITHUB

### Stap 6.1: Voeg GitHub remote toe

In PowerShell (in je project folder):

```powershell
git remote add origin https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
```

### Stap 6.2: Check remote

```powershell
git remote -v
```

Output verwacht:

```
origin  https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git (fetch)
origin  https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git (push)
```

### Stap 6.3: Rename branch naar main (optioneel)

```powershell
git branch -M main
```

---

## DEEL 7: PUSHEN NAAR GITHUB

### Stap 7.1: Push naar GitHub

```powershell
git push -u origin main
```

Output verwacht:

```
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 1.50 KiB | 750 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0

remote: Create a pull request for 'main' on GitHub by visiting:
remote:   https://github.com/Fedor-Goossens-pxl/lab-8-2-automation/pull/new/main

To https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
 * [new branch]      main -> main

Branch 'main' set up to track remote tracking branch 'main' from 'origin'.
```

### Stap 7.2: Volgende keer (simpeler)

Volgende pushes zijn simpeler:

```powershell
git push
```

Dat's het! Git onthoudt de remote.

---

## DEEL 8: WORKFLOW VOOR VOLGENDE UPDATES

Telkens je iets aanpast:

### Workflow stap 1: Check status

```powershell
git status
```

### Workflow stap 2: Add changes

```powershell
git add .
```

### Workflow stap 3: Commit

```powershell
git commit -m "Beschrijf wat je veranderd hebt"
```

### Workflow stap 4: Push

```powershell
git push
```

### Voorbeeld volledige workflow:

```powershell
# Edit task36_netconf.py

git status
# Output: modified: task36_netconf.py

git add .
git commit -m "Fix error handling in NETCONF script"
git push

git log --oneline -1
# Output: def5678 Fix error handling in NETCONF script
```

---

## DEEL 9: PRAKTISCHE COMMANDO REFERENCE

### Repository aanmaken

```powershell
# 1. Folder maken
mkdir my-project
cd my-project

# 2. Git init
git init

# 3. Configuratie
git config --global user.name "Fedor Goossens"
git config --global user.email "fedor.goossens@student.pxl.be"
```

### Files toevoegen en committen

```powershell
# 1. Files plaatsen in folder

# 2. Add
git add .

# 3. Commit
git commit -m "Initial commit"
```

### GitHub verbinden en pushen

```powershell
# 1. Maak repo aan op GitHub.com

# 2. Voeg remote toe
git remote add origin https://github.com/username/repo.git

# 3. Branch naar main
git branch -M main

# 4. Push
git push -u origin main
```

### Volgende updates

```powershell
# 1. Edit files

# 2. Workflow
git add .
git commit -m "Update message"
git push
```

### Logs bekijken

```powershell
# Alle commits
git log

# Korte format
git log --oneline

# Laatste 3 commits
git log --oneline -3

# Grafisch
git log --graph --oneline --all
```

---

## DEEL 10: ECHT VOORBEELD - FEDOR'S WORKFLOW

### Sessie 1: Repository aanmaken

```powershell
# Setup
mkdir C:\Users\fedor\lab-8-2-automation
cd C:\Users\fedor\lab-8-2-automation
git init

# Configuratie
git config --global user.name "Fedor Goossens"
git config --global user.email "fedor.goossens@student.pxl.be"

# Files plaatsen
# (copy task36_netconf.py, config-iosxe.xml, README.md)

# First commit
git add .
git commit -m "Task 36 NETCONF initial setup"

# GitHub remote
git remote add origin https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
git branch -M main
git push -u origin main
```

Output:
```
✓ Repository aangemaakt op GitHub
✓ Files gepusht
✓ Branch main actief
```

### Sessie 2: Task 38 toevoegen

```powershell
# Folder maken
mkdir task38-restconf

# Files plaatsen
# (copy task38_restconf.py, config-restconf.json, README.md)

# Commit
git add .
git commit -m "Add Task 38 RESTCONF implementation"
git push

# Check
git log --oneline -2
```

Output:
```
def5678 Add Task 38 RESTCONF implementation
abc1234 Task 36 NETCONF initial setup
```

### Sessie 3: Stappenplannen toevoegen

```powershell
# Files plaatsen
# (copy alle .md stappenplannen)

# Commit
git add .
git commit -m "Add documentation and step-by-step guides"
git push

# Verificatie
git log --oneline -3
```

---

## TROUBLESHOOTING

### Probleem: "fatal: not a git repository"

```
Error: fatal: not a git repository
```

Oorzaak: Je bent niet in een Git folder

Oplossing:
```powershell
cd C:\Users\fedor\lab-8-2-automation
git status
```

---

### Probleem: "Permission denied" bij push

```
Error: Permission denied (publickey)
```

Oorzaak: GitHub authentication mislukt

Oplossing:
```powershell
# Probeer HTTPS in plaats van SSH
git remote set-url origin https://github.com/Fedor-Goossens-pxl/lab-8-2-automation.git
git push
```

---

### Probleem: "Already exists" bij remote add

```
Error: fatal: remote origin already exists
```

Oorzaak: Remote is al toegevoegd

Oplossing:
```powershell
git remote -v
# Check huidige remote

git remote remove origin
# Verwijder oude remote

git remote add origin https://github.com/...
# Voeg correct toe
```

---

## CHECKLIST - GIT & GITHUB SETUP

- [ ] Git geïnstalleerd
- [ ] User.name geconfigureerd
- [ ] User.email geconfigureerd
- [ ] GitHub account aangemaakt
- [ ] Repository aangemaakt op GitHub
- [ ] Lokale folder aangemaakt
- [ ] git init uitgevoerd
- [ ] Files toegevoegd
- [ ] Eerste commit gemaakt
- [ ] Remote toegevoegd
- [ ] Branch naar main hernoemd
- [ ] Push succesvol
- [ ] GitHub.com toont files

---

## SNELLE REFERENTIE TABEL

| Taak | Command |
|------|---------|
| Repository aanmaken | `git init` |
| Status controleren | `git status` |
| Files toevoegen | `git add .` |
| Commit | `git commit -m "message"` |
| History zien | `git log --oneline` |
| Remote toevoegen | `git remote add origin URL` |
| Push | `git push` |
| Pull (anderen's werk) | `git pull` |
| Branch zien | `git branch` |
| Terug naar vorige commit | `git reset --hard HEAD~1` |

---

**Nu ben je klaar om Git en GitHub te gebruiken!**
