
import os, sys, string, random

import pyparsing

from twisted.internet import defer
from twisted.python import reflect, rebuild, util

import imaginary
from imaginary import text as T, eimaginary, iterutils

def stripper(s, loc, toks):
    toks = toks.asList()
    toks[0] = toks[0][1:-1]
    return toks

def targetString(name):
    qstr = pyparsing.quotedString.setParseAction(stripper)
    return (
        pyparsing.Word(pyparsing.alphanums) ^
        qstr).setResultsName(name)

class CommandType(type):
    commands = {}
    def __new__(cls, name, bases, attrs):
        infrastructure = attrs.pop('infrastructure', False)
        t = super(CommandType, cls).__new__(cls, name, bases, attrs)
        if not infrastructure:
            cls.commands[reflect.qual(t)] = t
        return t

    def parse(self, player, line):
        for cls in self.commands.values():
            try:
                match = cls.match(player, line)
            except pyparsing.ParseException:
                pass
            else:
                if match is not None:
                    match = dict(match)
                    for k,v in match.items():
                        if isinstance(v, pyparsing.ParseResults):
                            match[k] = v[0]
                    return cls().run(player, line, **match)
        return defer.fail(eimaginary.NoSuchCommand(line))

class Command(object):
    __metaclass__ = CommandType
    infrastructure = True

    def match(cls, player, line):
        return cls.expr.parseString(line)
    match = classmethod(match)

