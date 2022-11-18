import datetime as dt
import psycopg2
from typing import Dict

class CurrencyRepository:

    def __init__(self, dbname:str, user:str, password:str, host:str, port:str='5432') -> None:
        self.conn = psycopg2.connect(database = dbname, host=host, user=user, password=password, port=port)
        

    def insert_currency(self, date:dt.date, data:Dict[str, float]) -> None:
        """Veritabanına currency verilerini kaydeder.
        """
        cur = self.conn.cursor()
        for currency_code in data:
            print(date.isoformat(), currency_code, data[currency_code])
            p = {"date": date.isoformat(), "currency_code": currency_code, "rate": data[currency_code]}
            cur.execute("""UPDATE currency SET rate = %(rate)s WHERE date = %(date)s and currency_code = %(currency_code)s;
            INSERT INTO currency (date, currency_code, rate)
            SELECT %(date)s, %(currency_code)s, %(rate)s
            WHERE NOT EXISTS (SELECT 1 FROM currency WHERE date = %(date)s and currency_code = %(currency_code)s);
            """, p)
            # cur.execute("""INSERT INTO currency (date, currency_code, rate) VALUES (%s, %s, %s);""", ())
        self.conn.commit()
        cur.close()
    
    # def update_currency(self, date:dt.date, data:Dict[str, float]) -> None:
    #     """Veritabanındaki currency verilerini güncelle.
    #     """
    #     cur = self.conn.cursor()
    #     for currency_code in data:
    #         print(date.isoformat(), currency_code, data[currency_code])
    #         cur.execute("""UPDATE currency SET rate = %s WHERE date = %s and currency_code = %s """, (date.isoformat(), currency_code, data[currency_code]))
    #     self.conn.commit()
    #     cur.close()


    def read_last_date(self) -> dt.date:
        """Veritabanındaki son kayıt tarihini döndürür.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(date) FROM currency")
        data = cur.fetchone()
        cur.close()
        if data[0] is None: return None
        if type(data[0]) == dt.datetime: return data[0].date()
        return data[0]
    

    def close(self):
        """Veritabanı bağlantısını kapatır.
        """
        self.conn.close()
