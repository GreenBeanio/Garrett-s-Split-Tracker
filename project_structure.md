# Structure of the project

("#" meaning in progress)

- Symbols
  - / is a directory
  - @ is a file
  - ! Means it's being worked on
  - & Ignored by git

- /Root: Everything (as well as misc files for now)
  - /restructured: trying to tidy up the flask program for later
    - &@ config.json: The configuration file for the application
    - @requirements.txt: The requirements file for pip
    - @main.py: The main file to create the flask application factory
    - @make_celery.py: The file for creating celery workers
    - @stored_credentials.py: A file holding a variable that stores the config information
    - /static: the main static directory for flask
      - /js: main directory for javascript
        - @cookies.js: A script to get the cookie information from the current webpage
      - /css: main directory for css
        - @base.css: The basic css for the project
      - /html: main directory for html
      - /images: main directory for images
    - /templates: general templates
      - @base.j2: The base template that is extended
      - @home.j2: The template for a users home page
    - /functions: General python functions
      - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
      - @load_credentials.py: script to load the credentials
    - /classes: general python classes
      - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
      - @credentials.py: class to hold the credentials
    - !/auth: the "module" for authorizing users
      - @auth.py: The file containing all the flask auth routes
      - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
      - /classes: Directory for python classes
        - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
        - @auth_classes.py: The classes used in the auth module.
      - /functions: Directory for python functions
        - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
        - @auth_functions.py: The functions used in the auth module.
      - /static: Directory for flask static files
        - /css: Directory for css
        - /js: Directory for javascript
      - /templates: Directory for jinja templates
        - @login.j2: The template for the log in page
        - @logout.j2: The template for the log out page
        - @new_user.j2: The template for creating a new user
        - @user.j2: The template for displaying user information
    - !/tracker: the "module" to handle tracking activities
      - @tracker.py: The file containing all the flask tracker routes
      - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
      - /classes: Directory for python classes
        - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
        - @tracker_classes.py: The classes used in the tracker module.
      - /functions: Directory for python functions
        - @\_\_init\_\_.py: empty init file for a python module (not namespace module)
        - @tracker_functions.py: The functions used in the tracker module.
      - /static: Directory for flask static files
        - /css: Directory for css
        - /js: Directory for javascript
          - @password.js: A javascript script for validating the confirmed password.
      - /templates: Directory for jinja templates
        - @tracker.j2: The main interface when actually tracking activities.
        - @tracked.j2: The main interface for looking at previously tracked activity components (such as the activity and its categories)
- !/docker: Stuff for docker in the future
  - @docker-compose.yaml: Will be used for docker compose in the future
  - /dockerfiles: Will be used to store dockerfiles for the various components in the future
    - @python.dockerfile: The dockerfile to set up the container for handling python
- @project_structure.md: Document trying to explain the structure
- @api_structure.md: Document trying to explain the api structure
- @setup_notes.md: notes on the setup process
- @README.md: Main introduction to the project
- @LICENSE: The license of this project
- @NOTES.md: Random notes to remind myself
- @Information.md: Information about the technology used in this project
- @template.py: A template python file with the header comments
