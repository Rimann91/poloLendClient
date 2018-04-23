"""
This is the view model for the app
It acts as the middle man between the data model
and the User Interface
"""

from dataModel import PoloniexWrap
from poloniex import Poloniex
import dataModel
import decimal
import asyncio

class DataDisplay():
    """retrieve data from data model and
    configure for display"""

    def __init__(self, key=False, secret=False):

        self.pw = PoloniexWrap(key, secret)
        self.al = dataModel.myAsyncLoans()
        self.poloSend = Poloniex(key, secret)
        self.key = self.pw.key
        self.secret = self.pw.secret
        self.activeOffers = {}

################## START ASYNC ATTEMPT ###########################
    async def loanOffers(self):
        """retrieve loan order
        Configure loan order data for display"""

        loanData = await self.al.returnLoanOrders('BTC')
        offers = ''
        whiteSpaceAmount = 25
        whiteSpaceRate = 20

        for i in loanData['offers']:
            ratePercent = '%.5f' % float(i['rate'])
            rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
            amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
            rMin = i['rangeMin']
            rMax = i['rangeMax']
            offers += "{}{}{}-{}{}".format(rate, amount, rMin, rMax, '\n')

        return offers

    async def loanDemands(self):
        """retrieve loan demands
        Configure demands  data for display"""

        loanData = self.pw.getLoanOrders()
        demands = ''
        whiteSpaceAmount = 25
        whiteSpaceRate = 20

        for i in loanData['demands']:
            ratePercent = '%.5f' % float(i['rate'])
            rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
            amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
            rMin = i['rangeMin']
            rMax = i['rangeMax']
            demands += "{}{}{}-{}{}".format(rate, amount, rMin, rMax, '\n')

        return demands


################# END ASYNC ATTEMPT ###############################

#    def loanOffers(self):
#        """retrieve loan order
#        Configure loan order data for display"""
#
#        loanData = self.pw.getLoanOrders()
#        offers = ''
#        whiteSpaceAmount = 25
#        whiteSpaceRate = 20
#
#        for i in loanData['offers']:
#            ratePercent = '%.5f' % float(i['rate'])
#            rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
#            amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
#            rMin = i['rangeMin']
#            rMax = i['rangeMax']
#            offers += "{}{}{}-{}{}".format(rate, amount, rMin, rMax, '\n')
#
#        return offers
#
#    def loanDemands(self):
#        """retrieve loan demands
#        Configure demands  data for display"""
#
#        loanData = self.pw.getLoanOrders()
#        demands = ''
#        whiteSpaceAmount = 25
#        whiteSpaceRate = 20
#
#        for i in loanData['demands']:
#            ratePercent = '%.5f' % float(i['rate'])
#            rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
#            amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
#            rMin = i['rangeMin']
#            rMax = i['rangeMax']
#            demands += "{}{}{}-{}{}".format(rate, amount, rMin, rMax, '\n')
#
#        return demands
#
    def activeoffers(self):
        """retrieve my open loan orders"""

        ordersData = self.pw.getActiveLoanOffers()
        orders = []
        whiteSpaceAmount = 20
        whiteSpaceRate = 15
        whiteSpaceDuration = 13
        whiteSpaceAutoRenew = 12
        whiteSpaceCoin = 13

        for k,v in ordersData.items():

            for i in ordersData[k]:
                coin = k+' '*self.formatWs(k, whiteSpaceCoin)
                ratePercent = '%.5f' % float(i['rate'])
                rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
                amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
                duration = str(i['duration'])+' '*self.formatWs(i['duration'],whiteSpaceDuration)
                date = i['date']
                if i['autoRenew'] == 1:
                    autoRenew = 'on'+' '*self.formatWs('on', whiteSpaceAutoRenew)
                elif i['autoRenew'] == 0:
                    autoRenew = 'off'+' '*self.formatWs('off', whiteSpaceAutoRenew)
                else: autoRenew = 'NULL'+' '*self.formatWs('NULL', whiteSpaceAutoRenew)
                orders.append({'display':'{}{}{}{}{}{}'.format(coin, rate, amount, duration, autoRenew, date),'id': i['id']})

        return orders

    def activeLoans(self):
        """format active loans for display"""

        loansData = self.pw.getActiveLoans()
        loans = []
        whiteSpaceAmount = 15
        whiteSpaceRate = 10
        whiteSpaceDuration = 10
        whiteSpaceAutoRenew = 10
        whiteSpaceCoin = 10
        whiteSpaceDate = 25

        for i in loansData['provided']:

            coin = i['currency']+' '*self.formatWs(i['currency'], whiteSpaceCoin)
            ratePercent = '%.5f' % float(i['rate'])
            rate = str(ratePercent)+' '*self.formatWs(ratePercent, whiteSpaceRate)
            amount = i['amount']+' '*self.formatWs(i['amount'], whiteSpaceAmount)
            duration = str(i['duration'])+' '*self.formatWs(i['duration'], whiteSpaceDuration)
            date = i['date']+' '*self.formatWs(i['date'], whiteSpaceDate)
            fee = i['fees']
            identify = i['id']

            if i['autoRenew'] == 1:
                autoRenew = 'on'+' '*self.formatWs('on', whiteSpaceAutoRenew)

            elif i['autoRenew'] == 0:
                autoRenew = 'off'+' '*self.formatWs('off', whiteSpaceAutoRenew)

            else: 
                autoRenew = 'NULL'+' '*self.formatWs('NULL', whiteSpaceAutoRenew)

            loans.append({'display':'{}{}{}{}{}{}{}'.format(coin, rate, amount, duration, autoRenew, date, fee),
                        'id': identify})

        return loans


    def totalFees(self):
        """"""

        decimal.getcontext().prec = 8
        loansData = self.pw.getActiveLoans()
        fees = []
        totalFees = 0.0

        for i in loansData['provided']:
            fees.append(decimal.Decimal(i['fees']))
        totalFees = sum(fees)

        return totalFees

    def averageRate(self):
        """"""
        
        decimal.getcontext().prec = 8
        loansData = self.pw.getActiveLoans()
        rates = []
        for i in loansData['provided']:
            rates.append(decimal.Decimal(i['rate']))
            if  len(rates) != 0:
                average = sum(rates) / len(rates)
            else: average = 0

        return average

    def totalActiveAmount(self):
        """ calculates the total sum of the active loans """

        decimal.getcontext().prec = 8
        loansData = self.pw.getActiveLoans()

        if len(loansData['provided']) != 0:

            amounts = []

            for i in loansData['provided']:

                if i['currency'] == 'BTC':
                    amounts.append(decimal.Decimal(i['amount']))

            amount = float(sum(amounts))

            return amount

        else:
            return 0

    def activeTotals(self):
        amount = str(self.totalActiveAmount())
        amount += ' '*self.formatWs(amount, 25)
        rate = '%.5f' % self.averageRate()
        rate = str(rate)+' '*self.formatWs(rate, 25)
        fee = str(self.totalFees())
        #fee += ' '*self.formatWs(fee, 15)
        totals = "{}{}{}".format(rate, amount, fee)
        return totals

    def formatWs(self, displayItem, spaces):
        """format white space between display info"""

        displayItem = str(displayItem)
        return spaces-len(displayItem)

    ################# SEND DATA TO POLONIEX ############################
    def createOffer(self, currency, rate, amount, duration=2, autoRenew=0):
        self.poloSend.createLoanOffer(currency, amount, rate, autoRenew, duration)

    def cancelOffer(self, id):
        self.poloSend.cancelLoanOffer(id)



