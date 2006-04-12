# -*- test-case-name: imaginary.test.test_language -*-

"""

Textual formatting for game objects.

"""
from zope.interface import implements

from twisted.python.components import registerAdapter

from imaginary.iimaginary import IConcept

from imaginary.places import Gender



def express(concept, observer):
    """
    This is the top-level entrypoint for expressing a concept to an observer.

    For example, you can use it like this:

        bob = Person()
        food = SomeEdibleThing()
        express([bob, ' eats the ', food], # the concept
                bob)

    """
    return IConcept(concept).expressTo(observer)


class Noun:
    """
    This is a language wrapper around a Thing.

    It is separated into its own class for two reasons:

     - You should try to keep your game-logic self-contained and avoid
       polluting it with lots of constant strings, so that porting to new
       interfaces (text prototype -> isometric final implementation) is easy.
       It's easier to read the code that way and make changes to the logic even
       if you don't want to move to a different interface.


     - It would be nice if text games could be internationalized by separating
       the formatting logic from the game logic.  In an extreme case, it would
       be SUPER-COOL if people could be playing the same game in french and
       english on the same server, simply by changing a setting on their
       client.

    """

    implements(IConcept)

    def __init__(self, original, unique=False):
        self.original = original
        self.unique = False

    def expressTo(self, observer):
        return self.nounPhrase(observer)

    def nounPhrase(self, observer):
        return (self.article(observer) + self.shortName(observer))

    def article(self, observer):
        if self.unique:
            return self.definiteArticle(observer)
        else:
            return self.indefiniteArticle(observer)

    def indefiniteArticle(self, observer):
        if self.original.name[0].lower() in u'aeiou':
            return u'an '
        return u'a '

    def definiteArticle(self, observer):
        return u'the '

    def shortName(self, observer):
        return self.original.name

    def containerPreposition(self, content, observer):
        """When this object acts as a container, this is the preposition that
        objects will be in relation to it."""
        return u"on"

    def containedPhrase(self, observer, containerNoun):
        # A self is container.preposition the container
        return u"%s is %s %s." % (
            self.nounPhrase(observer),
            containerNoun.containerPreposition(self, observer),
            containerNoun.nounPhrase(observer))

    def presentPhrase(self, observer):
        # ugh: this is terrible.
        if self.original.location == observer.location:
            return "%s is here." % self.nounPhrase(observer)
        else:
            return self.containedPhrase(self)

    def heShe(self, observer):
        if self.original.gender == Gender.MALE:
            return 'he'
        elif self.original.gender == Gender.FEMALE:
            return 'she'
        else:
            return 'it'

    def himHer(self, observer):
        if self.original.gender == Gender.MALE:
            return 'him'
        elif self.original.gender == Gender.FEMALE:
            return 'her'
        else:
            return 'its'

    def hisHer(self, observer):
        if self.original.gender == Gender.MALE:
            return 'his'
        elif self.original.gender == Gender.FEMALE:
            return 'her'
        else:
            return 'its'

class Facet:
    def __init__(self, original):
        self.original = original

class _ExpressSeq(Facet):
    def expressTo(self, observer):
        return ''.join([IConcept(x).expressTo(observer) for x in self.original])

class _ExpressNothing(Facet):
    def expressTo(self, observer):
        return ''

class _ExpressYourself(Facet):
    def expressTo(self, observer):
        return self.original

class _FunctionAsConcept(Facet):
    def expressTo(self, observer):
        return self.original(observer)

registerAdapter(_ExpressSeq, tuple, IConcept)
registerAdapter(_ExpressSeq, list, IConcept)
registerAdapter(_ExpressNothing, type(None), IConcept)

registerAdapter(_ExpressYourself, str, IConcept)
registerAdapter(_ExpressYourself, unicode, IConcept)

registerAdapter(_FunctionAsConcept, type(lambda observer: None), IConcept)

def _g():
    yield None

registerAdapter(_ExpressSeq, type(_g()), IConcept)

class ItemizedList:
    implements(IConcept)

    def __init__(self, listOfConcepts):
        self.listOfConcepts = listOfConcepts

    def expressTo(self, observer):
        return IConcept(
            itemizedStringList(self.listOfConcepts[:])).expressTo(observer)

def itemizedStringList(desc):
    if len(desc) == 1:
        return desc[0]
    origLen = len(desc)
    didOneAnd = False
    for x in xrange(len(desc) - 1):
        if didOneAnd:
            thingToInsert = u', '
        else:
            thingToInsert = u' and '
            didOneAnd = True
        desc.insert(origLen - (x+1), thingToInsert)
    return desc

