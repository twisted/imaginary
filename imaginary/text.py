# -*- test-case-name: imaginary.test.test_text -*-

import pprint

from twisted.conch.insults import insults

class _structlike(list):
    __names__ = []
    __slots__ = []
    __defaults__ = []

    def _name2slot(self, name):
        return self.__names__.index(name)

    def __init__(self, *args, **kw):
        super(_structlike, self).__init__()

        # Turn all the args into kwargs
        for n, v in zip(self.__names__, args):
            if n in kw:
                raise TypeError("Got multiple values for argument " + n)
            kw[n] = v

        # Fill in defaults
        for n, v in zip(self.__names__[::-1], self.__defaults__[::-1]):
            if n not in kw:
                kw[n] = v

        self.extend([None] * len(self.__names__))
        for n in self.__names__:
            self[self._name2slot(n)] = kw[n]

    def __getattr__(self, attr):
        try:
            return self[self._name2slot(attr)]
        except (IndexError, ValueError):
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        try:
            self[self._name2slot(attr)] = value
        except ValueError:
            if attr.startswith('__') and attr.endswith('__'):
                super(_structlike, self).__setattr__(attr, value)
            raise AttributeError(attr)

class _unset(object):
    def __nonzero__(self):
        return False
unset = _unset()

class AttributeSet(_structlike):
    """
    @ivar bold: True, False, or unset, indicating whether characters
    with these attributes will be bold, or if boldness should be
    inherited from the previous setting.

    @ivar underline: Similar to C{bold} but indicating the underlined
    state of characters.

    @ivar reverseVideo: Similar to C{bold} but indicating whether
    reverse video should be applied.

    @ivar blink: Similar to C{bold} but indicating whether foreground
    material should blink.

    @ivar fg: An integer between 0 and 9 inclusive or unset.
    Integer values indicate a color setting for the foreground,
    whereas unset indicates foreground color should be inherited from
    the previous settings.

    @ivar bg: Like C{fg} but for background color.
    """

    __names__ = [
        'bold', 'underline', 'reverseVideo', 'blink',
        'fg', 'bg']

    __defaults__ = [
        False, False, False, False, '9', '9']

    def __init__(self, *a, **kw):
        _structlike.__init__(self, *a, **kw)
        assert self.fg is unset or self.fg in '012345679'
        assert self.bg is unset or self.bg in '012345679'
        assert self.bold is unset or self.bold in (True, False)
        assert self.underline is unset or self.underline in (True, False)
        assert self.reverseVideo is unset or self.reverseVideo in (True, False)
        assert self.blink is unset or self.blink in (True, False)

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(['='.join((k, str(v)))
                       for (k, v)
                       in zip(self.__names__, self)
                       if v is not unset]))

    def clone(self):
        return self.__class__(*self)

    def update(self, other):
        for i in range(len(self)):
            if other[i] is not unset:
                self[i] = other[i]
        return self

    _flags = {'bold': '1', 'underline': '4', 'reverseVideo': '7', 'blink': '5'}
    def toVT102(self, state):
        passive = []
        active = []
        reset = False

        for attr in 'bold', 'underline', 'reverseVideo', 'blink':
            was = getattr(state, attr)
            willBe = getattr(self, attr)

            if was is unset:
                if willBe is unset:
                    # Absolutely nothing to do here.
                    pass
                elif willBe:
                    # We're going to turn it on.  Yay.
                    active.append(self._flags[attr])
                else:
                    # We're going to turn it off.  Yay.
                    reset = True
            elif was:
                if willBe is unset:
                    # Who cares!  But make a note.
                    passive.append(self._flags[attr])
                elif willBe:
                    # Nothing to do!  But make a note.
                    passive.append(self._flags[attr])
                else:
                    # Time to destroy!  Zoom.
                    reset = True
            else:
                if willBe is unset:
                    # Big woop!  Die.
                    pass
                elif willBe:
                    # Enablement now.
                    active.append(self._flags[attr])
                else:
                    # Consensus is neat.
                    pass

        for x, attr in ('3', 'fg'), ('4', 'bg'):
            was = getattr(state, attr)
            willBe = getattr(self, attr)

            if was is unset:
                if willBe is unset:
                    # Boringly do nothing.
                    pass
                elif willBe == '9':
                    # Again there is no work.
                    pass
                else:
                    # Wee it is time for colorizing.
                    active.append(x + willBe)
            elif was == '9':
                if willBe is unset:
                    # We don't care.  Snore.
                    pass
                elif willBe == '9':
                    # We are happily already in the state desired.
                    pass
                else:
                    # Time for mashin'.
                    active.append(x + willBe)
            else:
                if willBe is unset:
                    # We don't care about the color.
                    passive.append(x + was)
                elif willBe == '9':
                    # Reset the entire state to put this back to normal
                    reset = True
                elif willBe == was:
                    # It is correct already.  Good night.
                    passive.append(x + was)
                else:
                    # Just switch the color
                    active.append(x + willBe)

        if reset:
            active.extend(passive)
            active.insert(0, '0')

        if active:
            return '\x1b[' + ';'.join(active) + 'm'
        return ''


