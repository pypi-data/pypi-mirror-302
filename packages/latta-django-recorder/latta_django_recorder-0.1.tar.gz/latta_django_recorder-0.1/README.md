# Latta Django Recorder

This is a python package used to record exception throw inside [Django](https://www.djangoproject.com/) projects, it also supports [Django REST framework](https://www.django-rest-framework.org/)

## Usage

Install latta-django package

```py
pip install latta-django-recorder
```

Registration is fairly straightforward, all you have to do is install the app in `settings.py`

```py

INSTALLED_APPS = [
    # ...
    'latta.latta.apps.LattaConfig',
    # ...
]

```

Then register the Latta middleware

```py
MIDDLEWARE = [
    # ...
    'latta.latta.middleware.LattaMiddleware',
    # ...
]
```

And a a last step provide a Latta api key

```py
LATTA_API_KEY = "..."
```

On application startup it is going to create a new instance and reuse it through the life time of the application. 

Currently it only creates new snapshots when an exception happens. It is going to be fairly easy to extend it to record every request/response, or even just depending on response status code.