# -*- test-case-name: reality.test_reality -*-

from actions import NoTargetAction, TargetAction, ToolAction
from reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from twisted.python.components import Interface, implements


class BlowUp(ToolAction):
    """Simple action to demonstrate parser functionality.
    """

class Extinguish(ToolAction):
    """Simple action to demonstrate parser functionality.
    """

class ExplosivesParser(Subparser):
    simpleToolParsers = {
        "blow_up": BlowUp,
        "explode": BlowUp,
        "put_out": Extinguish,
        "blow_out": Extinguish,
        "blow": Extinguish,
        "blow_at": Extinguish
        }

registerSubparser(ExplosivesParser())

