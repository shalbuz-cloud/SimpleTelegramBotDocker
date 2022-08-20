from os import getenv

# Теперь за нас переменные окружения подгрузит докер

TOKEN = getenv('TOKEN')
admin_id = getenv('ADMIN_ID')
host = getenv('PGHOST')
PG_USER = getenv('PG_USER')
PG_PASS = getenv('PG_PASS')
