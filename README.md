# Garrett's Split Tracker

 A program used to track and display "splits" for activities.

## Run Template

This application DOES NOT run on windows! (unless using Docker, which I haven't set up)

### Linux

#### Initial Run

- cd /your/folder
- python3 -m venv env
- source env/bin/activate
- pip install -r requirements.txt
- See Below

#### Flask

- cd src
- source env/bin/activate
- python main.py
<!--
- flask --app main run
  - flask --app main run --debug
-->

#### Celery

- cd src
- source env/bin/activate
- celery -A make_celery beat --loglevel INFO
- celery -A make_celery worker --loglevel INFO

## Q&A

### What is the purpose of this project?

This project is first and foremost a project for me to learn Flask, improve with Vanilla JavaScript, HTML, and CSS, and to learn to create an API.

The project itself being a "Split Tracker" serves the main purpose of being a precursor project. The goal project being my years long ongoing attempt to create an expansive Tracking System as well as Analysis. This project will help be facilitate that goal by creating a smaller scale version of the larger tracking ecosystem. Possibly even being implemented into the larger tracking system later as a microservice, or whatever architecture I choose to use.

This project is specifically intended for "split tracking" in video games. Which is recording how long it takes to do specific tasks in a video game. Such as beating a level, beating a boss, etc. However, it will also be able to record "splits" for any other type of activity. I'll give some examples besides video games. For painting you could record how long it takes to sketch, paint, varnish, etc. For music you could record how long it takes to compose, write, record, mix, master, etc. For writing you could record how long it takes to plan, write, edit, etc. For programming you could record how long it takes to plan, program, document, etc. Really any activity you want to record the different tasks that make it up.

Besides the learning experience and being a precursor to my main project I chose a video game split tracker for another reason. That reason being that some of my friends have been wanting me to stream an Elden Ring playthrough for them to watch. I think it would be cool to track the time, attempts, etc it takes for me to beat every boss and area. As well as to display it on stream and later visualize it. That is probably just my data science, nerdy, statistics, data collection side coming out though. What can I say. I like to track.

### Why using PostgreSQL, MongoDB, and Redis?

I'm using all 3 of these options because as stated above this is a learning project. I was originally going to only user MongoDB, because I don't have much experience with NoSQL. However, since I want to specifically learn PostgreSQL I decided to add it as well. Redis was originally added because I needed it to use Celery, but if I have to use it anyway I'm going to play around with it as a cache for sessions and such.

I'm well aware that PostgreSQL has native support for Json, but I still want to learn more MongoDB. For that reason I will be using PostgreSQL for traditional structured relational data, MongoDB for semi-structured and non-relational data, and Redis to store commonly used data to reduce database requests. I will try PostgreSQL Json as well because I want to learn that too.

For example:

- PostgreSQL will store data such as the accounts and activities.
- MongoDB will store data such as the individual activity entries.
- Redis will store data such as the currently connected sessions.
