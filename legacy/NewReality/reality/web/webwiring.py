

import os

from twisted.python import components
from twisted.web import microdom, server
from twisted.web.woven import page, interfaces, widgets, input

from reality.text import common
from reality import things
from reality import errors
from reality import observation
from reality import ambulation


class IOutputSession(components.Interface):
    """Hold the output from a user's session.
    """
    def append(output):
        """Append a line, flushing any lines over 200
        """
    
    def read():
        """Read the current output
        """


class OutputSession(components.Adapter):
    __implements__ = (IOutputSession, )
    def __init__(self, original):
        components.Adapter.__init__(self, original)
        self.output = []
    
    def append(self, output):
        wid, node = ToHTML(output), microdom.Element('span')
        wid.setNode(node)
        output = wid.generate(self.request, node).toxml()
        self.appendRaw(output)

    def appendRaw(self, output):
        output = output.replace('\n', '')
        output = output.replace('\r', '')
        output = output.replace("\\", "\\\\")
        output = output.replace("'", "\\'")
        self.output.append(output)
        if len(self.output) > 200:
            self.output.remove(0)
        # Here's the key; update the page
        self.live.sendScript("top.woven_appendChild('%s', '%s')" % ('output', output) )

    def read(self):
        return self.output


components.registerAdapter(OutputSession, server.Session, IOutputSession)


class ToHTML(widgets.Widget):
    def setUp(self, request, node, data):
        spl = data.split('\n')
        for l in spl:
            div = microdom.Element('div')
            div.appendChild(microdom.Text(l))
            self.add(div)


def doIt(doWhat, person, out):
        try:
            person.getComponent(common.IThinker).parse(doWhat)
        except things.Refusal, ref:
            out.append(common.express(ref.whyNot, person))
        except errors.RealityException, re:
            out.append(common.express(re, person))


class SubmitInput(input.Anything):
    def initialize(self):
        self.view.addEventHandler(
            "onsubmit", 
            self.onInput, 
            'document.getElementById(\'woven_firstResponder\').value')

    def onInput(self, request, widget, arg):
        doIt(arg, self.model.person, self.model.out)


class LookInput(input.Anything):
    def initialize(self):
        data = self.model.original
        noun = data.getComponent(common.INoun)
        self.view.addEventHandler("onclick", self.lookItem, '\'%s\'' % noun.name)

    def lookItem(self, request, widget, arg):
        top = widget.getTopModel()
        doIt("look " + arg, top.person, top.out)


class DirectionInput(input.Anything):
    def initialize(self):
        ## arg why is getTopModel not on the model duh
        top = self.model
        while top.parent is not None:
            top = top.parent
        direction = self.model.original.direction
        if self.model.original.source is not top.person.location:
            direction = ambulation.opposite(direction)
        self.view.addEventHandler("onclick", self.goDirection, '\'%s\'' % direction)

    def goDirection(self, request, widget, arg):
        top = widget.getTopModel()
        doIt("go "+arg, top.person, top.out)


def getStuffInTargetForPerson(target, person):
    collected = target.collectImplementors(
       person, things.IThing, {}, {}).values()

    inventory = [x for x in collected 
        if x is not target 
        and x is not person
        and getattr(x.getComponent(things.IThing), 'location', None) == target]
    return inventory

class RealityPage(page.LivePage):
    templateDirectory = os.path.join(os.path.split(__file__)[0], 'templates')

    def __init__(self, person, *args, **kwargs):
        self.person = person
        self.latestOutput = []
        # Make sure the Page instance is it's own model by not passing a model,
        # so that wmfactory_ methods defined here will work
        page.LivePage.__init__(self, *args, **kwargs)

    def setUp(self, request, d=None):
        self.request = request
        self.out = request.getSession(IOutputSession)
        self.live = request.getSession(interfaces.IWovenLivePage)
        self.out.request = request
        self.out.live = self.live
        self.person.setComponent(things.IEventReceiver, self)
        self.person.setComponent(things.IMoveListener, self)

        self.person.getComponent(common.IThinker).parse("look")

    def wchild_index(self, request):
        return self.makeView(self.person, "WebWiring.html")

    def eventReceived(self, emitter, evt):
        print "evt recvd ", emitter, evt
        ## implements(conveyance.ITake)?
        if isinstance(evt, things.MovementEvent):
            # All you should need to do is self.model.getSubmodel("roomContents").notify()
            self.model.getSubmodel("roomContents").notify({'request': self.request})
            self.model.getSubmodel("playerInventory").notify({'request': self.request})

        desc = common.express(evt, self.person)
        self.out.append( desc )

    def thingMoved(self, emitter, event):
        if emitter is self.person:
            self.person.getComponent(common.IThinker).parse("look")
            # refactor MethodModel to rerun the method on notify
            # make notify clear out submodel cache, too
            self.model.getSubmodel("roomExits").notify({'request': self.request})
            self.model.getSubmodel("roomContents").notify({'request': self.request})

    def thingArrived(self, emitter, event):
        self.out.append( common.express(event, self.person) )
        #self.out.append('thingArrived' + str(emitter)+str(event))

    def thingLeft(self, emitter, event):
        self.out.append( common.express(event, self.person) )
        #self.out.append('thingLeft' + str(emitter)+str(event))

    def wmfactory_latestOutput(self, request):
        ## not really using this any more; just using eventReceived to get output to browser
        return []
        print "retrv output ", self.out.output
        return self.out.read()

    def wmfactory_roomContents(self, request):
        return getStuffInTargetForPerson(self.person.location, self.person)

    def wmfactory_roomExits(self, request):
        collected = self.person.location.collectImplementors(self, things.IThing, {}, {}, intensity=1).values()
        return [x for x in collected if isinstance(x, ambulation.Exit)]

    def wmfactory_playerInventory(self, request):
        return getStuffInTargetForPerson(self.person, self.person)

    def wcfactory_look(self, request, node, m):
        return LookInput(m)

    def wcfactory_exit(self, request, node, m):
        return DirectionInput(m)

    def wvupdate_item(self, request, wid, data):
        wid['class'] = 'item'
        noun = data.getComponent(common.INoun)
        if noun is not None:
            wid.add(widgets.Text(noun.nounPhrase(self.person)))
        dcomp = data.getComponent(common.IDescribeable)
        desc = dcomp.explainTo(self.person, component='html')
        if not desc:
            desc = dcomp.explainTo(self.person)
        if desc:
            wid.add(widgets.Text(": " + desc, raw=1))

    def wvfactory_html(self, request, node, m):
        return ToHTML(m)

    def wcfactory_submitInput(self, request, node, m):
        return SubmitInput(m)
    
    def wvupdate_compassRose(self, request, wid, data):
        wid.clearNode = 1
        top = wid.getTopModel()
        loc = top.person.location
        valid = [
            x.source is loc and x.direction or ambulation.opposite(x.direction) 
            for x in data]
        for row in [
            ['Northwest', 'North', 'Northeast'], 
            ['West', 'Look', 'East'], 
            ['Southwest', 'South', 'Southeast']]:
            curRow = wid.getPattern('row', deep=0)
            wid.add(curRow)
            for direction in row:
                elm = wid.getPattern('element')
                if direction.lower() in valid:
                    elm.appendChild(microdom.Text(direction))
                    widgets.appendModel(elm, valid.index(direction.lower()))
                    elm.setAttribute('controller',  'exit')
                    elm.setAttribute('view', 'Widget')
                    elm.setAttribute('style', 'cursor: pointer')
                else:
                    elm.appendChild(microdom.Text('&nbsp;', raw=1))
                curRow.appendChild(elm)
                
            

