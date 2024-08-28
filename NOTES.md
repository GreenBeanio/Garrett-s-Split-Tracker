# General notes to remind myself

The make_celery file is mostly useless, but contains code to test if the redis server is working. I can call the celery worker from the main file right now, but not from that file.

Wait maybe I'm tripping

celery -A make_celery worker --loglevel INFO

well that returns a bunch of errors

celery -A main worker --loglevel INFO

well that one doesn't return errors, but I don't think it works right
