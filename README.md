# live-journal

    git clone https://github.com/MichaelPavlov/live-journal
    cd live-journal
    virtualenv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python manage.py migrate
    .venv/bin/python manage.py loadfixture fixture.json
