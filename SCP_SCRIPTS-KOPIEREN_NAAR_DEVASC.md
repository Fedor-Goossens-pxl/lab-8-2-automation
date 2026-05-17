# SCP GIDS: FILES KOPIËREN NAAR DEVASC MACHINE

Fedor Goossens - 2SNEb

---

## WAT IS SCP?

SCP = Secure Copy Protocol

- Veilige file transfer via SSH
- Gebruikersnaam + wachtwoord
- Geen extra software nodig (zit in OpenSSH)
- Windows PowerShell ondersteunt het

---

## VOORBEREIDING

### Stap 1: Check SSH bereikbaarheid

In PowerShell:

```powershell
ping 192.168.19.140
# Output: Bytes=32 time=5ms
```

### Stap 2: Test SSH login

```powershell
ssh devasc@192.168.19.140
# Prompt password: (voer wachtwoord in)
# Output: Welcome to Ubuntu...
```

Type `exit` om uit te loggen.

---

## SCP SYNTAX

Basis syntax:

```
scp [options] source destination
```

Lokaal naar remote:

```powershell
scp C:\path\to\file.txt devasc@192.168.19.140:~/destination/
```

Remote naar lokaal:

```powershell
scp devasc@192.168.19.140:~/file.txt C:\local\path\
```

---

## PRAKTISCHE VOORBEELDEN

### Voorbeeld 1: Task 36 files kopiëren naar DEVASC (WERKEND VOORBEELD)

Dit is een echt werkend voorbeeld van Fedor Goossens die Task 36 files naar DEVASC kopieert:

```powershell
PS C:\Users\fedor\Downloads\task36> scp task36_netconf.py devasc@192.168.19.140:~/netconf-automation/
devasc@192.168.19.140's password:
task36_netconf.py                           100%   10KB   2.5MB/s   00:00

PS C:\Users\fedor\Downloads\task36> scp config-iosxe.xml devasc@192.168.19.140:~/netconf-automation/
devasc@192.168.19.140's password:
config-iosxe.xml                            100% 2161   527.6KB/s   00:00

PS C:\Users\fedor\Downloads\task36> scp README.md devasc@192.168.19.140:~/netconf-automation/
devasc@192.168.19.140's password:
README.md                                   100% 4082   797.3KB/s   00:00

PS C:\Users\fedor\Downloads\task36>
```

Dit voorbeeld toont:
- Alle 3 Task 36 files succesvol gekopieerd
- Transfer snelheid: 2.5MB/s tot 797KB/s (normaal)
- 100% = compleet
- Geen errors = alles OK

---

### Voorbeeld 2: Multiple files in één keer

```powershell
scp C:\Users\fedor\task36_netconf.py C:\Users\fedor\config-iosxe.xml C:\Users\fedor\README.md devasc@192.168.19.140:~/netconf-automation/
```

---

### Voorbeeld 3: Hele folder kopiëren

```powershell
scp -r C:\Users\fedor\lab-8-2-automation devasc@192.168.19.140:~/
```

Toelichting:
- `-r` = recursive (folder + inhoud)

---

### Voorbeeld 4: File van DEVASC naar Windows

```powershell
scp devasc@192.168.19.140:~/netconf-automation/output.log C:\Users\fedor\Downloads\
```

---

## TASK 36 WORKFLOW - FILES NAAR DEVASC

Stap-voor-stap om Task 36 files naar DEVASC te kopiëren:

### Stap 1: Maak folder op DEVASC

```powershell
ssh devasc@192.168.19.140
mkdir ~/netconf-automation
exit
```

### Stap 2: Kopieer Task 36 files

Zorg dat je in de folder met files bent:

```powershell
cd C:\Users\fedor\lab-8-2-automation\task36-netconf

# Kopieer alle 3 files
scp task36_netconf.py devasc@192.168.19.140:~/netconf-automation/
scp config-iosxe.xml devasc@192.168.19.140:~/netconf-automation/
scp README.md devasc@192.168.19.140:~/netconf-automation/
```

### Stap 3: Verificatie

```powershell
ssh devasc@192.168.19.140
ls ~/netconf-automation/
# Output:
# config-iosxe.xml
# README.md
# task36_netconf.py
exit
```

---

## SNELLE TIPS

### Tip 1: Poort aangeven (als niet poort 22)

```powershell
scp -P 2222 file.txt user@host:/path/
# -P (hoofdletter!) voor poort
```

### Tip 2: Verbositeit (debugging)

```powershell
scp -v file.txt user@host:/path/
# -v toont detail output
```

### Tip 3: SSH key gebruiken (optioneel)

```powershell
scp -i C:\path\to\private_key.pem file.txt user@host:/path/
```

### Tip 4: File permissions behouden