class AttributeStack(object):
    def __init__(self, initialAttributes):
        self._stack = [initialAttributes]

    def __repr__(self):
        return pprint.pformat(self._stack)

    def __len__(self):
        return len(self._stack)

    def push(self, attrs):
        self._stack.append(self.get().clone().update(attrs))

    def duptop(self):
        self._stack.append(self.get().clone())

    def update(self, attrs):
        self.get().update(attrs)

    def pop(self):
        return self._stack.pop()

    def get(self):
        return self._stack[-1]

class fg:
    pass

class bg:
    pass

neutral = AttributeSet(unset, unset, unset, unset, unset, unset, unset)

for cls, attr in [(fg, 'fg'),
                  (bg, 'bg')]:
    for n, color in enumerate(['black', 'red', 'green', 'yellow', 'blue',
                               'magenta', 'cyan', 'white']):
        value = neutral.clone()
        setattr(value, attr, str(n))
        setattr(cls, color, value)
    cls.normal = neutral.clone()
    setattr(cls.normal, attr, '9')
del n, cls, attr, color

for attr in 'bold', 'blink', 'reverseVideo', 'underline':
    value = neutral.clone()
    setattr(value, attr, True)
    locals()[attr] = value

def flatten(*dag, **kw):
    currentAttrs = kw.pop('currentAttrs')
    attrs = AttributeStack(currentAttrs)
    attrs.duptop()

    if kw:
        raise TypeError(
            "flatten takes only `currentAttrs' as a keyword argument")

    stack = [iter(dag)]
    dirty = False
    while stack:
        try:
            obj = stack[-1].next()
        except StopIteration:
            stack.pop()
            attrs.pop()
            if len(attrs):
                dirty = bool(attrs.get().toVT102(currentAttrs))
        else:
            if isinstance(obj, AttributeSet):
                attrs.update(obj)
                dirty = bool(attrs.get().toVT102(currentAttrs))
            elif isinstance(obj, (str, unicode)):
                if obj:
                    if dirty:
                        yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
            else:
                try:
                    newIter = iter(obj)
                except TypeError:
                    if dirty:
                        yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
                else:
                    stack.append(newIter)
                    attrs.duptop()
    if dirty and len(attrs):
        yield attrs.get().toVT102(currentAttrs)

__all__ = [
    'fg', 'bg',
    'flatten']

if __name__ == '__main__':
    print repr(''.join(list(flatten(
        [fg.red, bg.blue, bold, ['hello world']], '\n',
        [fg.blue, bg.red, blink, ['how are you?']], '\n',
        [fg.blue, [bg.red, [blink, 'how'], ' are'], ' you?'], '\n'))))
