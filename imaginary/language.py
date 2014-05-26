# -*- test-case-name: imaginary.test.test_look -*-

"""

Textual formatting for game objects.

"""
import types
from string import Formatter

from zope.interface import implements, implementer

from twisted.python.components import registerAdapter

from epsilon import structlike

from imaginary import iimaginary, iterutils, text as T
from imaginary.iimaginary import IConcept, IExit


class Gender(object):
    """
    enum!
    """
    MALE = 1
    FEMALE = 2
    NEUTER = 3



class Noun(object):
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


    def __init__(self, thing):
        self.thing = thing


    def shortName(self):
        return ExpressString(self.thing.name)


    def nounPhrase(self):
        if self.thing.proper:
            return self.shortName()
        return ExpressList([self.indefiniteArticle(), self.shortName()])


    def definiteNounPhrase(self):
        if self.thing.proper:
            return self.shortName()
        return ExpressList([self.definiteArticle(), self.shortName()])


    def indefiniteArticle(self):
        # XXX TODO FIXME: YTTRIUM
        if self.thing.name[0].lower() in u'aeiou':
            return u'an '
        return u'a '


    def definiteArticle(self):
        return u'the '


    def heShe(self):
        """
        Return the personal pronoun for the wrapped thing.
        """
        x = {Gender.MALE: u'he',
             Gender.FEMALE: u'she'
             }.get(self.thing.gender, u'it')
        return ExpressString(x)


    def himHer(self):
        """
        Return the objective pronoun for the wrapped thing.
        """
        x = {Gender.MALE: u'him',
             Gender.FEMALE: u'her'
             }.get(self.thing.gender, u'it')
        return ExpressString(x)


    def hisHer(self):
        """
        Return a possessive pronoun that cannot be used after 'is'.
        """
        x = {Gender.MALE: u'his',
             Gender.FEMALE: u'her' # <-- OMG! hers!
             }.get(self.thing.gender, u'its')
        return ExpressString(x)


    #FIXME: add his/hers LATER



def flattenWithoutColors(vt102):
    return T.flatten(vt102, useColors=False)


@implementer(iimaginary.IConcept)
class BaseExpress(object):

    def __init__(self, original):
        self.original = original


    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))



@implementer(IConcept)
class DescriptionWithContents(structlike.record("target others")):
    """
    A description of a target with some context.

    @ivar target: an L{IThing}

    @ivar others: some L{Path} objects pointing at objects related to
        C{target}.
    """

    def capitalizeConcept():
        return "Smash the patriarchy"


    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))


    def vt102(self, observer):
        """
        some text
        """
        title = [T.bold, T.fg.green, u'[ ',
                 [T.fg.normal, Noun(self.target).shortName().vt102(observer)],
                 u' ]\n']

        yield title

        # TODO: Think about how to do better than this special-case support for
        # IExit.  For example have some powerups on the observer that get a
        # chance to inspect others and do the formatting.
        exits = []
        for other in self.others:
            # All of self.others are paths that go through self.target so just
            # using targetAs won't accidentally include any exits that aren't
            # for the target room except for the bug mentioned below.
            # 
            # TODO: This might show too many exits.  There might be exits to
            # rooms with exits to other rooms, they'll all show up as on some
            # path here as IExit targets.  Check the exit's source to make sure
            # it is self.target.
            exit = other.targetAs(IExit)
            if exit is not None:
                nameConcept = IConcept(exit.name)
                namePileOfVT102Sequences = nameConcept.vt102(observer)
                exits.append(namePileOfVT102Sequences)
                print("Found an exit on", other, ":", exit.name)

        if exits:
            yield [T.bold, T.fg.green, u'( ',
                   [T.fg.normal, T.fg.yellow,
                    iterutils.interlace(u' ', exits)],
                   u' )', u'\n']

        description = self.target.description or u""
        if description:
            description = (T.fg.green, description, u'\n')

        descriptionConcepts = []

        for pup in self.target.powerupsFor(iimaginary.IDescriptionContributor):
            descriptionConcepts.append(pup.conceptualize())

        def index(c):
            preferredOrder = DescriptionConcept.preferredOrder
            try:
                return preferredOrder.index(c.__class__.__name__)
            except ValueError:
                # Anything unrecognized goes after anything recognized.
                return len(preferredOrder)

        descriptionConcepts.sort(key=index)

        descriptionComponents = []
        for c in descriptionConcepts:
            s = c.vt102(observer)
            if s:
                descriptionComponents.extend([s, u'\n'])

        if descriptionComponents:
            descriptionComponents.pop()

        yield description
        yield descriptionComponents

        # for path in self.others:
        #     for nameable in path.eachTargetAs(IThing):
        #         yield u" / "
        #         yield Noun(nameable).shortName().vt102(observer)
        #     yield u"\n"




