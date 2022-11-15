import currencyapi
import settings
import repositories as repos
import datetime as dt


curr_repo = repos.CurrencyRepository(
    dbname=settings.DATABASE_CONNECTION_DATABASE_NAME,
    password=settings.DATABASE_CONNECTION_PASSWORD,
)
last_regis_date = curr_repo.read_last_date()

if last_regis_date == dt.date.today() - dt.timedelta(days=1): # Eğer son kaydedilen veri düne aitse
    cur = currencyapi.CurrencyApi(key=settings.CURRENCYAPI_KEY)
    curr_repo.insert_currency(cur.rates())

# -----------------------------------------------------------------------------------------------------------
# Bu bölüm ücretli web servise ait kodlar olduğundan test edilemedi.
elif last_regis_date < dt.date.today() - dt.timedelta(days=1): # Eğer son kaydedilen veri dünden de eskiyse
    cur = currencyapi.CurrencyApi(key=settings.CURRENCYAPI_KEY)
    temp_date = last_regis_date + dt.timedelta(days=1) # Son kaydedilen veriden bir gün sonrasının tarihi
    # Kaydedilmeyen her gün için geçmiş veriyi veritabanına kaydet.
    while temp_date < dt.date.today(): 
        curr_repo.insert_currency(cur.history(temp_date))
        temp_date += dt.timedelta(days=1)
    curr_repo.insert_currency(cur.rates()) # Son olarak bugünün verisini de kaydet.
# -----------------------------------------------------------------------------------------------------------
elif last_regis_date == dt.date.today(): # Eğer son kaydedilen veri bugüne aitse
    pass # Güncelleme durumu yazılacak.
    