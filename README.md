# year-tracker

Tool for myself to track my New Year resolutions 

Whose development turned into a hinderance for some of my new year's resolutions.

Currently consists of a database and a frontend.

Plan is to host it on a raspberry pi for checking/updating progress on a local network, with a way to update remotely by email or twitter.

UI improvements and any other contributions very welcome!

## Setup:
  1. provide `config.json` with details to a postgres database
  2. run `export FLASK_APP=server.py; flask run`
  3. invoke endpoint `/init`, e.g. `curl http://127.0.0.1:5000/init`
  4. go to default endpoint `/` and track your 2020!
  
## Points on Usage:
  * The day is colored a different intensity of green based on the amount of resolutions done that day
  * The database has an int field for each of the goals in case of more in-depth tracking (e.g. pages read, minutes exercised, etc.) but currently visualization only checks if field is more than 0


Planned Features:
  * Juicier frontend with animations
  * Refactor code for easier modification/addition of trackable goals
  * Login feature in case of hosting publicly
  * Edit past days
  * Graphs of stats!
  * More ways to update progress (email?)
  

