# Software Documentation

---

## /config.json

A json file that holds the configuration information for the python program.

---
---

## /main.py

The main python script that your start to set up and run the program.

### celeryInitApp

A function to create a celery app.

### createFlaskApp

A function to create a flask app.

### addBlueprints

A function to add blueprints to a flask app.

### index

A function that handles the endpoint "/".

Shows the websites index or landing page.

---
---

## /make_celery.py

A python script that is run to create celery workers and beats.

### setup_periodic

A function used to add periodic tasks (beats) to celery.

---
---

## /stored_credentials.py

A python script that only serves the purpose of storing the app configuration variable for other python modules to call.

---
---

## /classes/credentials.py

A python script that holds the class that contains configuration information

### Config

A class that holds the configuration information.

---
---

## /functions/load_credentials.py

A python script that holds the function to load the credentials held in the configuration file.

### loadCredentials

A function that loads the configuration information from /config.json

---
---

## /templates/base.j2

A jinja file that holds the base file that other jinja templates extend.

---
---

## /templates/home.j2

A jinja file that renders the websites index or landing page.

---
---

## /static/css/base.css

The css file that is used as the default style sheet for the jinja templates.

---
---

## /static/js/cookies.js

A javascript file to get the cookies from a webpage.

### getCookies

A function to return a map of the cookies on the webpage.

---
---

## /auth/auth.py

The main python script for the auth module. It holds the flask blueprint.

### showUser

A function that handles the endpoint "/auth/user/\<string:username>".

Shows a user their account page.

### showLogin

A function that handles the endpoint "/auth/login".

Shows the login page.

### loginAttempt

A function that handles the endpoint "/auth/login-attempt".

Handles an login attempt and either returns the login page again or the users account page.

### showLogout

A function that handles the endpoint "/auth/logout".

Handles a logout request by a user.

### newUser

A function that handles the endpoint "/auth/new-user".

Shows the page to create a new user.

### createAttempt

A function that handles the endpoint "/auth/create-attempt".

Handles the request to create a new account.

---
---

## /auth/classes/auth_classes.py

A python script to hold the classes used in the auth module.

### UserObj

A class that holds user information.

### UserAuth

A class that is used to store user authorization information.

---
---

## /auth/functions/auth_functions.py

A python script to hold the functions used in the auth module.

### generateAuth

A function that generates the auth information for a user logging in.

### checkAuth

A function that checks if the auth information being checked is currently valid.

### checkUser

A function that checks if a user exists.

### getUser

A function that gets user information.

### removeSession

A function that removes the current session being passed in.

### removeAllUserSessions

A function that removes all of the sessions for the user being passed in.

### checkHashPass

A function that checks if a password and salt gives the correct hashed password.

### checkLogin

A function that checks if a login for a user is valid.

### createSalt

A function that creates a new salt, used when a user is created or changes their password.

### createHashPass

A function that creates a hashed password from a password and a hash.

### createUser

A function that creates a new user.

### getUserAuthCookies

A function that gets the cookies about the user.

Returns the following:

- str: username
- str: auth

### getUserAuthCookiesStatus

A function that gets the cookies and checks the authorization status of the user.

Returns the following:

- str: username
- bool: authorization status

### getUserAuthStatus

A function that checks the authorization status of the user.

Returns the following:

- bool: authorization status

### getUserAuthCookiesStatusFull

A function that gets the user cookies and checks the authorization status of the user.

Returns the following:

- str: username
- str: auth
- bool: authorization status

### getUserAuthProper

A function that checks the authorization status of the user and that they are attempting to access information about themselves.

Returns the following:

- bool: proper authorization status

### getUserAuthProperBoth

A function that checks the authorization status of the user and that they are attempting to access information about themselves.

Returns the following:

- bool: authorization status
- bool: proper authorization status

### getUserAuthProperBothName

A function that gets the user's cookies and checks the authorization status of the user and that they are attempting to access information about themselves.

Returns the following:

- str: username
- bool: authorization status
- bool: proper authorization status

### removeExpiredSessions

A function that removes all expired sessions. It is ran every hour by celery.

---
---

## /auth/templates/login.j2

A jinja file that renders the login page.

---
---

## /auth/templates/logout.j2

A jinja file that renders a user's logout page.

---
---

## /auth/templates/new_user.j2

A jinja file that renders the webpage to create a new user.

---
---

## /auth/templates/user.j2

A jinja file that renders a user's profile page.

---
---

## /tracker/tracker.py

The main python script for the tracker module. It holds the flask blueprint.

### showTracker

A function that handles the endpoint "/tracker/user/\<string:username>".

Shows a user their tracking interface.

### showTrackedActivities

A function that handles the endpoint "/tracker/user/\<string:username>/activities".

Shows a user their activities interface.

---
---

## /tracker/classes/tracker_classes.py

A python script to hold the classes used in the tracker module.

---
---

## /tracker/functions/tracker_functions.py

A python script to hold the functions used in the tracker module.

---
---

## /tracker/templates/tracked.j2

A jinja file that renders a users tracking interface.

---
---

## /tracker/templates/tracker.j2

A jinja file that renders a users activities interface.

---
---

---
---

## /tracker/static/js/password.js

A javascript file to check that the 2 password fields are the same.

### validatePassword()

Validates that the two passwords are the same.
