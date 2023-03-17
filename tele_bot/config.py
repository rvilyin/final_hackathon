

from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'stream',
    user = 'blackhat',
    password = '1',
    host = 'localhost',
    port = 5432
)

TOKEN = '6031835250:AAFoytaeMDsaVukPbmrOs_sRho-I7R9oFzk'

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:52607'

PAYMENT_IMAGE_URL = 'https://images.prom.ua/3757111310_kartiny-po-nomeram.jpg'
