# Mosbymods.de_installer
##The official Mosbymods.de installer made to install ets2 dlcs free

pyinstaller code:
```sh
pyinstaller app.py --onefile --noconsole --icon=icon.ico --uac-admin --add-data "browseicon.png;." --add-data "dlcs;dlcs" --add-data "icon.ico;."
```
