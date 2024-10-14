# TO DO

- Add a single CLI argument to change the path of the config file, but that's it!
- Make sure the config file checks for the right data types (bools and ints not strings for example)
- Maybe change the chmod on some of those directories to not let others read it, there really wasn't a reason for that.
  - Yeah I don't think any of those directories need to be open to others. Even some of the groups could be modified.
- Create a shell script (or some other method) to automate most of the set up when the project is completed.
  - Possibly docker, but I'm not sure if I want to use docker for this project.
- Set up regular back ups for PostgreSQL and MongoDB.
  - Crontab most likely, but I could also have it run from celery.
