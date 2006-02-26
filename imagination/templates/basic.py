from zope.interface import implementedBy
from imagination import simulacrum, containment, architecture, observation, simdata, social, scrutinize
from imagination.text import english


Thing = simdata.baseTemplate[
    (simulacrum.ICollector, containment.ILinkable): containment.Container,
    containment.ILocatable: containment.ContainerMobility,
    english.INoun: english.ProperNoun]

Actor = Thing[
    english.IThinker: english.Parsing,
    observation.ILookActor: observation.Looker,
    scrutinize.IScrutinizeActor: scrutinize.Scrutinizeer,

    (simulacrum.ISeer, simulacrum.IHearer): simulacrum.Sensibility,

    architecture.IEnterActor: architecture.Enterer,
    (architecture.IOpenActor, architecture.ICloseActor): architecture.OpenCloseActor,

    (containment.ITakeActor,
     containment.IPutActor,
     containment.IDropActor): containment.Owner,

    social.ISayActor: social.Speaker,
    ]

Book = Thing.copy()

Room = Thing.copy()

# Room = Thing[
#     simulacrum.IPlace: architecture.IndoorPointOfInterest,
#     ]

from imagination import architecture

Portal = Thing[
    list(implementedBy(architecture.Portal)): architecture.Portal,
    ].fill(containment.ILocatable, mobile=False)

Door = Thing[
    list(implementedBy(architecture.Door)): architecture.Door,
    ].fill(containment.ILocatable, mobile=False)

##Roach = Thing[
##    roach.IRoach: roach.Roach,
##    ]
