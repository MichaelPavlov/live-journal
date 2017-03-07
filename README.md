# live-journal

    git clone https://github.com/MichaelPavlov/live-journal
    cd live-journal
    virtualenv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python manage.py migrate
    .venv/bin/python manage.py loadfixture fixture.json


Для отправки сообзений по почте, необходимо выставить следующие настройки в live_magazine/settings.py:

    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    