class DescriptionConcept(structlike.record('name description exits others',
                                           description=u"", exits=(), others=())):
    """
    A concept which is expressed as the description of a Thing as well as
    any concepts which power up that thing for IDescriptionContributor.

    Concepts will be ordered by the C{preferredOrder} class attribute.
    Concepts not named in this list will appear last in an unpredictable
    order.

    @ivar name: The name of the thing being described.

    @ivar description: A basic description of the thing being described, the
        first thing to show up.

    @ivar exits: An iterable of L{IExit}, to be listed as exits in the
        description.

    @ivar others: An iterable of L{IDescriptionContributor} that will
        supplement the description.
    """
    implements(iimaginary.IConcept)

    # This may not be the most awesome solution to the ordering problem, but
    # it is the best I can think of right now.  This is strictly a
    # user-interface level problem.  Only the ordering in the string output
    # send to the user should depend on this; nothing in the world should be
    # affected.
    preferredOrder = ['ExpressCondition',
                      'ExpressClothing',
                      'ExpressSurroundings',
                      ]

    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))


    def vt102(self, observer):
        exits = u''
        if self.exits:
            exits = [T.bold, T.fg.green, u'( ',
                     [T.fg.normal, T.fg.yellow,
                      iterutils.interlace(u' ',
                                          (exit.name for exit in self.exits))],
                     u' )', u'\n']

        description = self.description or u""
        if description:
            description = (T.fg.green, self.description, u'\n')

        descriptionConcepts = []

        for pup in self.others:
            descriptionConcepts.append(pup.conceptualize())

        def index(c):
            try:
                return self.preferredOrder.index(c.__class__.__name__)
            except ValueError:
                # Anything unrecognized goes after anything recognized.
                return len(self.preferredOrder)

        descriptionConcepts.sort(key=index)

        descriptionComponents = []
        for c in descriptionConcepts:
            s = c.vt102(observer)
            if s:
                descriptionComponents.extend([s, u'\n'])

        if descriptionComponents:
            descriptionComponents.pop()

        return [
            [T.bold, T.fg.green, u'[ ', [T.fg.normal, self.name], u' ]\n'],
            exits,
            description,
            descriptionComponents]



class ExpressNumber(BaseExpress):
    implements(iimaginary.IConcept)

    def vt102(self, observer):
        return str(self.original)



class ExpressString(BaseExpress):
    implements(iimaginary.IConcept)

    def __init__(self, original, capitalized=False):
        self.original = original
        self._cap = capitalized


    def vt102(self, observer):
        if self._cap:
            return self.original[:1].upper() + self.original[1:]
        return self.original


    def capitalizeConcept(self):
        return ExpressString(self.original, True)



class ExpressList(BaseExpress):
    implements(iimaginary.IConcept)

    def concepts(self, observer):
        return map(iimaginary.IConcept, self.original)

    def vt102(self, observer):
        return [x.vt102(observer) for x in self.concepts(observer)]

    def capitalizeConcept(self):
        return Sentence(self.original)




