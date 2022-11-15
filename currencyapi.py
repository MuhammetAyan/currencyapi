import requests
import datetime as dt


ERROR_MAPS = {
    400: "You did not supply an API key",
    401: "Your API key is not valid",
    402: "Your requesting an API function that does not exist. Please check the docs",
    403: "You requested a pair that does not exist",
    405: "You have hit your monthly subscription allowance.",
    406: "You've requested a base currency that doesn't exist",
    407: "Your subscription plan does not allow you to use secure HTTPS encryption.",
    408: "Your subscription plan does not allow you to select a base currency.",
    410: "The 'from' parameter was not set.",
    411: "The 'to' parameter was not set.",
    412: "The 'amount' parameter was not set",
    413: "The value you entered for the amount parameter is incorrect. Please make sure it is numeric and greater than 0.",
    414: "One or more of the currencies is not a currency we support or has been entered invalid.",
    415: "One or more of the currencies you wanted to receive (limit) is not a currency we support or has been entered invalid.",
    416: "Your subscription plan does not allow you to use the %s endpoint",
    417: "There is no historical data for %s for the date supplied.",
    418: "One or more of the dates you supplied were not in the correct format (eg 2017-12-25).",
    419: "We allow a maximum of 365 days. Please change this and try again.",
    420: "You have requested either today's date or a date in the future. For timeframe and history endpoints, we store the data at 23:59 GTM of the current day.",
    500: "There seems to be a technical fault our end"
}

class CurrencyApi:

    def __init__(self, key):
        self.key = key
    
    def currencies(self):
        """Para birimlerinin isimleri
        """
        url = f"https://currencyapi.net/api/v1/currencies?key={self.key}&output=JSON"
        response = requests.request("GET", url)
        return response.json()
    
    def rates(self, base: str='USD'):
        """Para birimlerinin belirtilen para birimi karşısındaki değeri. Belirtilen birim varsayılan USD'dir.
        """
        url = f"https://currencyapi.net/api/v1/rates?key={self.key}&base={base}&output=JSON"
        response = requests.request("GET", url)
        if response.status_code in ERROR_MAPS.keys(): raise Exception("Error:" + ERROR_MAPS[response.status_code])
        if not response.json()['valid']: raise Exception("Veriye doğru bir şekilde erişilemedi!")
        return response.json()['rates']
    
    
    def history(self, date: dt.date, base:str='USD'): 
        """ Para birilerinin belirtilen tarihteki belirtilen para birimi karşısındaki değeri. Belirtilen birim varsayılan USD'dir. Premium 
        """
        url = f"https://currencyapi.net/api/v1/history?key={self.key}&base={base}&date={date.isoformat()}&output=JSON"
        response = requests.request("GET", url)
        if response.status_code in ERROR_MAPS.keys(): raise Exception("Error:" + ERROR_MAPS[response.status_code])
        if not response.json()['valid']: raise Exception("Veriye doğru bir şekilde erişilemedi!")
        return response.json()['rates']
