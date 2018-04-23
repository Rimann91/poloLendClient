"""
This is the Data Model for the app
"""
from poloniex import Poloniex
import async_timeout
import aiohttp


class PoloniexWrap():
    """ Syncronously Retrieves Poloniex Data """

    def __init__(self, key, secret):
        """ Initialize data model and authenticate"""
        self.key = key
        self.secret = secret
        self.polo = Poloniex(self.key, self.secret, 120)

    def getTick(self, pair):
        """get ticker"""

        ticker = self.polo.returnTicker()[pair]
        return ticker

    def getOrderBooks(self, pair):
        """ get orders"""

        return self.polo.returnOrderBook(pair, '10')

    def getLoanOrders(self):
        """get Loan orders"""
        #orders = self.polo.returnLoanOrders('BTC')
        order = self.polo.returnLoanOrders('BTC')
        return order

    def getActiveLoanOffers(self):
        """get my active loan offers"""

        return self.polo.returnOpenLoanOffers()

    def getActiveLoans(self):
        """get my active loans"""

        return self.polo.returnActiveLoans()

class myAsyncLoans():
    """My api calls to retrieve asyncronous loan data form Poloniex"""
    def __init__(self, key=False , secret=False):
        self.key = key
        self.secret = secret
        self.publicUrl = 'https://poloniex.com/public'

    async def fetch(self, session, url, params):
        """ Retrieves The Data from Poloniex API"""
        async with async_timeout.timeout(60):
            async with session.get(url, params=params) as response:
                dictJson = await response.json()
                url = response.url
                status = response.status
            return dictJson

    async def returnLoanOrders(self, currency):
        params = {'command': 'returnLoanOrders', 'currency': currency}
        async with aiohttp.ClientSession() as session:
            strJson = await self.fetch(session, self.publicUrl,
                    params)
        return strJson