class Sentence(ExpressList):
    def vt102(self, observer):
        o = self.concepts(observer)
        if o:
            o[0] = o[0].capitalizeConcept()
        return [x.vt102(observer) for x in o]


    def capitalizeConcept(self):
        return self



registerAdapter(ExpressNumber, int, iimaginary.IConcept)
registerAdapter(ExpressNumber, long, iimaginary.IConcept)
registerAdapter(ExpressString, str, iimaginary.IConcept)
registerAdapter(ExpressString, unicode, iimaginary.IConcept)
registerAdapter(ExpressList, list, iimaginary.IConcept)
registerAdapter(ExpressList, tuple, iimaginary.IConcept)
registerAdapter(ExpressList, types.GeneratorType, iimaginary.IConcept)


class ItemizedList(BaseExpress):
    implements(iimaginary.IConcept)

    def __init__(self, listOfConcepts):
        self.listOfConcepts = listOfConcepts


    def concepts(self, observer):
        return self.listOfConcepts


    def vt102(self, observer):
        return ExpressList(
            itemizedStringList(self.concepts(observer))).vt102(observer)


    def capitalizeConcept(self):
        listOfConcepts = self.listOfConcepts[:]
        if listOfConcepts:
            listOfConcepts[0] = iimaginary.IConcept(listOfConcepts[0]).capitalizeConcept()
        return ItemizedList(listOfConcepts)



def itemizedStringList(desc):
    if len(desc) == 1:
        yield desc[0]
    elif len(desc) == 2:
        yield desc[0]
        yield u' and '
        yield desc[1]
    elif len(desc) > 2:
        for ele in desc[:-1]:
            yield ele
            yield u', '
        yield u'and '
        yield desc[-1]



class ConceptTemplate(object):
    """
    A L{ConceptTemplate} wraps a text template which may intersperse literal
    strings with markers for substitution.

    Substitution markers follow U{the syntax for str.format<http://docs.python.org/2/library/string.html#format-string-syntax>}.

    Values for field names are supplied to the L{expand} method.
    """
    def __init__(self, templateText):
        """
        @param templateText: The text of the template.  For example,
            C{u"Hello, {target:name}."}.
        @type templateText: L{unicode}
        """
        self.templateText = templateText


    def expand(self, values):
        """
        Generate concepts based on the template.

        @param values: A L{dict} mapping substitution markers to application
            objects from which to take values for those substitutions.  For
            example, a key might be C{u"target"}.  The associated value will be
            sustituted each place C{u"{target}"} appears in the template
            string.  Or, the value's name will be substituted each place
            C{u"{target:name}"} appears in the template string.
        @type values: L{dict} mapping L{unicode} to L{object}

        @return: An iterator the combined elements of which represent the
            result of expansion of the template.  The elements are adaptable to
            L{IConcept}.
        """
        parts = Formatter().parse(self.templateText)
        for (literalText, fieldName, formatSpec, conversion) in parts:
            if literalText:
                yield ExpressString(literalText)
            if fieldName:
                try:
                    target = values[fieldName.lower()]
                except KeyError:
                    extra = u""
                    if formatSpec:
                        extra = u" '%s'" % (formatSpec,)
                    yield u"<missing target '%s' for%s expansion>" % (
                        fieldName, extra)
                else:
                    if formatSpec:
                        # A nice enhancement would be to delegate this logic to
                        # target
                        try:
                            expander = getattr(
                                self, '_expand_' + formatSpec.upper()
                            )
                        except AttributeError:
                            yield u"<'%s' unsupported by target '%s'>" % (
                                formatSpec, fieldName)
                        else:
                            yield expander(target)
                    else:
                        yield target


    def _expand_NAME(self, target):
        """
        Get the name of a L{Thing}.
        """
        return target.name


    def _expand_PRONOUN(self, target):
        """
        Get the personal pronoun of a L{Thing}.
        """
        return Noun(target).heShe()
