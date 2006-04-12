# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2002 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#evil, evil, evil hack.

import sys, re
import token, tokenize


class FoundEnd(Exception): pass

class SourceFinder:
    def __init__(self):
        self.indents = None
        self.line = 0
        self.lines = []
        
    def findSource(self, obj):
        try:
            c = obj.__class__
        except AttributeError:
            raise ValueError("Doesn't seem to be an instance of a python class")
        cname = c.__name__
        mname = c.__module__
        try:
            fname = sys.modules[mname].__file__
        except AttributeError:
            raise ValueError("This class does not seem to live in a module which is defined as a file.")
        if fname.endswith('.pyc'):
            fname = fname[:-1]
        #here comes the wizardry
        f = open(fname, 'r')

        while 1:
            prevpos = f.tell()
            line = f.readline()
            if line.find("class %s" % cname) != -1:

                try:
                    f.seek(prevpos) # we need to seek back so the tokenizer can have this line.
                    tokenize.tokenize(f.readline, self.eatToken)
                except FoundEnd:
                    return self.lines[:-1] #for some reason, we don't get the
                                           #final dedent till _after_ the line
                                           #that _really_ does the dedent...

            

## The generator produces 5-tuples with these members: the token type; the token
## string; a 2-tuple (srow, scol) of ints specifying the row and column where the
## token begins in the source; a 2-tuple (erow, ecol) of ints specifying the row
## and column where the token ends in the source; and the line on which the token
## was found. The line passed is the logical line; continuation lines are
## included. New in version 2.2.

    def eatToken(self, type, st, bloc, eloc, line):
        if type == token.INDENT:
            try:
                self.indents += 1
            except TypeError:
                self.indents = 1
            
        elif type == token.DEDENT:
            self.indents -= 1
            
        if self.indents == 0:
            raise FoundEnd

        if not bloc[0] == self.line:
            self.lines.append(line[:-1])
            self.line = bloc[0]



def findSource(obj):
    return SourceFinder().findSource(obj)


if __name__ == '__main__':
    sys.path.append('/home/chris/Projects/Twisted')
    sys.path.append('/home/chris/Projects/Reality')
    from reality import realities
    r = realities.Reality()
    for x in findSource(r): print x
