from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('TOKEN')
admin_id = getenv('ADMIN_ID')
host = getenv('PGHOST')
PG_USER = getenv('PG_USER')
PG_PASS = getenv('PG_PASS')
