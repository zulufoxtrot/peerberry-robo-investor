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

To run in a shell:

`poetry shell`
then
`python main.py`


To run automatically:

Set up a cron job for this command:

`poetry run bash -c "PEERBERRY_EMAIL=your_email PEERBERRY_PASSWORD=your_password python /path/to/project/main.py"`

