# Garrett's Split Tracker

 A program used to track and display "splits" for activities.

# Run Template

## Windows

- Initial Run
  - cd /your/folder
  - python3 -m venv env
  - call env/Scripts/activate.bat
  - python3 template.py
- Running After
  - cd /your/folder
  - call env/Scripts/activate.bat && python3 template.py

### Linux

- Initial Run
  - cd /your/folder
  - python3 -m venv env
  - source env/bin/activate
  - python3 template.py
- Running After
  - cd /your/folder
  - source env/bin/activate && python3 template.py
  - You may have to set executable if it doesn't run

### Flask

- cd src
- flask --app main run
  - flask --app main run --debug
