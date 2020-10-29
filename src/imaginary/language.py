# -*- test-case-name: imaginary.test.test_language -*-
"""

Textual formatting for game objects.

"""
import types
from string import Formatter

from zope.interface import implements, implementer

from characteristic import attributes

from twisted.python.components import registerAdapter

from imaginary import iimaginary, iterutils, text as T
from imaginary.iimaginary import IConcept, IExit

class Gender(object):
    """
    enum!
    """
    MALE = 1
    FEMALE = 2
    NEUTER = 3
    INDETERMINATE = 4



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


    def _declension(self, male, female, indeterminate, neuter):
        """
        Produce a declension based on the grammatical gender of the wrapped
        L{Thing}.

        @param male: the male declension of the specified pronoun
        @type male: L{unicode}

        @param female: the female declension of the specified pronoun
        @type female: L{unicode}

        @param indeterminate: the indeterminate declension of the specified
            pronoun
        @type indeterminate: L{unicode}

        @param neuter: the neuter declension of the specified pronoun
        @type neuter: L{unicode}

        @return: one of the parameters
        @rtype: L{unicode}
        """
        return ExpressString({
            Gender.MALE: male,
            Gender.FEMALE: female,
            Gender.INDETERMINATE: indeterminate,
        }.get(self.thing.gender, neuter))


    def heShe(self):
        """
        Return the personal pronoun for the wrapped thing.
        """
        return self._declension(u'he', u'she', u'they', u'it')


    def himHer(self):
        """
        Return the objective pronoun for the wrapped thing.
        """
        return self._declension(u'him', u'her', u'them', u'it')


    def hisHer(self):
        """
        Return a possessive determiner for the wrapped thing.
        """
        return self._declension(u'his', u'her', u'their', u'its')


    def hisHers(self):
        """
        Return a substantival possessive pronoun for the wrapped thing.
        """
        return self._declension(u'his', u'hers', u'theirs', u'its')



def flattenWithoutColors(vt102):
    return T.flatten(vt102, useColors=False)


@implementer(iimaginary.IConcept)
class BaseExpress(object):

    def __init__(self, original):
        self.original = original


    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))



@implementer(IConcept)
@attributes(["title", "exits", "description", "components", "target"],
            defaults=dict(target=None))
class Description(object):

    def plaintext(self, observer):
        return flattenWithoutColors(self.vt102(observer))


    def vt102(self, observer):
        title = [T.bold, T.fg.green, u'[ ',
                 [T.fg.normal, IConcept(self.title).vt102(observer)],
                 u' ]\n']
        yield title
        exits = list(
            IConcept(exit.name).vt102(observer)
            for exit in (self.exits or ())
            if exit.shouldEvenAttemptTraversalFrom(self.target,
                                                   observer))
        if exits:
            yield [
                T.bold, T.fg.green, u'( ', [
                    T.fg.normal, T.fg.yellow,
                    iterutils.interlace(
                        u' ', exits)],
                    u' )', u'\n']
        if self.description:
            yield (T.fg.green, self.description, u'\n')
        if self.components:
            yield iterutils.interlace(
                u"\n",
                filter(None,
                       (component.vt102(observer)
                        for component in self.components)))


    @classmethod
    def fromVisualization(cls, target, others):
        """
        Create a L{Description} from a L{Thing} and some L{Paths} visually
        related to that L{Thing}.

        @param target: The L{IThing} being described by this L{Description}.
        @type target: L{IThing}

        @param others: Paths to items that are visible as portions of the
            target.
        @type others: L{list} of L{Path <imaginary.idea.Path>}s.

        @return: A L{Description} comprising C{target} and C{others}.
        """
        exits = []
        for other in others:
            # All of others are paths that go through target so just
            # using targetAs won't accidentally include any exits that aren't
            # for the target room except for the bug mentioned below.
            #
            # TODO: This might show too many exits.  There might be exits to
            # rooms with exits to other rooms, they'll all show up as on some
            # path here as IExit targets.  Check the exit's source to make sure
            # it is target.
            anExit = other.targetAs(IExit)
            if anExit is not None:
                exits.append(anExit)

        exits.sort(key=lambda anExit: anExit.name)

        descriptionConcepts = []

        for pup in target.powerupsFor(iimaginary.IDescriptionContributor):
            descriptionConcepts.append(pup.contributeDescriptionFrom(others))

        def index(c):
            # https://github.com/twisted/imaginary/issues/63
            preferredOrder = [
                'ExpressCondition',
                'ExpressClothing',
            ]
            try:
                return preferredOrder.index(c.__class__.__name__)
            except ValueError:
                # Anything unrecognized goes after anything recognized.
                return len(preferredOrder)

        descriptionConcepts.sort(key=index)

        return cls(
            title=Noun(target).shortName(),
            exits=exits,
            description=target.description,
            components=descriptionConcepts,
            target=target,
        )



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
        self.listOfConcepts = list(listOfConcepts)


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
