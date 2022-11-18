import currencyapi
import repositories as repos
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()


curr_repo = repos.CurrencyRepository(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)


last_regis_date = curr_repo.read_last_date()

if last_regis_date is None: # Eğer henüz veri kaydedilmediyse
    cur = currencyapi.CurrencyApi(key=os.getenv('CURRENCYAPI_KEY'))
    curr_repo.insert_currency(dt.date.today(), cur.rates())

elif last_regis_date == dt.date.today() - dt.timedelta(days=1): # Eğer son kaydedilen veri düne aitse
    cur = currencyapi.CurrencyApi(key=os.getenv('CURRENCYAPI_KEY'))
    curr_repo.insert_currency(dt.date.today(), cur.rates())

# -----------------------------------------------------------------------------------------------------------
# Bu bölüm ücretli web servise ait kodlar olduğundan test edilemedi.
elif last_regis_date < dt.date.today() - dt.timedelta(days=1): # Eğer son kaydedilen veri dünden de eskiyse
    cur = currencyapi.CurrencyApi(key=os.getenv('CURRENCYAPI_KEY'))
    temp_date = last_regis_date + dt.timedelta(days=1) # Son kaydedilen veriden bir gün sonrasının tarihi
    # Kaydedilmeyen her gün için geçmiş veriyi veritabanına kaydet.
    while temp_date < dt.date.today(): 
        curr_repo.insert_currency(temp_date, cur.history(temp_date))
        temp_date += dt.timedelta(days=1)
    curr_repo.insert_currency(dt.date.today(), cur.rates()) # Son olarak bugünün verisini de kaydet.
# -----------------------------------------------------------------------------------------------------------
elif last_regis_date == dt.date.today(): # Eğer son kaydedilen veri bugüne aitse
    cur = currencyapi.CurrencyApi(key=os.getenv('CURRENCYAPI_KEY'))
    curr_repo.insert_currency(dt.date.today(), cur.rates())
    pass # Güncelleme durumu yazılacak.
    