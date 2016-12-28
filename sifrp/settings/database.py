from restricted import DATABASE_PASSWORDS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'sifrp',
        'PORT': '5433',
        'PASSWORD': DATABASE_PASSWORDS['default'],
    }
}
