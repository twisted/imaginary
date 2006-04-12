#random stuff of washort's


from Reality import thing
from twisted import web
import string

import __main__ # rely upon the twisted.net convention

#one troy ounce = 31.103477 grams

class QuoteBoard(thing.Thing):

    def __init__(self, name, r=''):
        thing.Thing.__init__(self, name, reality=r)
        self.description = "A large chalkboard, currently blank."
        self.quotes = {}

    def fetchQuote(self, currency="US"):
        self.currency = currency
        web.HTTPCallback("http://www.e-gold.com/unsecure/metaldata.asp?LATEST=1&GOLD=1&SILVER=1&CUR=%s" % currency,
                         self.parseQuote, __main__.selector)
        self.place.allHear(self, " emits a soft hum.")

    def parseQuote(self, code, headers, data):
        time, gold, silver = string.split(data, ",")
        self.quotes[self.currency] = [float(gold), float(gold) / 31.103477,float(silver), float(silver) /  31.103477]

    def updateBoard(self, data):
        self.parseQuote(data)
        self.description = """A large chalkboard, with this hastily written on it:
         $/Ounce   $/Gram
Gold     $%.3f     $%.3f
Silver   $%.3f     %.3f""" % tuple(self.quotes["US"])
        self.place.allHear(self, " emits a soft *ching*.")
        #self.later(self.fetchQuote, 4320)
