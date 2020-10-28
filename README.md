# Testr - An Automation Controller Interface

Testr is a web based interface to configure and run Commvault automation tests and install updates.

## Technology
* Python 3
* PowerShell

## Development

Create virtual env
Activate Virtual Environment
Run pip install

```
python -m venv venv
pip install -r requirements.txt
```

## Database Migrations
We use SQLAlchemy to perform migrations on the database, to get it up and running execute the following commands:

```
flask db init
flask db migrate
flask db upgrade
```
