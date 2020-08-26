# Treebuster
Treebuster - recursive Gobuster

This is pretty much a fancy wrapper for Gobuster or any other *buster program which is compatible to Gobuster. 
It scans a target and if it finds a directory listing it will read it out or start a new Gobuster process on the found directory. 



# Dependencies
anytree - only for neat output
https://pypi.org/project/anytree/

Gobuster - duh!
https://github.com/OJ/gobuster


# How to use:
You have to change [launcher.py](https://github.com/pyrat3/Treebuster/blob/master/launcher.py "launcher.py") to specify your word list and your Gobuster location/command from which Gobuster is started.
` python tools/treebuster/start.py <target>` - DONT FORGET the `http://`

**THIS IS FAR FROM COMPLETE AND MAY OR MAY NOT WORK FOR YOU!**
Feedback very welcome. 