```powershell
scp -p file.txt user@host:/path/
# -p = preserve file properties
```

---

## VOLLEDIGE TASK 36 KOPIEER PROCEDURE

```powershell
# 1. Ga naar project folder
cd C:\Users\fedor\lab-8-2-automation\task36-netconf

# 2. Check files
ls
# Output:
# task36_netconf.py
# config-iosxe.xml
# README.md

# 3. SSH naar DEVASC en maak folder
ssh devasc@192.168.19.140
mkdir -p ~/netconf-automation
exit

# 4. Kopieer files één voor één
scp task36_netconf.py devasc@192.168.19.140:~/netconf-automation/
scp config-iosxe.xml devasc@192.168.19.140:~/netconf-automation/
scp README.md devasc@192.168.19.140:~/netconf-automation/

# 5. Verificatie
ssh devasc@192.168.19.140
cd ~/netconf-automation
ls -la
# Output:
# total 32
# drwxr-xr-x  2 devasc devasc  4096 May 17 17:30 .
# -rw-r--r--  1 devasc devasc 10240 May 17 17:30 task36_netconf.py
# -rw-r--r--  1 devasc devasc  2048 May 17 17:30 config-iosxe.xml
# -rw-r--r--  1 devasc devasc  5120 May 17 17:30 README.md

# 6. Check Python syntax op DEVASC
python3 -m py_compile netconf-automation/task36_netconf.py
# Geen output = OK

exit
```

---

## VEELGEBRUIKTE COMMANDO'S

### Kopieer file naar home folder

```powershell
scp myfile.txt devasc@192.168.19.140:~/
```

### Kopieer file naar specifieke folder

```powershell
scp myfile.txt devasc@192.168.19.140:~/netconf-automation/
```

### Kopieer folder recursief

```powershell
scp -r myfolder devasc@192.168.19.140:~/
```

### Kopieer met wildcard

```powershell
scp *.py devasc@192.168.19.140:~/netconf-automation/
# Alle .py files
```

### Kopieer terug van DEVASC naar Windows

```powershell
scp devasc@192.168.19.140:~/netconf-automation/* C:\Users\fedor\Downloads\
```

---

## TROUBLESHOOTING

### Probleem: "Permission denied"

```
Error: Permission denied (publickey,password)
```

Oorzaken:
- Fout wachtwoord
- User bestaat niet
- SSH service staat niet aan

Oplossing:
- Check wachtwoord
- Check username (devasc)
- Herstart SSH service

---

### Probleem: "Connection refused"

```
Error: ssh: connect to host 192.168.19.140 port 22: Connection refused
```

Oorzaken:
- DEVASC staat uit
- Netwerk niet bereikbaar
- SSH service niet actief

Oplossing:
- Ping: `ping 192.168.19.140`
- Check netwerk kabel
- Zorg DEVASC online is

---

### Probleem: "No such file or directory"

```
scp: task36_netconf.py: No such file or directory
```

Oorzaken:
- File bestaat niet
- Verkeerd pad

Oplossing:
- Check of file bestaat: `ls task36_netconf.py`
- Check volledige pad: `pwd`

---

### Probleem: "File already exists"

```
Overwrite file? (y/n)
```

Oplossing:
- Type `y` voor overschrijven
- Type `n` voor skip
- Of verwijder oud bestand eerst op DEVASC

---

## DEVASC INLOGGEGEVENS

```
Host: 192.168.19.140
Username: devasc
Password: (vraag je docent)
SSH Port: 22 (standaard)
```

---

## HANDIGE ALIASES (optioneel)

Voeg toe in PowerShell profile:

```powershell
# $PROFILE aanpassen:
notepad $PROFILE

# Voeg toe:
function scp-netconf {
    scp -r C:\Users\fedor\lab-8-2-automation\task36-netconf devasc@192.168.19.140:~/
}

function scp-task38 {
    scp -r C:\Users\fedor\lab-8-2-automation\task38-restconf devasc@192.168.19.140:~/
}

# Gebruik:
# scp-netconf (kopieert Task 36)
# scp-task38 (kopieert Task 38)
```

---

## CHECKLIST VOOR TASK 36 NAAR DEVASC

- [ ] DEVASC bereikbaar (ping 192.168.19.140)
- [ ] SSH inloggen werkt (ssh devasc@...)
- [ ] Folder op DEVASC aangemaakt (mkdir ~/netconf-automation)
- [ ] task36_netconf.py gekopieerd
- [ ] config-iosxe.xml gekopieerd
- [ ] README.md gekopieerd
- [ ] Verificatie: ls ~/netconf-automation/
- [ ] Python syntax OK: python3 -m py_compile

---

**Nu kan je gemakkelijk files naar DEVASC kopiëren!**
