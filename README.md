# Peerberry Robo-investor
Invests automatically on the Peerberry crowdlending platform.

Peerberry already has a robo-investor built-in, but for some reason it does not invest fast enough, causing cash drag.

# Install

Requires python 3.9+

Install Poetry:

`curl -sSL https://install.python-poetry.org | python -`

Setup project with poetry:

`poetry install`

# Run

Set up a cron job for this command:

`PEERBERRY_EMAIL=your_email PEERBERRY_PASSWORD=your_password python /path/to/project/main.py`

