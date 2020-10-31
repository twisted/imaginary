# -*- test-case-name: imaginary.test.test_text -*-

import pprint

import attr

class _unset(object):
    def __nonzero__(self):
        return False
unset = _unset()

_tristate = attr.validators.in_((True, False, unset))

@attr.s
class AttributeSet(object):
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
    bold = attr.ib(default=False, validator=_tristate)
    underline = attr.ib(default=False, validator=_tristate)
    reverseVideo = attr.ib(default=False, validator=_tristate)
    blink = attr.ib(default=False, validator=_tristate)
    fg = attr.ib(
        default="9",
        validator=attr.validators.in_([unset] + list("012345679")),
    )
    bg = attr.ib(
        default="9",
        validator=attr.validators.in_([unset] + list("012345679")),
    )

    def __len__(self):
        return 6


    def __getitem__(self, index):
        return [self.bold, self.underline, self.reverseVideo, self.blink, self.fg, self.bg][index]


    def __setitem__(self, index, value):
        setattr(self, ['bold', 'underline', 'reverseVideo', 'blink', 'fg', 'bg'][index], value)


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

        for attr_ in 'bold', 'underline', 'reverseVideo', 'blink':
            was = getattr(state, attr_)
            willBe = getattr(self, attr_)

            if was is unset:
                if willBe is unset:
                    # Absolutely nothing to do here.
                    pass
                elif willBe:
                    # We're going to turn it on.  Yay.
                    active.append(self._flags[attr_])
                else:
                    # We're going to turn it off.  Yay.
                    reset = True
            elif was:
                if willBe is unset:
                    # Who cares!  But make a note.
                    passive.append(self._flags[attr_])
                elif willBe:
                    # Nothing to do!  But make a note.
                    passive.append(self._flags[attr_])
                else:
                    # Time to destroy!  Zoom.
                    reset = True
            else:
                if willBe is unset:
                    # Big woop!  Die.
                    pass
                elif willBe:
                    # Enablement now.
                    active.append(self._flags[attr_])
                else:
                    # Consensus is neat.
                    pass

        for x, attr_ in ('3', 'fg'), ('4', 'bg'):
            was = getattr(state, attr_)
            willBe = getattr(self, attr_)

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

neutral = AttributeSet(unset, unset, unset, unset, unset, unset)

def _setup():
    for cls, attr_ in [(fg, 'fg'),
                      (bg, 'bg')]:
        for n, color in enumerate(['black', 'red', 'green', 'yellow', 'blue',
                                   'magenta', 'cyan', 'white']):
            value = neutral.clone()
            setattr(value, attr_, str(n))
            setattr(cls, color, value)
        cls.normal = neutral.clone()
        setattr(cls.normal, attr_, '9')

    for attr_ in 'bold', 'blink', 'reverseVideo', 'underline':
        value = neutral.clone()
        setattr(value, attr_, True)
        globals()[attr_] = value
_setup()
del _setup


def flatten(dag, currentAttrs=None, useColors=True):
    # XXX TODO: Add unicode handling!
    """
    Serialize a tree of strings and terminal codes to an iterable of strings,
    ready to be written to your favorite terminal device.

    @type currentAttrs: L{AttributeSet}
    @param currentAttrs: The current set of attributes.

    @param useColors: If False, terminal codes will be left out.
    """
    if currentAttrs is None:
        if not useColors:
            currentAttrs = AttributeSet()
        else:
            raise TypeError("currentAttrs is required when useColors is False")
    attrs = AttributeStack(currentAttrs)
    attrs.duptop()

    stack = [iter(dag)]
    dirty = False
    while stack:
        try:
            obj = stack[-1].next()
        except StopIteration:
            stack.pop()
            attrs.pop()
            if len(attrs):
                if useColors:
                    dirty = bool(attrs.get().toVT102(currentAttrs))
        else:
            if isinstance(obj, AttributeSet):
                attrs.update(obj)
                if useColors:
                    dirty = bool(attrs.get().toVT102(currentAttrs))
            elif isinstance(obj, (str, unicode)):
                if obj:
                    if dirty:
                        if useColors:
                            yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
            else:
                try:
                    newIter = iter(obj)
                except TypeError:
                    if dirty:
                        if useColors:
                            yield attrs.get().toVT102(currentAttrs)
                        currentAttrs = attrs.get().clone()
                        dirty = False
                    yield obj
                else:
                    stack.append(newIter)
                    attrs.duptop()
    if dirty and len(attrs):
        if useColors:
            yield attrs.get().toVT102(currentAttrs)



__all__ = [
    'fg', 'bg',
    'flatten']
