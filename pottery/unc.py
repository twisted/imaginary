def getInt(i):
    d = ''
    for c in i:
        if not c.isdigit():
            return d, c
        d = d+c

ss = '\x1b[31;42;4mhello\x1b[0;31;42m \x1b[0;31mworld\x1b[0m'
BEGIN, END, ADD, NUMBER, CHAR, ATTS, STR = range(7)

def tokenize(s):
    s = iter(s)
    for c in s:
        if c != '\x1b':
            yield CHAR, c
            continue
        c = s.next()
        if c != '[':
            yield CHAR, '\x1b'
            yield CHAR, c
            continue
        yield BEGIN, c
        while 1:
            d, c = getInt(s)
            yield NUMBER, d
            if c == 'm':
                yield END, c
                break

def parser(tokens):
    tokens = iter(tokens)
    sofar = ''
    for tp, token in tokens:
        if tp == CHAR:
            sofar += token
        if tp == BEGIN:
            if sofar:
                yield STR, sofar
                sofar = ''
            atts = []
            for tp, token in tokens:
                if tp == END:
                    break
                atts.append(int(token))
            yield ATTS, atts
    if sofar:
        yield STR, sofar
        sofar = ''

def prettylist(l):
    res = []
    for tp, data in l:
        if tp == ATTS:
            res.append('COLOR('+', '.join(map(str, data))+')\n')
        else:
            res.append(repr(data)+'\n')
    return ''.join(res)

def prettystring(s):
    return prettylist((parser(tokenize(s))))

def _test():
    print prettystring(ss)

if __name__ == '__main__':
    _test()
