class atLeastOne(object):
    def __init__(self, methodName, *objs):
        self.methodName = methodName
        self.objs = objs

    def __call__(self, obj):
        for o in self.objs:
            if getattr(obj, self.methodName)(o):
                return True
        return False

class isNot(object):
    def __init__(self, *objs):
        self.objs = objs

    def __call__(self, obj):
        for o in self.objs:
            if o is obj:
                return False
        return True

class And(object):
    def __init__(self, *what):
        self.what = what

    def __call__(self, obj):
        for w in self.what:
            if not w(obj):
                return False
        return True
