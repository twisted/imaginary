from zope.interface import Interface


class IUI(Interface):
    def presentMenu(list, typename=None):
        """
        Present 'list' of 'typename's as a menu to the user; return a
        Deferred of an index into the list.
        """

    def presentEvent(iface, event):
        """
        Present an event!
        """
