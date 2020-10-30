# Testr - An Automation Controller Interface

Testr is a web based interface to configure and run Commvault automation tests and install updates.

![Testr Main Form Screenshot](/Screenshots/testr.png)

## Technology
* Python 3

## Development

Create virtual env
Activate Virtual Environment
Run pip install
Copy config.yaml.example to config.yaml

```
python -m venv venv
pip install -r requirements.txt
cp config.yaml.example config.yaml
```

Edit config.yaml in your preferred text editor

## Database Migrations
We use SQLAlchemy to perform migrations on the database, to get it up and running execute the following commands:

```
flask db init
flask db migrate
flask db upgrade
```
