# Matching Engine
This is the matching engine we are building to match students with each other &amp; ideas!

To clone the app, run in terminal:

```bash
git clone https://github.com/ac-i2i-engineering/matching-engine.git
cd matching-engine
```

Set-up a virtual environment and activate it to "containerize" the dependencies:

```bash
python3 -m venv env
source env/bin/activate
```

To run the app locally, run:

```bash
pip install -r requirements.txt
cd matching_backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
