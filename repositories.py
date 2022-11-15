import datetime as dt
import psycopg2

class CurrencyRepository:

    def __init__(self, dbname:str, user:str, password:str) -> None:
        self.conn = psycopg2.connect(f'dbname="{dbname}" user="{user}" password="{password}"')
        

    def insert_currency(self, data) -> None:
        """Veritabanına currency verilerini kaydeder. Eğer kaydedilmişse günceller.
        """
        pass


    def read_last_date(self) -> dt.date:
        """Veritabanındaki son kayıt tarihini döndürür.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(date) FROM currency")
        cur.fetchall()
        cur.close()
    

    def close(self):
        """Veritabanı bağlantısını kapatır.
        """
        self.conn.close()
