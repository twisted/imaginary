# Copyright 1997-1999 Greg Stein and Bill Tutt
#
# C code generator
#
# Generates C code (with a helper .py file) for an input module
#

import transformer
import string
import os
import types
import time
import marshal
import pprint

error = 'genc.error'

indentlevel = 0
cIndentSpaces = 4
INDENT = " " * cIndentSpaces

class objConstantPool:
  def __init__(self):
    self.objects = { }
    self.maxobject = 0
  def getConstant(self, reference, value):
    if self.objects.has_key(reference):
      return self.objects[reference]
    self.objects[reference] = ('cObj_%d' % self.maxobject, value)
    self.maxobject = self.maxobject + 1
    return self.objects[reference][0]
  def getCode(self):
    s = ''
    for k, v in self.objects.items():
      s = s + v[1] % { "objname" : v[0] }
    return s
  def getDeclarations(self):
    s = ''
    for k, v in self.objects.items():
      s = s + 'static PyObject *%s;\n' % v[0]
    return s

class ConstantPool:
  def __init__(self):
    # Key = constant value, value = C name
    self.ints = { }
    self.strings = { }
    self.maxint = 0
    self.maxstring = 0
  def getConstant(self, type, value):
    if type == 'int':
      if self.ints.has_key(value):
        return self.ints[value]
      self.ints[value] = 'cInt_%d' % self.maxint
      self.maxint = self.maxint + 1
      return self.ints[value]
    if type == 'string':
      if self.strings.has_key(value):
        return self.strings[value]
      self.strings[value] = 'cStr_%d' % self.maxstring
      self.maxstring = self.maxstring + 1
      return self.strings[value]
  def getDeclarations(self):
    s = ''
    for k in self.ints.keys():
      s = s + 'static PyObject *%s;\n' % self.ints[k]
    for k in self.strings.keys():
      s = s + 'static PyObject *%s;\n' % self.strings[k]
    return s

  def getCode(self):
    s = ''
    for k, v in self.ints.items():
      s = s + INDENT * (indentlevel + 1) + '%s = PyInt_FromLong(%d);\n' % (v, k)
    for k, v in self.strings.items():
      s = s + INDENT * (indentlevel + 1) + '%s = PyString_InternFromString("%s");\n' % (v, _cstr(k))
    return s

constantPool = ConstantPool()
objectConstantPool = objConstantPool()

class Generator:

  def __init__(self, input, cfile, pyfile):
    global identlevel
    
    self.input = input
    self.cmodule = os.path.splitext(os.path.split(cfile)[1])[0]

    t = transformer.Transformer()
    tree = t.parsefile(input)

    self.cfile = open(cfile, 'w')
    self.pyfile = open(pyfile, 'w')

    d = self._dispatch = { }
    for name, func in _node_names.items():
      d[name] = getattr(self, func)

    d = self._dispatchbuiltin = { }
    for name, func in _optimized_builtins.items():
      d[name] = getattr(self, func)

    self.dispatch(tree)
    self.cfile.flush()
    self.cfile.close()

  def indent(self, inc=0):
    return INDENT + INDENT * (indentlevel + inc)

  def indentCommentBlock(self, s, prefix=" * "):
    lines = string.split(s, '\n')
    s2 = ''
    for l in lines:
      s2 = s2 + self.indent() + prefix + l + "\n"

    return s2

  def incIndent(self):
    global indentlevel
    indentlevel = indentlevel + 1

  def decIndent(self):
    global indentlevel
    indentlevel = indentlevel - 1

  def enterLoop(self):
    self.ctx.incNestingLevel()

  def exitLoop(self):
    self.ctx.decNestingLevel()

  def inLoop(self):
    return self.ctx.getNestingLevel() > 0
  
  def dispatchbuiltin(self, builtin, args):
    s, t, w = self._dispatchbuiltin[builtin](args)
    return s, 'object', w

  def _dispatchif(self, node, itype, iwhere):
    if itype:
      s, t, w = self._dispatch[node[0]](node, itype, iwhere)
    else:
      s, t, w = self._dispatch[node[0]](node)
    return s, t, w

  def dispatch(self, node, srcType=None, srcWhere=None):
    "Dispatch the compile of a node."
    # srcType and srcWhere are used to pass along the right hand of an expression chain for use in an assignment.
    if not node:
      return '', 'void', None

    # Catch constants that can use the intenger constant pool
    if node[0] == 'const' and type(node[1]) == types.IntType:
      return '', 'object', constantPool.getConstant('int', node[1])
    
    s, t, w = self._dispatchif(node, srcType, srcWhere)

    if t == 'int':
      s2, w2 = self.int2object(w)
      s = s + s2
      return s, 'object', w2
    return s, t, w

  def int2object(self, wint):
    ### hack in case we didn't get a result
    if not wint:
      wint = '<<< ERROR: no result >>>'

    wo = self.ctx.gettemp()
    s = self.indent() + '%s = PyInt_FromLong(%s);\n' % (wo, wint) + \
        self.ctx.donewith(wint) + self.check(wo)
    return s, wo

  def dispatchvoid(self, node, itype=None, iwhere=None):
    "Dispatch the compile of a node, expecting no return values."
    if not node:
      return ''
    s, t, w = self._dispatchif(node, itype, iwhere)
    return s + self.ctx.release(w)

  def dispatchint(self, node, itype=None, iwhere=None):
    "Dispatch the compile of a node, expecting an object or an int"
    if not node:
      return '', 'void', None
    s, t, w = self._dispatchif(node, itype, iwhere)
    ### Void should not be accepted here and should be tossed later.
    if t != 'int' and t != 'object' and t != 'void':
      raise ValueError, "Dispatchint dispatch returned nonint/nonobject."+str((s,t,w))
    return s, t, w

  def check(self, varname):
    s = self.indent() + 'if ( %s == NULL )\n' % varname
    s = s + self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    return s

  def checkint(self, varname):
    s = self.indent() + 'if ( %s == -1 )\n' % varname
    s = s + self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    return s

  def lookup(self, name):
    return self.ctx.ns.lookup(name)

  def ownref(self, where):
    "Make sure we own a reference for this object."
    if where[:5] == 'temp_':
      # we always own the reference in a temp variable
      return ''

    # oops. it is a global or a local. the variable owns the ref.
    return self.indent() + 'Py_INCREF(%s);\n' % where

  def defaultexprs(self, definfo, defaults):
    fi = '' # function init code
    dn = [ ]        # default init nodes

    for i in range(len(definfo)):
      parsefmt, w = definfo[i]

      defname = 'def_%s_%d' % (self.ctx.ns.getNestedName(), i)
      self.globals[defname] = defname

      # this node will initialize the variable that holds the default
      dn.append('assign', [('ass_name', defname, transformer.OP_ASSIGN)], defaults[i])

      if type(w) == type([]):
        # don't incref the values... after arg processing, all args will
        # have their obs incref'd. defaults always get stored into an
        # argument, by definition, so the defaults will be incref'd
        fi = fi + self.tuple_unpack(w, defname, 0, parsefmt, 0)
      else:
        fi = fi + self.indent() + '%s = %s;\n' % (w, defname)

    return fi, ('stmt', dn)
        
  def list_unpack(self, wheres, src, goerror=1):
    'Returns string to unpack non recursive list into result locations.'
    s = ''
    for i in range(len(wheres)):
      s = s + self.indent() + '%s = PyList_GET_ITEM(%s, %d);\n' % (wheres[i], src, i)
    return s

  def tuple_unpack(self, wheres, src, goerror=1, parsefmt=None, incref=1):
    'Returns string to unpack tuple into locals.'

    if len(wheres) == 0:
      return ''

    if parsefmt == None:
      parsefmt = 'O' * len(wheres)
    s = self.indent() + 'if ( !PyArg_ParseTuple(%s, "%s", &%s) )\n' % \
            (src, parsefmt, string.joinfields(wheres, ', &'))

    # get the right kind of error handling
    if goerror:
      s = s + self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    else:
      s = s + self.indent(1) + 'return NULL;\n'

    # get our own ref to the values in the tuple
    if incref:
      for w in wheres:
        # no need to incref a temp var... the caller will the source around
        # long enough that the temp will remain valid. also, it kind of
        # screws up the ref counting :-)
        if w[:5] != 'temp_':
          s = s + self.indent() + 'Py_INCREF(%s);\n' % w

    return s

  def args_unpack(self, numargs, numdefs, wheres, parsefmt, vawhere, kwwhere):
    'Returns string to unpack tuple into locals.'
    # fast-path for def foo(*args, **kw)
    if numargs == 0:
      if vawhere:
        #s = self.ctx.ns.assign(vawhere, 'object', 'args')
        s = self.indent() + 'Py_INCREF(args);\n' + self.indent() + '%s = args;\n' % vawhere
      else:
        s = ''
      if kwwhere:
        s = s + self.indent() + '%s = %s_copydict(kw);\n' % (kwwhere, self.cmodule)
      return s

    src = 'args'
    t = ''

    wn = self.ctx.getint()
    s = self.check(src)
    s = s + self.indent() + '%s = ((PyTupleObject *)(%s))->ob_size;\n' % (wn, src)

    if vawhere:
      # GetSlice into temp/vararg value
      t = self.ctx.gettemp()

      # note that len(numargs) >= len(src) ... some args may be optional
      # this is okay... the slice pins the args properly
      ### we need to add code to check and clean these properly if the
      ### kwarg func errors
      s = s + self.indent() + '%s = PyTuple_GetSlice(%s, 0, %s);\n' % (t, src, numargs)
      s = s + self.indent() + '%s = PyTuple_GetSlice(%s, %s, %s);\n' % (vawhere, src, numargs, wn)
      src = t

    # The following code calls the keyword/arg unpacking routine.
    if kwwhere is None:
      kww = 'NULL'
    else:
      kww = '&' + kwwhere
    s = s + \
            self.indent() + 'if ( !%s_kwarg(%s, "|%s", kw, %s, %s, %s, %s_argnames, ' % \
            (self.cmodule, src, parsefmt, kww, wn, numargs - numdefs, self.ctx.ns.getNestedName())
    s2 = self.ctx.release(t)

    s = s + '&' + string.joinfields(wheres, ', &') + \
            ') )\n' + \
            self.indent() + '{\n' + \
            self.indent(1) + '%s\n' % s2
    if vawhere:
      s = s + self.indent(1) + 'Py_DECREF(%s);\n' % vawhere
    s = s + self.indent(1) + 'return NULL;\n' + \
        self.indent() + '}\n' + s2
    self.ctx.donewith(wn)

    # all local variables should own their own reference
    s = s + string.joinfields(map(lambda w, self=self: self.indent() + 'Py_INCREF(%s);\n' % w, wheres), '')

    return s

  def _createargs(self, numargs, args, defaults):
    startdef = numargs - len(defaults)
    definfo = [ None ] * len(defaults)
    parsefmt = ''
    wheres = [ ]
    for i in range(numargs):
      arg = args[i]
      if type(arg) != type(()):
        w = self.ctx.ns.nameof(arg)
        wheres.append(w)
        fmt = 'O'
      else:
        fmt, w, x = self._createargs(len(arg), arg, [])
        fmt = '(%s)' % fmt
        wheres = wheres + w

      if i >= startdef:
        definfo[i - startdef] = (fmt, w)

      parsefmt = parsefmt + fmt

    return parsefmt, wheres, definfo

  def func_args(self, args, defaults, flags, emitDefaults=1):
    kw = flags & transformer.CO_VARKEYWORDS
    va = flags & transformer.CO_VARARGS
    if kw and va:
      numargs = len(args) - 2
    elif kw == va == 0:
      numargs = len(args)
    else:
      numargs = len(args) - 1

    s = ''
    dn = None

    # Create parse string and flattened arglist for args_unpack
    parsefmt, wheres, definfo = self._createargs(numargs, args, defaults)

    if len(defaults) > 0 and emitDefaults:
      # get the func initializer code string and default initializer node
      fi, dn = self.defaultexprs(definfo, defaults)

      # Tack onto list of defaults to stick into the module.
      #self.defaults.append(dn)

      # Initialize args with default values before unpacking args.
      s = s + fi

    vawhere = kwwhere = None
    if kw:
      kwwhere = self.ctx.ns.nameof(args[-1])
      if va:
        vawhere = self.ctx.ns.nameof(args[-2])
    elif va:
      vawhere = self.ctx.ns.nameof(args[-1])

    if numargs > 0 or vawhere or kwwhere:
      s = s + self.args_unpack(numargs, len(defaults), wheres, parsefmt, vawhere, kwwhere)

    return s, dn, numargs

  def binary(self, funcname, node, extra=''):
    ### clean this sucker up... we don't care about release order now
    if len(node[1]) == 2:
      # where the result goes. could be either... acquire up front for
      # proper release ordering
      wo = self.ctx.gettemp()
      wi = self.ctx.getint()

      # we may need objects for the left and right nodes. alloc some.
      wl2 = self.ctx.gettemp()
      wr2 = self.ctx.gettemp()

      if len(node) == 3:
        left = node[1]
        right = node[2]
      else:
        left = node[1][0]
        right = node[1][1]
      sl, tl, wl = self.dispatchint(left)
      sr, tr, wr = self.dispatchint(right)
      if tl == tr == 'int' and extra == '' and _func_cop.has_key(funcname):
        s = sl + sr + \
                self.indent() + '%s = %s %s %s;\n' % (wi, wl, _func_cop[funcname], wr) + \
                self.ctx.donewith(wr) + self.ctx.donewith(wl)
        self.ctx.neverused(wr2, wl2, wo)
        return s, 'int', wi

      # get the order right so we release wr/wl properly
      if tr == 'int':
        # release result of dispatchint()
        # Use integer constant pool if possible
        if right[0] == 'const':
          self.ctx.neverused(wr2)
          wr2 = constantPool.getConstant('int', right[1])
          self.ctx.donewith(wr)
        else:
          sr = sr + self.indent() + '%s = PyInt_FromLong(%s);\n' % (wr2, wr) + \
               self.ctx.donewith(wr) + self.check(wr2)
        wr = wr2
        wr2 = None
      if tl == 'int':
        # release result of dispatchint()
        #Use integer constant pool if possible
        if left[0] == 'const':
          self.ctx.neverused(wl2)
          wl2 = constantPool.getConstant('int', left[1])
          self.ctx.donewith(wl)
        else:
          sl = sl + self.indent() + '%s = PyInt_FromLong(%s);\n' % (wl2, wl) + \
               self.ctx.donewith(wl) + self.check(wl2)
        wl = wl2
        wl2 = None

      s = sl + sr
      if _func_cop.has_key(funcname):
        s = s + self.indent() + 'if (PyInt_Check(%s) && PyInt_Check(%s))\n' % (wl, wr)
        s = s + self.indent() + '{\n'
        s = s + self.indent(1) + '/* INLINE: int %s int */\n' % (_func_cop[funcname])
        s = s + self.indent(1) + 'register long a, b, i;\n'
        s = s + self.indent(1) + 'a = ((PyIntObject*) %s)->ob_ival;\n' % wl
        s = s + self.indent(1) + 'b = ((PyIntObject*) %s)->ob_ival;\n' % wr
        s = s + self.indent(1) + 'i = a %s b;\n' % (_func_cop[funcname])
        s = s + self.indent(1) + 'if ((i^a) < 0 && (i^b) < 0)\n'
        s = s + self.indent(1) + '{\n'
        s = s + self.indent(2) + 'PyErr_SetString(PyExc_OverflowError, "integer overflow");\n'
        s = s + self.indent(2) + '%s = NULL;\n' % wo
        s = s + self.indent(1) + '}\n'
        s = s + self.indent(1) + 'else\n'
        s = s + self.indent(2) + '%s = PyInt_FromLong(i);\n' % wo
        s = s + self.indent() + '}\n'
        s = s + self.indent() + 'else\n'
        s = s + self.indent(1)
      else:
        s = s + self.indent()
        
      s = s + '%s = %s(%s, %s%s);\n' % (wo, funcname, wl, wr, extra)

      # get the deallocation ordering right!

      if wr2:
        # release result of dispatchint()
        s = s + self.ctx.release(wr)
      if wl2:
        # release result of dispatchint()
        s = s + self.ctx.release(wl)

      if wr2:
        # we never used the temp var we allocated
        self.ctx.neverused(wr2)
      else:
        # the temp var was moved to wr
        s = s + self.ctx.release(wr)
      if wl2:
        # we never used the temp var we allocated
        self.ctx.neverused(wl2)
      else:
        # the temp var was moved to wl
        s = s + self.ctx.release(wl)

      s = s + self.check(wo)

      # we never used this integer result var
      self.ctx.neverused(wi)

      return s, 'object', wo

    ### This should really use dispatchint() below
    ### but is left as an excersice for later.

    # where the result goes
    w = self.ctx.gettemp()

    # need a secondary result holder
    w2 = self.ctx.gettemp()

    # where is the current value? where does the next one go?
    if len(node[1]) & 1:
      # odd: first result goes in w
      wcur = w
      wnext = w2
    else:
      # even: first result goes in w2
      wcur = w2
      wnext = w

    # get the first operand and move it into a temp
    sl, tl, wl = self.dispatch(node[1][0])
    s = sl + self.check(wl) + \
            self.indent() + 'Py_INCREF(%s);\n' % wl + \
            self.indent() + '%s = %s;\n' % (wcur, wl) + \
            self.ctx.release(wl)

    # iterate over the rest
    for operand in node[1][1:]:
      sr, tr, wr = self.dispatch(operand)

      # apply the operator
      s = s + sr + \
              self.indent()+ 'Py_XDECREF(%s);\n' % wnext + \
              self.indent() + '%s = %s(%s, %s);\n' % (wnext, funcname, wcur, wr) + \
              self.ctx.release(wr) + self.check(wnext)

      # flip the current and next
      wcur, wnext = wnext, wcur

    # based on our initial placement, we know the answer is in "w"
    # we're done with whatever is in "w2" (we know something is there)
    s = s + self.ctx.release(w2)

    return s, 'object', w

  def logical_binary(self, node):
    # where the result goes
    wo = self.ctx.gettemp()

    if node[0]=='or':
      c = ''
      i = 1
    elif node[0]=='and':
      c = '!'
      i = 0
    s = self.indent() + '/* logical_binary begin */\n'
    s = s + self.indent() + 'do {\n'
    
    self.incIndent()
    # s = s + self.indent() + '%s = 1;\n' % wo
    # iterate over the operands
    for operand in node[1]:
      sr, tr, wr = self.dispatchint(operand)
      wi2 = self.ctx.getint()
      s = s + sr
      s = s + self.indent() + 'Py_XDECREF(%s); %s = NULL;\n' % (wo,wo)
      if tr == 'int':
        s = s + self.indent() + '%s = PyInt_FromLong(%s);\n' % (wo, wr)
      else:
        s = s + self.indent() + 'Py_INCREF(%s);\n' % wr
        s = s + self.indent() + '%s = %s;\n' % (wo, wr)
      if tr == 'object':
        s = s + self.indent() + '%s = %sPyObject_IsTrue(%s);\n' % (wi2, c, wr)
        s = s + self.ctx.release(wr)
        s = s + self.indent() + 'if (%s)\n' % wi2
      elif tr == 'int':
        self.ctx.neverused(wi2)
        s = s + self.indent() + 'if (%s%s)\n' % (c, wr)
      s = s + self.indent() + "{\n"
      if tr == 'int':
        s = s + self.ctx.release(wr)
      s = s + self.indent(1) + 'break;\n'
      s = s + self.indent() + "}\n"
      if tr != 'int':
        s = s + self.ctx.donewith(wi2)

    self.decIndent()
    s = s + self.indent() + '} while(0);\n'
    s = s + self.indent() + '/* logical_binary end */\n'
    return s, 'object', wo

  def unary(self, funcname, node):
    s2, t2, w2 = self.dispatchint(node[1])
    if t2 == 'int':
      if _func_cop.has_key(funcname):
        wi = self.ctx.getint()
        s = s2 + self.indent() + '%s = %s%s;\n' % (wi, _func_cop[funcname], w2)
        self.ctx.donewith(w2)
        return s, t2, wi
      s3, w2 = self.int2object(w2)
      s2 = s2 + s3

    wo = self.ctx.gettemp()
    s = s2 + \
            self.indent() + '%s = %s(%s);\n' % (wo, funcname, w2) + \
            self.ctx.release(w2) + self.check(wo)
    return s, 'object', wo

  def assign_unpack(self, node, itype, iwhere, unpacker):
    # node[1] is list of nodes to dispatch to find where's.

    # List of where to unpack the tuple to
    wheres = [ ]
    # List of donewith's that need to be executed after we finish
    # The for loop below
    releases = [ ]

    # Outer layer of tuple/list unpacking
    s = ''
    # Inner layer of tuple/list unpacking
    # Contains code to move the unpacked values into their ultimate destination
    s2 = ''
    for n in node[1]:
      if n[0] == 'ass_name':
        # nameof can fail if we need to look up in a dictionary to get the destination
        try:
          w = self.ctx.ns.nameof(n[1])
        except error:
          w = None
        # If we don't need to look it up in a dictionary, free the old value
        if w:
          wheres.append(w)
          s = s + self.indent() + 'Py_XDECREF(%s);\n' % w
        else:
          # If we do need to look it up in a dictionary
          # Create the destination to unpack into
          w = self.ctx.gettemp()
          wheres.append(w)
          # We can't call donewith(w) here, otherwise it could get
          # reused where it shouldn't
          releases.append(w)
          # Tack the assignment code onto the end of s2.
          s2 = s2 + \
                   self.ctx.ns.assign(n[1], 'object', w, takeref=1) 
      else:
        # If this isn't an ass_name, then we do the same thing.
        # Create the destination to unpack into
        w = self.ctx.gettemp()
        wheres.append(w)
        # Tack where we're going to assign this guy to onto the end of s2
        s2 = s2 + self.dispatchvoid(n, 'object', w) + self.ctx.release(w)

    s = s + unpacker(wheres, iwhere) + s2
    for w in releases:
      s = s + self.ctx.donewith(w)

    return s, 'void', None

  def createtuple(self, items):
    w = self.ctx.gettemp()
    s = self.indent() + '%s = PyTuple_New(%d);\n' % (w, len(items)) + self.check(w)

    for i in range(len(items)):
      s2, t2, w2 = self.dispatch(items[i])

      ### temp hack ... a value should have been returned
      if not w2:
        w2 = '<<< BAD VALUE >>>'

      # make sure we own the ref, then pass the ref to the tuple, then
      # note that we are done with the variable
      s = s + s2 + \
              self.ownref(w2) + \
              self.indent() + 'PyTuple_SET_ITEM(%s, %d, %s);\n' % (w, i, w2) + \
              self.ctx.donewith(w2)

    return s, 'object', w

  def createargskw(self, list):
    wa = self.ctx.gettemp()
    wkw = self.ctx.gettemp()
    hasKeyword = 0
    hasArg = 0
    numargs = 0

    for i in range(len(list)):
      if list[i][0] != 'keyword':
        hasArg = 1
        numargs = numargs + 1
        
    s = self.indent() + '%s = PyTuple_New(%d);\n' % (wa, numargs) + self.check(wa)
    skw = self.indent() + '%s = PyDict_New();\n' % (wkw,) + self.check(wkw)

    for i in range(len(list)):
      s2, t2, w2 = self.dispatch(list[i])

      ### temp hack ... a value should have been returned
      if not w2:
        w2 = '<<< BAD VALUE >>>'
      if list[i][0] != 'keyword':
        # make sure we own the ref, then pass the ref to the tuple, then
        # note that we are done with the variable
        s = s + s2 + \
                self.ownref(w2) + \
                self.indent() + 'PyTuple_SET_ITEM(%s, %d, %s);\n' % (wa, i, w2) + \
                self.ctx.donewith(w2)
      else:
        hasKeyword = 1
        wi = self.ctx.getint()
        wKwArg = constantPool.getConstant('string', list[i][1])
        skw = skw + s2 + \
                self.indent() + '%s = PyDict_SetItem(%s, %s, %s);\n' % (wi, wkw, wKwArg, w2) + \
                self.ctx.release(w2) + self.checkint(wi) + self.ctx.donewith(wi)
    if not hasKeyword:
      self.ctx.neverused(wkw)
      wkw = 'NULL'
    elif not hasArg:
      self.ctx.neverused(wa)
      wa = 'NULL'
      s = skw
    else:
      s = s + skw
    return s, wa, wkw

  def basicfunc(self, name, argnames, defaults, flags, doc, code, isLambda=0):
    "Generate basic function/lambda code."

    if self.ctx.ns.prior is None and isLambda == 0:
      # this is a function at the global level... expose it
      self.methods['%s_%s' % (self.cmodule, name)] = { \
        "flags": flags, 
        "argnames": argnames \
        }

    self.ctx = FunctionContext(self.cmodule, name, self.globals,
                                                       prior=self.ctx)
    if self.ctx.ns.canUseGlobalDefaultVar():
      emitDefaults = 1
    else:
      emitDefaults = 0
    args, defaultexprs, numargs = self.func_args(argnames, defaults, flags, emitDefaults)

    # Put us in the context of whomever is defining us to handle default arguments
    currentCtx = self.ctx
    self.ctx = currentCtx.prior
    defaultSetup = self.dispatchvoid(defaultexprs)
    # Put the new function context back in place
    self.ctx = currentCtx

    # Generate the code for the body of the function
    s = self.dispatchvoid(code)

    # before the func returns, clean up locals
    s = s + self.ctx.cleanup()

    # construct the function definition
    s = _func_defn % {
      'nestedname' : self.ctx.ns.getNestedName(),
      'decls' : self.ctx.decls(),
      'args' : args,
      'body' : s,
      'err' : self.ctx.errorhandler() }
    
    if doc is not None:
      s = 'static char %s_doc[] = "%s";\n\n%s' % \
          (self.ctx.ns.getNestedName(), _cstr(doc), s)
    else:
      s = 'static char %s_doc[] = "";\n\n%s' % \
          (self.ctx.ns.getNestedName(), s)
    
    # Spit out the argument names for this function.
    if numargs:
      paramNames = []
      for i in range(numargs):
        if type(args[i]) == type(''):
          paramNames.append('&%s' % constantPool.getConstant('string', argnames[i]))
        else:
          paramNames.append('NULL')
      s = self.indent() + 'static const PyObject **%s_argnames[] = {\n' % self.ctx.ns.getNestedName() + \
          self.indent() + '       %s\n' % string.joinfields(paramNames, ', ') + \
          self.indent() + '};\n\n' + s
        
    # "write out" the function
    self.funcs.append(s)

    # Put the old context back where it belongs
    self.ctx = self.ctx.prior

    # Handle creating a function object if necessary
    if (emitDefaults == 0 and not isLambda) or self.ctx.ns.isClass:
      # We must assign the function object iff we're in a class, or its not a lambda
      if not emitDefaults:
        s, t, w = self.make_func(name, numargs, flags, defaults, self.ctx.ns.isClass)
      else:
        s, t, w = self.make_func(name, numargs, flags, [], self.ctx.ns.isClass)
      
      s = defaultSetup + s + self.ctx.ns.assign(name, t, w, takeref=1) + \
          self.ctx.donewith(w)

      # we have code, but it still a statement... no return value
      return s
    
    if isLambda:
      # If we have a lambda we must always create a function object, but not assign it to anything.
      if not emitDefaults:
        s, t, w = self.make_func(name, numargs, flags, defaults, isLambda=1)
      else:
        # But don't bother re-emiting the defaults :)
        s, t, w = self.make_func(name, numargs, flags, [], isLambda=1)
      s = defaultSetup + s
      return s, t, w

    # Otherwise just return the code to initialize the default expression
    return defaultSetup

  def make_func(self, name, numargs, flags, defaults, isClass=0, isLambda=0):
    "Make a function object for the given C function and defaults."

    if len(defaults) == 0 and (isClass or isLambda):
       # If we don't have any defaults that require a PyFunction object, and we're in a class or lambda, we don't have to use a PyFunction,
       # we can use an unbound method object instead
       # In theory, this should give us slightly better performance since we don't have to go into eval_code2()
       wcf = self.ctx.gettemp()
       s = self.indent() + '%s = PyCFunction_New(&PyMethDef_%s_%s, NULL);\n' % \
           (wcf, self.ctx.ns.getNestedName(), name)
       s = s + self.check(wcf)
       self.methoddefs[self.ctx.ns.getNestedName() + "_" + name] = None
       if isClass:
         wf = self.ctx.gettemp()
         s = s + self.indent() + '%s = PyMethod_New(%s, NULL, %s);\n' % \
             (wf, wcf, self.ctx.ns.clsobj)
         s = s + self.check(wf) + self.ctx.release(wcf)
         return s, 'object', wf
       return s, 'object', wcf

    wc = self.ctx.gettemp()
    s = self.indent() + '%s = %s_newcode(&PyMethDef_%s_%s, %s, %s, %s_%s_argnames);\n' % \
            (wc, self.cmodule, self.ctx.ns.getNestedName(), name, numargs,
             flags,
             self.ctx.ns.getNestedName(),
             name) + \
            self.check(wc)
    self.methoddefs[self.ctx.ns.getNestedName() + "_" + name] = None

    # newcode depends on lambda helpers being generated, so up the lambda count by 1
    self.lambda_count = self.lambda_count + 1

    # build a function object now
    wf = self.ctx.gettemp()
    s = s + \
            self.indent() + '%s = PyFunction_New(%s, %s_Globals);\n' % \
            (wf, wc, self.cmodule) + \
            self.ctx.release(wc) + \
            self.check(wf)

    # if there are defaults, then place them into the function
    ### pre-build func obs if no defaults are present
    if defaults:
      sd, td, wd = self.createtuple(defaults)
      s = s + sd + \
          self.indent() + 'if ( PyFunction_SetDefaults(%s, %s) == -1 )\n' % (wf, wd) + \
          self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel() + \
          self.ctx.release(wd)

    return s, 'object', wf

  def n_module(self, node):
    def init(self):
      # initialize everything for the compilation...
      self.funcs = [ ]
      self.methods = { }      # list of exposed methods
      self.globals = { }
      self.defaults = [ ] # list of nodes to init default expressions
      self.methoddefs = { } # dict of non-global PyMethodDef's to create
      self.ctx = FunctionContext(self.cmodule, self.cmodule, self.globals)
      self.lambda_count = 0

      # what helpers do we need?
      self.need_print = 0
      self.need_slicer = 0
      self.need_compare = 0
      self.need_subscript = 0
      self.need_raise = 0
      self.need_exec  = 0
      self.need_import = 0

    init(self)
    self.globalfunctions = { }
    ### Lame first pass to gather gloabl function names
    # should be a 'stmt' node
    gcode = self.dispatchvoid(node[2])

    self.globalfunctions = self.methods
    # Reset life for the 2nd pass here
    init(self)

    ### Lame 2nd pass to generate the real code
    gcode = self.dispatchvoid(node[2])
    
    # before the func returns, clean up locals
    gcode = gcode + self.ctx.cleanup()

    doc = node[1]
    if not doc:
      doc = ''

    t = time.ctime(time.time())

    self.cfile.write(_cmod_header % {
      'time': t,
      'src' : self.input,
      'cmod' : self.cmodule,
      'doc' :_cstr(doc),
      })
    self.pyfile.write(_pymod_header % (t, self.input, `doc`, self.cmodule))

    # write out all the globals
    for g in self.globals.values():
      self.cfile.write('static PyObject * %s = NULL;\n' % g)

    # forward declare the constant pool
    self.cfile.write(constantPool.getDeclarations())
    # forward declare the object constant pool
    self.cfile.write(objectConstantPool.getDeclarations())
    
    # write out the helper functions as needed
    if self.need_print:
      self.cfile.write(_print_func % { 'cmod' : self.cmodule })
    if self.need_slicer:
      self.cfile.write(_slicer_func % { 'cmod' : self.cmodule })
    if self.need_compare:
      self.cfile.write(_compare_funcs % { 'cmod' : self.cmodule })
    if self.need_subscript:
      self.cfile.write(_subscript_helpers % { 'cmod' : self.cmodule })
    if self.lambda_count:
      self.cfile.write(_lambda_helpers % { 'cmod' : self.cmodule })
      initlambda = '        %s_lambda_init();\n' % self.cmodule
    else:
      initlambda = ''
    if self.need_raise:
      self.cfile.write(_raise_func % { 'cmod' : self.cmodule })
    if self.need_exec:
      self.cfile.write(_exec_func  % { 'cmod' : self.cmodule })
    if self.need_import:
      self.cfile.write(_import_func % { 'cmod' : self.cmodule })
    self.cfile.write(_copydict_func % { 'cmod' : self.cmodule })
    self.cfile.write(_kwarg_func % { 'cmod' : self.cmodule })

    # forward declare all of the methoddefs
    for name in self.methoddefs.keys():
      self.cfile.write('\nPyMethodDef PyMethDef_%(name)s;\n' % {
          'name' : name
          })

    # forward declare all of the global functions
    for name in self.methods.keys():
      self.cfile.write('static PyObject * %s(PyObject *, PyObject *, PyObject *);\n' % name)
    
    # write out all the functions
    for f in self.funcs:
      self.cfile.write('\n' + f + '\n')
          
    # write out the other code
    methods = ''
    for name in self.methods.keys():
      # use flags==3 meaning we take keywords, too
       methods = methods + \
                 '{ "%s", %s, METH_VARARGS|METH_KEYWORDS, %s_doc },\n' % (name[len(self.cmodule) + 1:], name, name)

    methoddefs = ''
    for name in self.methoddefs.keys():
      methoddefs = methoddefs + _methoddef_format % {
          'name' : name
          }

    defs = ''
    for defnode in self.defaults:
      defs = defs + self.dispatchvoid(defnode)

    self.cfile.write(_cmod_trailer % {
      'mod' : self.cmodule,
      'gcode' : gcode,
      'gdecls' : self.ctx.decls(),
      'gerr' : self.ctx.errorhandler(),
      'methods' : methods,
      'methoddefs' : methoddefs,
      'defaults' : defs,
      'constants' : constantPool.getCode(),
      'objconstants' : objectConstantPool.getCode(),
      'initlambda' : initlambda,
      })

    # this result "shouldn't" be used by anybody
    return '<<< ERROR: module >>>', 'void', None

  def insertNodeComment(self, node):
    # The special casing is to reduce useless duplication of printing nodes
    ### Add tryfinally, tryexcept
    comment = self.indent() + '/*\n'
    if node[0] == 'classdef' or node[0] == 'function' or node[0] == 'lambda':
      comment = comment + self.indentCommentBlock(pprint.pformat( node[:-2] ))
    elif node[0] == 'for' or node[0] == 'while':
      comment = comment + self.indentCommentBlock(pprint.pformat( node[:-3] ))
    elif node[0] == 'tryfinally' or node[0] == 'tryexcept' or node[0] == 'if':
      # Skip emitting a complete comment here
      comment = comment + self.indentCommentBlock(pprint.pformat( node[0] ))
    else:
      if type(node) is not type( (None, None)) and type(node) is not type( [] ):
        comment = comment + self.indentCommentBlock(pprint.pformat( node.asList() ))
      else:
        comment = comment + self.indentCommentBlock(pprint.pformat( node ))
                                                 
    comment = comment + self.indent() + ' */\n'
    return comment

  def n_stmt(self, node):
    body = ''
    for stmt in node[1]:
      comment = self.insertNodeComment(stmt)
      body = body + comment
      s = self.dispatchvoid(stmt)
      body = body + s
    return body, 'void', None

  def n_function(self, node):

   defaults = node[3]

   s = self.basicfunc(node[1], node[2], defaults, node[4], node[5], node[6])
   return s, 'void', None

  def n_lambda(self, node):
    self.lambda_count = self.lambda_count + 1

    name = 'lambda_%d' % self.lambda_count

    return self.basicfunc(name, node[1], node[2], node[3], None, ('return', node[4]), isLambda=1)

  def n_classdef(self, node):
    # a temp to hold the class's dictionary
    clsdict = self.ctx.gettemp()

    s = self.indent() + '%s = PyDict_New();\n' % clsdict + \
            self.check(clsdict)

    # compile the base classes
    sb, tb, wb = self.createtuple(node[2])
    s = s + sb

    # hold the class object somewhere while we create it and get it
    # placed into the target namespace
    clsobj = self.ctx.gettemp()
    clsName = constantPool.getConstant('string', node[1])
    s = s + self.indent() + '%s = PyClass_New(%s, %s, %s);\n' % (clsobj, wb, clsdict, clsName) + \
        self.check(clsobj) + self.ctx.release(wb)

    if node[3]:
      doc = self.ctx.gettemp()
      s = s + self.indent() + '%s = PyString_FromString("%s");\n' % (doc, _cstr(node[3])) + \
              self.check(doc) + \
              self.indent() + 'if ( PyMapping_SetItemString(%s, "__doc__", %s) == -1 )\n' % (clsdict, doc) + \
              self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel() + \
              self.ctx.release(doc)

    # push a new Namespaces for the class
    self.ctx.ns = Namespaces(self.ctx, node[1], clsdict, self.ctx.ns, clsobj, isClass=1)

    s = s + self.dispatchvoid(node[4])

    self.ctx.ns = self.ctx.ns.prior

    # release, the class dictionary and assign the classobject into the surrounding namespace
    s = s + self.ctx.release(clsdict) + \
            self.ctx.ns.assign(node[1], 'object', clsobj, takeref=1) + \
            self.ctx.donewith(clsobj)

    return s, 'void', None

  def n_pass(self, node):
    return self.indent() + '/* pass */ ;\n', 'void', None

  def n_break(self, node):
    assert self.inLoop(), "break found outside of loop"
    if self.ctx.inFinallyBlock():
      return self.indent() + 'finally_code = FC_BREAK;\n' + self.indent() + 'goto %s;\n' % self.ctx.toptryfinallylabel(), 'void', None
    return self.indent() + 'break;', 'void', None

  def n_continue(self, node):
    assert self.inLoop(), "continue found outside of a loop"
    if self.ctx.inFinallyBlock():
      return self.indent() + 'finally_code = FC_CONTINUE;\n' + self.indent() + 'goto %s;\n' % self.ctx.toptryfinallylabel(), 'void', None
    return self.indent() + 'continue;', 'void', None

  def canOptimizeRange(self, node):
    "Returns true if the range call is optimizable in a for loop"
    # node = ('call_func', ('name', 'range'), [('const', int), ... ])
    if node[0] != 'call_func':
      return 0
    if node[1][0] != 'name':
      return 0
    if node[1][1] != 'range' and node[1][1] != 'xrange':
      return 0
    if len(node[2]) > 3:
      return 0
    for n in node[2]:
      if n[0] != 'const':
        return 0
      if type(n[1]) != types.IntType:
        return 0
    if not self.ctx.ns.isPotentialSpecialBuiltin(node[1][1]):
      return 0
    return 1
      
  def n_for(self, node):
    s = ''
    optimized = 0
    wo = self.ctx.gettemp()
    wi = self.ctx.getint()
    # If we can optimize it, go for it.
    if self.canOptimizeRange(node[2]):
      #print "Optimized for"
      # node = ('call_func', ('name', 'range'), [('const', int), ... ])
      optimized = 1
      wFunction = self.ctx.gettemp()
      # Fallback if someone overrode us in the global scope.
      wName = constantPool.getConstant('string', node[2][1][1])
      s = s + self.indentCommentBlock(_builtin_header % (wFunction, self.ctx.cmodule, self.ctx.cmodule, wName), prefix='')
      self.incIndent()
      constNodes = node[2][2]
      iStart = 0
      iStep  = 1
      if len(constNodes) > 1:
        iStart = constNodes[0][1]
        # range(1,4) == [1,4) i.e. [1,2,3]
        iFinish = constNodes[1][1]
        if len(constNodes) == 3:
          iStep = constNodes[2][1]
      else:
        # range(1,4) == [1,4) i.e. [1,2,3]
        iFinish = constNodes[0][1]

      s = s + self.indent() + 'for( %s = %d; %s < %d; %s += %d)\n' % (wi, iStart, wi, iFinish, wi, iStep)
      s = s + self.indent() + '{\n'
      self.incIndent()
      s = s + self.indent() +  'Py_XDECREF(%s);\n' % wo
      s = s + self.indent() +  '%s = PyInt_FromLong(%s);\n' % (wo, wi) + self.check(wo)
      # do the assignment
      ### This creates needless increments/decrements for simple local variable assignment
      sa, ta, wa = self.dispatch(node[1], 'object', wo)
      s = s + sa
      # enter the loop.
      self.enterLoop()
      # run the code
      s = s +  self.dispatchvoid(node[3])
      # exit the loop.
      self.exitLoop()
      self.decIndent()
      s = s + self.indent() + '}\n'
      # handle the else
      if node[4]:
        s = s + self.indent() + 'if (%s == %d)\n' % (wi, iFinish)
        s = s + self.indent() + '{\n'
        self.incIndent()
        s = s + dispatchvoid(node[4])
        self.decIndent()
        s = s + self.indent() + '}\n'
      # free up resources
      s = s + self.ctx.release(wo) + self.ctx.release(wi)
      wo = self.ctx.gettemp()
      wi = self.ctx.getint()
      self.decIndent()
      s = s + self.indent() + '}\n'
      s = s + self.indent() + 'else\n'
      s = s + self.indent() + '{\n'
      self.incIndent()
      # Setup sequence object for fallback loop
      wl = self.ctx.gettemp()
      s2, wa, wkw = self.createargskw(constNodes)
      s = s + self.indent() + '%s = PyEval_CallObjectWithKeywords(%s, %s, %s);\n' % (wl, wFunction, wa, wkw)
      s = s + self.check(wl) + self.ctx.release(wFunction) + self.ctx.release(wa) + self.ctx.release(wkw)

    if not optimized:
      sl, tl, wl = self.dispatch(node[2])
      s = s + sl
    
    ### note: we could sometimes skip the assignment of -1
    ### If there isn't an else block
    s = s + \
        self.indent() + 'if ( %s->ob_type->tp_as_sequence == NULL )\n' % wl + \
        self.indent() + '{\n' + \
        self.indent(1) +   'PyErr_SetString(PyExc_TypeError, "loop over non-sequence");\n' + \
        self.indent(1) +   'goto %s;\n' % self.ctx.toperrorlabel() + \
        self.indent() +  '}\n' + \
        self.indent() +  'for ( %s = 0; ; ++%s )\n' % (wi, wi) + \
        self.indent() +  '{\n' + \
        self.indent(1) + '%s = (*%s->ob_type->tp_as_sequence->sq_item)(%s, %s);\n' % (wo, wl, wl, wi) + \
        self.indent(1) + 'if ( %s == NULL )\n' % wo + \
        self.indent(1) + '{\n' + \
        self.indent(2) +   'if ( PyErr_Occurred() != PyExc_IndexError )\n' + \
        self.indent(3) +      'goto %s;\n' % self.ctx.toperrorlabel() + \
        self.indent(2) +   'PyErr_Clear();\n' + \
        self.indent(2) +   '%s = -1;\n' % wi + \
        self.indent(2) +   'break;\n' + \
        self.indent(1) + '}\n' #% (wl, self.ctx.toperrorlabel(), wi, wi, wo, wl, wl, wi, wo, self.ctx.toperrorlabel(), wi)
    
    self.incIndent()
    # do the assignment
    ### This may create needless increments/decrements for local variable cases.
    sa, ta, wa = self.dispatch(node[1], 'object', wo)
    s = s + sa + self.ctx.release(wo)

    # enter the loop.
    self.enterLoop()
    
    # run the code
    s = s + self.dispatchvoid(node[3])

    # exit the loop.
    self.exitLoop()
    
    self.decIndent()
    # close up the loop and do the "else" code
    s = s + self.indent() + '}\n'
    if node[4]:
      s = s + self.indent() + \
              'if ( %s == -1 )\n' % wi + self.indent() + \
              '{\n'
      self.incIndent()
      s = s + self.dispatchvoid(node[4])
      self.decIndent()
      s = s + self.indent() + \
              '}\n'

    # done with the list and iterator variables
    s = s + self.ctx.release(wl) + self.ctx.donewith(wi)

    # if we optimized close the brace
    if optimized:
      self.decIndent()
      s = s + self.indent() +'}\n'
    s = s + '\n' + self.indent() + '/* end of for loop */\n'


    return s, 'void', None

  def n_while(self, node):
    we = self.ctx.getint()  # flag if while exitted normally
    s = self.indent() + '%s = 0;\n' % we
    s = s + self.indent() + 'while ( 1 )\n' + self.indent() + '{\n'

    self.incIndent()
    # compile the "test"
    s2, t2, w2 = self.dispatchint(node[1])
    self.decIndent()
    
    if t2 == 'int':
      s = s + s2 + self.indent(1) + '%s = !%s;\n' % (we, w2) + \
            self.indent(1) + 'if ( %s )\n' % we + \
            self.indent(2) + 'break;\n'
      self.ctx.donewith(w2)
    else:
      s = s + s2 + \
            self.indent(1) + '%s = !PyObject_IsTrue(%s);\n' % (we, w2) + \
            self.indent() + self.ctx.release(w2) + \
            self.indent(1) + 'if ( %s )\n' % we + \
            self.indent(2) + 'break;\n'

    # Enter the loop
    self.enterLoop()
    self.incIndent()

    # compile the "body"
    s = s + self.dispatchvoid(node[2])

    # Exit the loop
    self.exitLoop()
    self.decIndent()
    
    s = s  + self.indent() + '}\n'
    # compile the "else"
    if node[3]:
      s = s + \
              self.indent() + 'if ( %s )\n' % we + \
              self.indent() + '{\n'
      self.incIndent()
      s = s + self.dispatchvoid(node[3])
      self.decIndent()
      
      s = s + self.indent() + '}\n'

    # make sure the temp var is NULL'd out
    s = s + self.ctx.donewith(we)

    return s, 'void', None

  def n_if(self, node):
    s = ''
    insert_else = 0
    braces = 0
    for test, suite in node[1]:
      if insert_else:
        self.decIndent()
        s = s + self.indent() + '}\n' + \
            self.indent() + 'else\n' + \
            self.indent() + '{\n'
        braces = braces + 1
        self.incIndent()
      s2, t2, w2 = self.dispatchint(test)
      if t2 == 'int':
        s = s + s2 + \
          self.indent() + 'if ( %s )\n' % w2 + \
          self.indent() + '{\n'
        self.incIndent()
        s = s + self.ctx.donewith(w2)
      else:
        s = s + s2 + \
          self.indent() + 'if ( PyObject_IsTrue(%s) )\n' % w2 + \
          self.indent() + '{\n'
        self.incIndent()
        s = s + self.ctx.release(w2)
      s = s + self.dispatchvoid(suite)
      insert_else = 1
    if node[2]:
      if insert_else:
        self.decIndent()
        s = s + self.indent() + '}\n' + \
            self.indent() + 'else\n' + \
            self.indent() + '{\n'
        self.incIndent()
      s = s + self.dispatchvoid(node[2])
    for i in range(braces+1):
      self.decIndent()
      s = s + self.indent() + '}\n'
    return s, 'void', None

  def n_exec(self, node):
    # exec:         code, globals, locals
    self.need_exec = 1
    s = '<<< ERROR: exec  ---BEGIN--- >>>\n'
    s2, t2, w2 = self.dispatch(node[1])
    if node[2] is None:
      wGlobal = '%s_Globals' % self.cmodule
      s3 = ''
    else:
      s3, t3, wGlobal = self.dispatch(node[2])
    # Scream and yell if they didn't specify a locals dictionary.
    if node[3] is None:
      raise error, "exec: You must specify a locals argument to exec for Python 2 C."
    else:
      s4, t4, wLocal  = self.dispatch(node[3])
    s = s + s2 + s3 + s4
    wInt = self.ctx.getint()
    s = s + '        %s = %s_do_exec(%s, %s, %s);\n' % (wInt, self.cmodule, w2, wGlobal, wLocal)
    s = s + self.checkint(wInt)
    s = s + self.ctx.donewith(wInt)
    s = s + self.ctx.release(w2)
    s = s + self.ctx.release(wGlobal)
    s = s + self.ctx.release(wLocal)
    return s + '<<< ERROR: exec      ---END--- >>>\n', 'void', None

  def n_assert(self, node):
    s = '/* <<< assert ---BEGIN--- >>> */\n'
    #Assert generates:
    #          if __debug__:
    #                if not <test>:
    #                  raise AssertionError [, <message>]
    #
    #       where <message> is the second test, if present.
    # Expansion pulled from Python-1.5.1
    ### Expansion must rebuilt using new Node class
    n = ('if',
             [(('name', '__debug__'),
               ('stmt',
               [('if',
               [(('not', node[1]),
                     ('stmt',
                      [('raise',
                            ('name', 'AssertionError'),
                            node[2],
                            ('name', 'None'))]))],
                     None)]))],
             None)
    s2, t2, w2 = self.dispatch(n)
    s = s + s2
    return s + '/* <<< assert ---END--- >>> */\n', 'void', None

  def n_from(self, node):
    self.need_import = 1
    s = ""
    # If we're not in the global namespace
    # Complain loudly that we don't support this
    if not self.ctx.ns.isRoot() and node[2][0] == '*':
      raise error, "Python2C: from module import * is only supported in the global namespace"
    # Grab the module similarly to n_import
    wModule = self.ctx.gettemp()
    s2, t, wModuleName = self.n_const(('const', node[1]))
    s = s + s2
    s = s + self.indent() + '%s = PyImport_Import(%s);\n' % (wModule, wModuleName)
    s = s + self.ctx.release(wModuleName)
    # Find the module we need to import symbols from
    # Handle dotted module names here.
    mods = string.split(node[1], '.')
    for i in range(1, len(mods)-1):
      wNewModule = self.ctx.gettemp()
      s = s + self.indent() + '%s = PyObject_GetAttrString(%s, "%s");\n' % (wNewModule, wModule, node[2])
      s = s + self.ctx.release(wModule) + self.check(wNewModule)
      wModule = wNewModule

    wInt = self.ctx.getint()
    for obj in node[2]:
      if obj == '*':
        s2, t, wName = self.n_const(('const', obj))
        s = s + s2
        s = s + self.indent() + '%s = %s_import_from(%s_Globals, %s, %s);\n' % (wInt, self.cmodule, self.cmodule, wModule, wName)
        s = s + self.checkint(wInt) + self.ctx.donewith(wInt)
        s = s + self.ctx.release(wName)
      else:
        w3 = self.ctx.gettemp()
        s = s + self.indent() + '%s = PyObject_GetAttrString(%s, "%s");\n' % (w3, wModule, obj)
        s = s + self.check(w3)
        s2 = self.dispatchvoid(('ass_name', obj, 'OP_ASSIGN'), 'object', w3)
        s = s + s2 + self.ctx.release(w3)
    s = s + self.ctx.release(wModule)
    return s, 'void', None

  def n_import(self, node):
    self.need_import = 1
    s = ""
    for module in node[1]:
      name = string.split(module, ".")[0]
      s2, t, wModuleName = self.n_const(('const', module))
      s = s + s2
      wModule = self.ctx.gettemp()
      s = s + self.indent() + '%s = Py2C_Import(%s);\n' % (wModule, wModuleName)
      s = s + self.check(wModule)
      s2, t, w3 = self.n_ass_name( ('ass_name', name, 'OP_ASSIGN'), 'object', wModule)
      s = s + s2 + self.ctx.release(wModuleName) + self.ctx.release(wModule)
    return s, 'void', None

  def n_raise(self, node):
    s = ''
    self.need_raise = 1
    s2, t2, w1 = self.dispatch(node[1])
    s = s + s2 
    s2, t2, w2 = self.dispatch(node[2])
    s = s + s2 
    s2, t2, w3 = self.dispatch(node[3])
    s = s + s2
    s = s + self.indent() + "%s_do_raise(%s, %s, %s);\n" % (self.cmodule, w1, w2, w3)
    s = s + self.ctx.release(w1) + self.ctx.release(w2) + self.ctx.release(w3)
    s = s + self.indent() + "goto %s;\n" % self.ctx.toperrorlabel()
    return s, 'void', None

  def n_tryfinally(self, node):
    el1 = self.ctx.geterrorlabel()
    self.ctx.pusherrorlabel(el1, 'TRYFINALLY')
    s = self.dispatchvoid(node[1])
    self.ctx.poperrorlabel()
    s = s + self.indent()[:-2] + "%s: ;\n" % el1
    wExceptionType = self.ctx.gettemp()
    wExceptionValue = self.ctx.gettemp()
    wExceptionTraceback = self.ctx.gettemp()
    # Grab the current exposed Python exception
    s = s + self.indent() + "%s_ExposePyException(NULL, NULL, NULL, &%s, &%s, &%s);\n" % \
        (self.cmodule, wExceptionType, wExceptionValue, wExceptionTraceback)
    # execute code in the try block.
    s2 = self.dispatchvoid(node[2])
    s = s + s2
    # Reset the currently exposed Python exception.
    s = s + self.indent() + "%s_ResetPyException(%s, %s, %s);\n" % \
        (self.cmodule, wExceptionType, wExceptionValue, wExceptionTraceback)
    s = s + self.indent() + "%s = NULL;\n" % wExceptionType
    s = s + self.indent() + "%s = NULL;\n" % wExceptionValue
    s = s + self.indent() + "%s = NULL;\n" % wExceptionTraceback
    self.ctx.donewith(wExceptionType)
    self.ctx.donewith(wExceptionValue)
    self.ctx.donewith(wExceptionTraceback)
    s = s + self.indent() + "if (finally_code == FC_RETURN)\n"
    s = s + self.indent() + "{\n"
    self.incIndent()
    if self.ctx.inFinallyBlock():
      s = s + self.indent() + "goto %s;\n" % self.ctx.toptryfinallylabel()
    else:
      # clean up any locals and temps that are in use
      # we can't use cleanup here because we're in a finally block and the live information is incorrect
      s = s + self.ctx.errorhandler(hideLabel=1)
      s = s + self.indent() + "return result;\n"
    self.decIndent()
    s = s + self.indent() + "}\n"
    # only need to check for these guys if I'm in a loop.
    if self.inLoop():
      s = s + self.indent() + "if (finally_code == FC_BREAK)\n"
      s = s + self.indent() + "{\n"
      if self.ctx.inFinallyBlock():
        s = s + self.indent(1) + "goto %s;\n" % self.ctx.toptryfinallylabel()
      else:
        s = s + self.indent(1) + "finally_code = FC_NORMAL;\n"
        s = s + self.indent(1) + "break;\n"
      s = s + self.indent() + "}\n"
      s = s + self.indent() + "if (finally_code == FC_CONTINUE)\n"
      s = s + self.indent() + "{\n"
      if self.ctx.inFinallyBlock():
        s = s + self.indent(1) + "goto %s;\n" % self.ctx.toptryfinallylabel()
      else:
        s = s + self.indent(1) + "finally_code = FC_NORMAL;\n"
        s = s + self.indent(1) + "continue;\n"
      s = s + self.indent() + "}\n"
    s = s + self.indent() + "if (PyErr_Occurred())\n"
    s = s + self.indent(1) + "goto %s;\n" % self.ctx.toperrorlabel()
    return s, 'void', None

  def n_tryexcept(self, node):
    el1 = self.ctx.geterrorlabel()
    el2 = self.ctx.geterrorlabel()
    el3 = self.ctx.geterrorlabel()
    self.ctx.pusherrorlabel(el1, 'TRYEXCEPT')
    s2, t2, w2 = self.dispatch(node[1])
    self.ctx.poperrorlabel()
    s = s2 + self.indent() + "goto %s;\n" % el2
    s = s + self.indent()  + "%s: ;\n" % el1
    # Some kind of exception occured.
    # Save any existing exposed exception while we temporarily overwrite it.
    # because we may be inside someone elses except block.
    wet = self.ctx.gettemp()
    wev = self.ctx.gettemp()
    wetb = self.ctx.gettemp()
    wfet = self.ctx.gettemp()
    wfev = self.ctx.gettemp()
    wfetb = self.ctx.gettemp()
    fHasCleanup = 0
    s = s + self.indent() + "PyErr_Fetch(&%s, &%s, &%s);\n" % \
        (wet, wev, wetb)
    s = s + self.indent() + \
        "%s_ExposePyException(%s, %s, %s, &%s, &%s, &%s);\n" % \
        (self.cmodule, wet, wev, wetb, wfet, wfev, wfetb)
    s = s + self.ctx.donewith(wet, wev, wetb)
    j = len(node[2]) - 1
    i = 0
    #b is the # of braces we gotta close up after the loop.
    b = 0
    for test, result, suite in node[2]:
      #Expression to compare possible exception against
      if test:
        s2, t2, w2 = self.dispatch(test)
        s = s + s2
        t3 = self.ctx.gettemp()
        ires = self.ctx.getint()
        s = s + self.indent() + "%s = PyThreadState_Get()->exc_type;\n" % t3

        s = s + self.indent() + '%s = PyErr_GivenExceptionMatches(%s, %s);\n' % (ires, t3, w2)
        s = s + self.ctx.donewith(t3) + self.ctx.release(w2)
        s = s + self.indent() + "if ( %s )\n" % ires
        s = s + self.indent() + "{\n"
        self.incIndent()
        # Assign expression into result
        s2 = self.dispatchvoid(result, 'object', w2)
        s = s + s2 + self.ctx.donewith(ires)
      # Code to execute if the Exception comarison returns true.
      s = s + \
          self.indent() + '/*\n' + \
          self.indentCommentBlock('except') + \
          self.indent() + ' */\n'
      s2 = self.dispatchvoid(suite)
      s = s + s2
      # Restore any pre-existing exposed exception before our try block started.
      s = s + self.indent() + "%s_ResetPyException(%s, %s, %s);\n" % \
          (self.cmodule, wfet, wfev, wfetb)
      s = s + self.indent() + "%s = NULL;\n" % wfet
      s = s + self.indent() + "%s = NULL;\n" % wfev
      s = s + self.indent() + "%s = NULL;\n" % wfetb
      s = s + self.indent() + "goto %s;\n" % el3
      if test:
        self.decIndent()
        s = s + self.indent() + "}\n"
        if j>i :
          s = s + self.indent() + "else\n" + self.indent() + "{\n"
          self.incIndent()
          b = b + 1
      i = i + 1
    # close up the braces.
    for i in range(b):
      self.decIndent()
      s = s + self.indent() + "}\n"
    # Else node, aka code to execute if there wasn't an exception.
    s = s + self.indent() + "%s: ;\n" % el2
    # Restore any pre-existing exposed exception before our try block started.
    s = s + self.indent() + '%s_ResetPyException(%s, %s, %s);\n' % (self.cmodule, wfet, wfev, wfetb)
    s = s + self.ctx.donewith(wfet, wfev, wfetb)
    s = s + self.dispatchvoid(node[3])
    s = s + self.indent()[:-2] + "%s: ;\n" % el3
    return s, 'void', None

  def n_return(self, node):
    s, t, w = self.dispatch(node[1])

    # If we don't get a result something is wrong.
    if not w:
      raise error, "Internal Error: missing where on n_return's valueNode"

    # If we're inside a tryfinally block, the last finally block calls cleanup before returning the result
    if self.ctx.inFinallyBlock():
      s = s + self.indent() + 'finally_code = FC_RETURN;\n'
      s = s + self.indent() + 'result = %s;\n' % w
      # Save our return result from disappearing during cleanup
      s = s + self.indent() + 'Py_INCREF(result);\n'
      s = s + self.indent() + 'goto %s;\n' % self.ctx.toptryfinallylabel()
    else:
      # clean up any locals and temps that are in use (except for the retval!)
      # This may clean up values we think are live. This may include exception state temporaries
      # created by n_tryfinally
      s = s + self.ctx.cleanup(w)
      s = s + self.indent() + 'return %s;\n' % w
    self.ctx.donewith(w)

    return s, 'void', None

  def strspn(self, s):
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
    map = [0] * 31
    for c in charset:
      map[ord(c) >> 3] = map[ord(c) >> 3] | (1 << (ord(c) & 7))
    count = 0
    for c in s:
      if map[ord(c) >> 3] & (1 << (ord(c) & 7)):
        count = count + 1
      else:
        break
    return count
    
  def n_const(self, node):
    k = node[1]

    if type(k) == types.IntType:
      w = self.ctx.getint()
      return self.indent() + '%s = %s;\n' % (w, k), 'int', w
    if k is None:
      return self.indent() + 'Py_INCREF(Py_None);\n', 'object', 'Py_None'

    w = self.ctx.gettemp()
    if type(k) == types.LongType:
      s = 'PyLong_FromString("%s")' % k
    elif type(k) == types.StringType:
      self.ctx.neverused(w)
      s = ''
      w = constantPool.getConstant('string', k)
      return s, 'object', w
    elif type(k) == types.ComplexType:
      s = 'PyComplex_FromDoubles(%s, %s)' % (str(k.real), str(k.imag))
    elif k == []:
      s = 'PyList_New(0)'
    elif k == ():
      s = 'PyTuple_New(0)'
    elif k == {}:
      s = 'PyDict_New()'
    elif type(k) == types.FloatType:
      s = 'PyFloat_FromDouble(%g)' % k
    else:
      s = '<<< ERROR UNKNOWN CONSTANT TYPE: %s >>>' % str(k)
      ### how to log an error?

    s = self.indent() + '%s = %s;\n' % (w, s) + self.check(w)
    return s, 'object', w

  def n_print(self, node):
    self.need_print = 1
    s = ''
    for expr in node[1]:
      s2, t2, w2 = self.dispatch(expr)
      s = s + s2 + \
              self.indent() + 'if ( %s_print_helper(%s) )\n' % (self.cmodule, w2) + \
              self.indent(1) + 'goto error;\n' + \
              self.ctx.release(w2)
    return s, 'void', None

  def n_printnl(self, node):
    s, t, w = self.n_print(node)
    s = s + self.indent() + '%s_print_helper_nl();\n' % self.cmodule
    return s, 'void', None

  def n_discard(self, node):
    if node[1][0] == 'const':
      # Don't evaluate constant's that aren't going anywhere.. duh. :)
      return '', 'void', None

    s = self.dispatchvoid(node[1])
    return s, 'void', None

  def n_assign(self, node):
    s, t, w = self.dispatch(node[2])

    ### temp hack ... a value should have been returned
    if not w:
      w = '<<< BAD VALUE >>>'

    # optimize a simple assignment
    if len(node[1]) == 1 and node[1][0][0] == 'ass_name':
      s = s + \
              self.ownref(w) + \
              self.ctx.ns.assign(node[1][0][1], 'object', w, takeref=1) + \
              self.ctx.donewith(w)
      return s, 'void', None

    for ass in node[1]:
      # can be ass_name, ass_tuple, ass_list, ass_attr, subscript, slice
      s = s + self.dispatchvoid(ass, t, w)

    s = s + self.ctx.release(w)
    return s, 'void', None

  def n_ass_tuple(self, node, itype=None, iwhere=None):
    return self.assign_unpack(node, itype, iwhere, self.tuple_unpack)

  def n_ass_list(self, node, itype=None, iwhere=None):
    return self.assign_unpack(node, itype, iwhere, self.list_unpack)

  def n_ass_name(self, node, itype=None, iwhere=None):
    s = ""
    if node[2] == transformer.OP_ASSIGN:
      ### Should this have takeref=1??? 
      s = self.ctx.ns.assign(node[1], itype, iwhere)
    elif node[2] == transformer.OP_DELETE:
      # This would remove a local, or a global
      # If a local, raise an exception
      if self.ctx.ns.isLocal(node[1]):
        raise error, "Python2C: can't delete local variable: %s" % node[1]
      # If a declared global, delete it
      if self.ctx.ns.isDeclaredGlobal(node[1]):
        s = s + \
                self.indent() + 'if ( %s_assign_subscript(%s_Globals, "%s", NULL) == -1 )\n' % (self.cmodule, self.cmodule, node[1]) + \
                self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
      # Otherwise we don't know where it is.
      # Throw an exception, to complain about it.
      else:
        raise error, "Python2C: can't find variable to delete: %s" % node[1]
    else:
      raise error, "Unknown ass_name flag: %s" % node[2]
    return s, 'void', None

  def n_ass_attr(self, node, itype=None, iwhere=None):
    s, t, w = self.dispatch(node[1])
    wAttr = constantPool.getConstant('string', node[2])
    if node[3] == transformer.OP_ASSIGN:
      s = s + \
              self.indent() + 'if ( PyObject_SetAttr(%s, %s, %s) == -1 )\n' % (w, wAttr, iwhere) + \
              self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    elif node[3] == transformer.OP_DELETE:
      s = s + \
              self.indent() + 'if ( PyObject_DelAttr(%s, %s) == -1 )\n' % (w, wAttr) + \
              self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    else:
      s = s + self.indent() + '<<< ERROR: unknown flags: %s >>>\n' % node[3]

    s = s + self.ctx.release(w)

    return s, 'void', None

  def n_tuple(self, node):
    return self.createtuple(node[1])

  def n_list(self, node):
    w = self.ctx.gettemp()
    s = self.indent() + '%s = PyList_New(%d);\n' % (w, len(node[1])) + self.check(w)

    for i in range(len(node[1])):
      s2, t2, w2 = self.dispatch(node[1][i])
      # Disgusting hack to avoid a function call
      # We can do this because we just created a new & EMPTY list.
      ### Change to PyList_SET_ITEM later
      s = s + s2 + \
              self.indent() + 'Py_INCREF(%s);\n' % w2 + \
              self.indent() + 'PyList_GET_ITEM(%s, %d) = %s;\n' % (w, i, w2) + \
              self.ctx.release(w2)

    return s, 'object', w

  def n_dict(self, node):
    w = self.ctx.gettemp()
    s = self.indent() + '%s = PyDict_New();\n' % (w,) + self.check(w)

    for key, value in node[1]:
      sk, tk, wk = self.dispatch(key)
      sv, tv, wv = self.dispatch(value)
      s = s + sk + sv + \
              self.indent() + 'PyDict_SetItem(%s, %s, %s);\n' % (w, wk, wv) + \
              self.ctx.release(wv) + self.ctx.release(wk)

    return s, 'object', w

  def n_or(self, node):
    return self.logical_binary(node)

  def n_and(self, node):
    return self.logical_binary(node)

  def n_not(self, node):
    s, t, w = self.dispatchint(node[1])
    if t == 'int':
      s = s + self.indent() + '%s = !%s;\n' % (w, w)
    else:
      w2 = self.ctx.getint()
      s = s + self.indent() + '%s = !PyObject_IsTrue(%s);\n' % (w2, w) + \
              self.ctx.release(w)
      w = w2
    return s, 'int', w

  def n_compare(self, node):
    # Logic comes from cmp_outcome() in ceval.c
    # compare:      exprNode, [ (op, node), ..., (op, node) ]

    # figure out where the result is going to go
    ires = self.ctx.getint()

    s = self.indent() + 'do\n'
    s = s + self.indent() + '{\n'
    
    self.incIndent()
    s2, t2, wl = self.dispatch(node[1])
    
    s = s + s2 + self.indent() + '%s = 1;\n' % ires

    for i in range(len(node[2])):
      s2, t2, wr = self.dispatch(node[2][i][1])
      op = node[2][i][0]
      s = s + s2
      if op == 'is':
        s = s + self.indent() + '%s = (%s == %s);\n' % (ires, wl, wr)
        s = s + self.ctx.release(wl)
      elif op == 'isnot':
        s = s + self.indent() + '%s = (%s != %s);\n' % (ires, wl, wr)
        s = s + self.ctx.release(wl)
      elif op == 'in' or op == 'notin':
        self.need_compare = 1
        s = s + self.indent() + '%s = %s_cmp_member(%s, %s);\n' % (ires, self.cmodule, wl, wr)
        s = s + self.ctx.release(wl)
      elif op == 'EXC_MATCH':
        s = s + self.indent() + '%s = PyErr_GivenExceptionMatches(%s, %s);\n' % (ires, wl, wr)
        s = s + self.ctx.release(wl)
      else:
        s = s + self.indent() + 'if (PyInt_Check(%s) && PyInt_Check(%s))\n' % (wl, wr)
        s = s + self.indent() + '{\n'
        s = s + self.indent(1) + '/* INLINE: cmp(int, int) */\n'
        s = s + self.indent(1) + 'register long a, b;\n'
	s = s + self.indent(1) + 'a = ((PyIntObject*) %s)->ob_ival;\n' % wl
	s = s + self.indent(1) + 'b = ((PyIntObject*) %s)->ob_ival;\n' % wr
	s = s + self.indent(1) + '%s = a %s b;\n' % (ires, op)
        s = s + self.indent()  + '}\n'
        s = s + self.indent()  + 'else\n'
        s = s + self.indent()  + '{\n'
        s = s + self.indent(1) + '%s = PyObject_Compare(%s, %s);\n' % (ires, wl, wr)
        s = s + self.indent(1) + '%s = %s %s 0;\n' % (ires, ires, op)
        s = s + self.indent()  + '}\n'
        s = s + self.ctx.release(wl)

      if i < len(node[2])-1:
        s = s + self.indent() + 'if (!%s)\n' % ires
        s = s + self.indent(1) + 'break;\n' 
        wl = wr
      else:
        s = s + self.ctx.release(wr)

    self.decIndent()
    s = s + self.indent() + '} while (0);\n\n'
    return s, 'int', ires

  def n_bitor(self, node):
    return self.binary('PyNumber_Or', node)

  def n_bitxor(self, node):
    return self.binary('PyNumber_Xor', node)

  def n_bitand(self, node):
    return self.binary('PyNumber_And', node)

  def n_name(self, node):
    # special case this one
    if node[1] == 'None':
      return '', 'object', 'Py_None'

    ### need to do builtins in here

    return self.lookup(node[1])

  def n_globals(self, node):
    for n in node[1]:
      self.ctx.ns.makeglobal[n] = None

    return self.indent() + '/* globals processed: %s */\n' % node[1], 'void', None

  def n_lshift(self, node):
    return self.binary('PyNumber_Lshift', node)

  def n_rshift(self, node):
    return self.binary('PyNumber_Rshift', node)

  def n_plus(self, node):
    return self.binary('PyNumber_Add', node)

  def n_minus(self, node):
    return self.binary('PyNumber_Subtract', node)

  def n_star(self, node):
    return self.binary('PyNumber_Multiply', node)

  def n_slash(self, node):
    return self.binary('PyNumber_Divide', node)

  def n_percent(self, node):
    return self.binary('PyNumber_Remainder', node)

  def n_uplus(self, node):
    return self.unary('PyNumber_Positive', node)

  def n_uminus(self, node):
    return self.unary('PyNumber_Negative', node)

  def n_invert(self, node):
    return self.unary('PyNumber_Invert', node)

  def n_power(self, node):
    return self.binary('PyNumber_Power', node, ', Py_None')

  def n_backquote(self, node):
    return self.unary('PyObject_Repr', node)

  def n_getattr(self, node):
    w = self.ctx.gettemp()
    s2, t2, w2 = self.dispatch(node[1])
    wAttr = constantPool.getConstant('string', node[2])
    s = s2 + self.indent() + 'if (PyInstance_Check(%s))\n' % w2
    s = s + self.indent() + '{\n'
    s = s + self.indent(1) + 'if (%s->ob_type->tp_getattro != NULL)\n' % w2
    s = s + self.indent(2) + '%s = (*%s->ob_type->tp_getattro)(%s, %s);\n' % (w, w2, w2, wAttr)
    s = s + self.indent() + '}\n'
    s = s + self.indent() + 'else\n'
    s = s + self.indent() + '{\n'
    s = s + self.indent(1) + '%s = PyObject_GetAttr(%s, %s);\n' % (w, w2, wAttr)
    s = s + self.indent() + '}\n'
    s = s + self.ctx.release(w2) + self.check(w)
    return s, 'object', w

  def n_call(self, node):
    # call_func:    node, [ arg1, ..., argN ]

    ### we may want to optimize for no keyword args

    # process the function object to call
    ### This needs to catch the case, where we can call the function
    ### locally via C
    ### Currently the mechanics of local/global lookup work around this failing.

    # Catch special case builtins:
    if node[1][0] == 'name' and self.ctx.ns.isPotentialSpecialBuiltin(node[1][1]):
      builtin = node[1][1]
      # Disallow globals(), locals(), and vars() without an argument.
      if builtin == "globals":
        raise error, "Python2C: you're not allowed to call globals() in Python2C translated code."
      elif builtin == "locals":
        raise error, "Python2C: you're not allowed to call locals() in Python2C translated code."
      elif builtin == "vars" and len(node[2]) == 0:
        raise error, "Python2C: you're not allowed to call vars() without an argument in Python2C translated code."
      # Specially optimize other builtin nodes
      elif builtin in _optimized_builtins.keys():
        # print "optimized builtin: ", builtin
        return self.dispatchbuiltin(builtin, node[2])

    # get a temp var for the result
    wr = self.ctx.gettemp()

    # create a tuple and keywords for the arguments
    s, wa, wkw = self.createargskw(node[2])

    if node[1][0] == 'name' and not self.ctx.ns.isLocal(node[1][1]) and not self.ctx.ns.isKnownGlobal(node[1][1]) and "%s_%s" % (self.cmodule, node[1][1]) in self.globalfunctions.keys():
      w2 = '%s_%s' % (self.cmodule, node[1][1])
      s = s + self.indent() + '%s = %s(NULL, %s, %s);\n' % (wr, w2, wa, wkw)
    else:
      s2, t2, w2 = self.dispatch(node[1])
      s = s + s2 + \
          self.indent() + '%s = PyEval_CallObjectWithKeywords(%s, %s, %s);\n' % (wr, w2, wa, wkw)
      s = s + self.ctx.release(w2)
      
    s = s +  \
        self.ctx.release(wa) + self.ctx.release(wkw) + self.check(wr)

    return s, 'object', wr

  def n_keyword(self, node):
    s = ''
    s2, t2, w2 = self.dispatch(node[2])
    s = s + s2
    return s, 'object', w2

  def n_subscript(self, node, itype=None, iwhere=None):
    self.need_subscript = 1
    if len(node[3]) > 1:
      s3, t3, w3 = self.createtuple(node[3])
    else:
      s3, t3, w3 = self.dispatch(node[3][0])
    s2, t2, w2 = self.dispatch(node[1])
    s = s3 + s2

    wo = None
    t4 = 'void'

    if node[2] == transformer.OP_APPLY:
      wo = self.ctx.gettemp()
      t4 = 'object'
      s = s + self.indent() + "%s = PyObject_GetItem(%s, %s);\n" % \
                               (wo, w2, w3)
    elif node[2] == transformer.OP_ASSIGN:
      s = s + \
              self.indent() + 'if ( %s_assign_subscript(%s, %s, %s) == -1 )\n' % (self.cmodule, w2, w3, iwhere) + \
              self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    elif node[2] == transformer.OP_DELETE:
      s = s + \
          self.indent() + 'if ( %s_assign_subscript(%s, %s, NULL) == -1 )\n' % (self.cmodule, w2, w3) + \
          self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    else:
      raise error, "InternalError: Unknown flag passed to n_subscript"

    s = s + self.ctx.release(w2) + self.ctx.release(w3) + self.check(wo)

    return s, t4, wo

  def n_ellipsis(self, node):
    return '', 'void', 'Py_Ellipsis'

  def n_sliceobj(self, node):
    # Get result
    wo = self.ctx.gettemp()
    s = ''
    s3 = '    %s = PySlice_New(' % wo
    wheres = []
    for expr in node[1]:
      s2, t2, w2 = self.dispatch(expr)
      wheres.append(w2)
      s3 = s3 + w2 + ', '
      s = s + s2
    s3 = s3[:-2] + ');\n'
    s = s + s3
    for w in wheres:
      s = s + self.ctx.release(w)
    return s, 'object', wo

  def n_slice(self, node, itype=None, iwhere=None):
    # slice:        exprNode, flags, lowerNode, upperNode
    self.need_slicer = 1

    if node[2] == transformer.OP_APPLY:
      # where the slice will end up
      wr = self.ctx.gettemp()
    else:
      # where the status code goes
      wr = self.ctx.getint()

    s, t, w = self.dispatch(node[1])

    wrlo = self.ctx.getint()
    wrhi = self.ctx.getint()

    ### it would be nice to use dispatchint() here...

    # handle the lower bound
    if node[3]:
      s2, t2, wolo = self.dispatch(node[3])
      s = s + s2
    else:
      wolo = 'NULL'

    # handle the upper bound
    if node[4]:
      s2, t2, wohi = self.dispatch(node[4])
      s = s + s2
    else:
      wohi = 'NULL'

    s = s + self.indent() + 'if ( %s_slicer_helper(%s, %s, %s, &%s, &%s) )\n' % (self.cmodule, w, wolo, wohi, wrlo, wrhi)
    s = s + self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    if wohi != 'NULL':
      s = s + self.ctx.release(wohi)
    if wolo != 'NULL':
      s = s + self.ctx.release(wolo)

    if node[2] == transformer.OP_APPLY:
      s = s + self.indent() + \
              '%s = (*%s->ob_type->tp_as_sequence->sq_slice)(%s, %s, %s);\n' % (wr, w, w, wrlo, wrhi) + \
              self.ctx.release(w) + self.check(wr)

      self.ctx.donewith(wrhi, wrlo)
      return s, 'object', wr

    if node[2] == transformer.OP_DELETE:
      s = s + self.indent() + \
              '%s = (*%s->ob_type->tp_as_sequence->sq_ass_slice)(%s, %s, %s, NULL);\n' % (wr, w, w, wrlo, wrhi) + \
              self.ctx.release(w) + self.checkint(wr)
    elif node[2] == transformer.OP_ASSIGN:
      s = s + self.indent() + \
              '%s = (*%s->ob_type->tp_as_sequence->sq_ass_slice)(%s, %s, %s, %s);\n' % (wr, w, w, wrlo, wrhi, iwhere) + \
              self.ctx.release(w) + self.checkint(wr)

    self.ctx.donewith(wrhi, wrlo, wr)
    return s, 'void', None

  def builtinFallback(self, wr, name, args):
    wFunction = self.ctx.gettemp()
    s2, wa, wkw = self.createargskw(args)
    wName = constantPool.getConstant('string', name)
    s = ''
    s = s + self.indent() + 'if ( ( %s = PyObject_GetItem(PyEval_GetBuiltins(), %s)) == NULL)\n' % (wFunction, wName)
    s = s + self.indent() + '{\n'
    s = s + self.indent(1) + '/* --- BAD LOCAL --- */\n'
    s = s + self.indent(1) + 'goto %s;\n' % self.ctx.toperrorlabel()
    s = s + self.indent() + '}\n'
    # self.decIndent()
    s = s + self.indent() + '}\n'
    s = s + s2
    s = s + self.indent() + '%s = PyEval_CallObjectWithKeywords(%s, %s, %s);\n' % (wr, wFunction, wa, wkw)
    s = s + self.check(wr) + self.ctx.release(wa) + self.ctx.release(wkw) + self.ctx.release(wFunction)
    return s

  def builtinFooter(self, wr, wFunction, args):
    s = ''
    s = s + self.indent() + '}\n'
    s = s + self.indent() + 'else\n'
    s = s + self.indent() + '{\n'
    self.incIndent()
    s2, wa, wkw = self.createargskw(args)
    s = s + s2
    s = s + self.indent() + '%s = PyEval_CallObjectWithKeywords(%s, %s, %s);\n' % (wr, wFunction, wa, wkw)
    s = s + self.check(wr) + self.ctx.release(wa) + self.ctx.release(wkw) + self.ctx.release(wFunction)
    self.decIndent()
    s = s + '}\n'
    return s

  def builtin_type(self, args):
    # from bltinmodule.c:
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    s = _builtin_header % (wFunction, self.ctx.cmodule, self.ctx.cmodule, "type")
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 1:
      self.ctx.neverused(wFunction)
      s2, t, wr = self.builtinFallback(wr, "type", args)
      s = s + s2
      return s, t, wr
    if args[0] == ('const', ()):
      self.ctx.neverused(wr)
      wr = 'PyTuple_Type'
      wa = None
    elif args[0] == ('const', []):
      self.ctx.neverused(wr)
      wr = 'PyList_Type'
      wa = None
    elif args[0] == ('const', {}):
      self.ctx.neverused(wr)
      wr = 'PyDict_Type'
      wa = None
    elif args[0][0] == 'const' and type(args[0][1]) == types.StringType:
      self.ctx.neverused(wr)
      wr = 'PyString_Type'
      wa = None
    elif args[0][0] == 'const' and type(args[0][1]) == types.IntType:
      self.ctx.neverused(wr)
      wr = 'PyInt_Type'
      wa = None
    elif args[0][0] == 'const' and type(args[0][1]) == types.FloatType:
      self.ctx.neverused(wr)
      wr = 'PyFloat_Type'
      wa = None
    if wa is not None:
      s, t, wa = self.dispatch(args[0])
      s = s + self.indent() + "%s = %s->ob_type;\n" % (wr, wa)
    s = s + self.indent() + "Py_INCREF(%s);\n" % (wr)
    if wa is not None:
      s = s + self.ctx.release(wa)
    s = s + self.builtinFooter(wr, wFunction, args)
    return s, 'object', wr

  def builtin_len(self, args):
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    wConst = constantPool.getConstant('string', "len")
    s = _builtin_header % (wFunction, self.ctx.cmodule, self.ctx.cmodule, wConst)
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 1:
      self.ctx.neverused(wFunction)
      s2 = self.builtinFallback(wr, "len", args)
      s = s + s2
      return s, t, wr
    wInt = self.ctx.getint()
    s2, t, w = self.dispatch(args[0])
    s = s + s2
    s = s + self.indent() + "if (PyString_Check(%s) || PyList_Check(%s))" % (w,w)
    s = s + self.indent() + "{\n"
    s = s + self.indent(1) + "%s = ((PyVarObject *)(%s))->ob_size;\n" % (wInt, w)
    s = s + self.indent() + "}\n"
    s = s + self.indent() + "else\n"
    s = s + self.indent() + "{\n"
    self.incIndent()
    s = s + self.indent() + "PyTypeObject *tp = NULL;\n"
    s = s + self.indent() + "tp = %s->ob_type;\n" % w
    s = s + self.indent() + "if (tp->tp_as_sequence != NULL)\n"
    s = s + self.indent() + "{\n"
    s = s + self.indent(1) + "%s = (*tp->tp_as_sequence->sq_length)(%s);\n" % (wInt, w)
    s = s + self.indent() + "}\n"
    s = s + self.indent() + "else if (tp->tp_as_mapping != NULL)\n"
    s = s + self.indent() + "{\n"
    s = s + self.indent(1) + "%s = (*tp->tp_as_mapping->mp_length)(%s);\n" % (wInt, w)
    s = s + self.indent() + "}\n"
    s = s + self.indent() + "else\n"
    s = s + self.indent() + "{\n"
    s = s + self.indent(1) + 'PyErr_SetString(PyExc_TypeError, "len() of unsized object");\n'
    s = s + self.indent(1) + "goto %s;\n" % self.ctx.toperrorlabel()
    s = s + self.indent() + "}\n"
    s = s + self.indent() + "if (%s < 0)\n" % wInt
    s = s + self.indent() + "{\n"
    s = s + self.indent(1) + "goto %s;\n" % self.ctx.toperrorlabel()
    s = s + self.indent() + "}\n"
    self.decIndent()
    s = s + self.indent() + "}\n"
    s = s + self.ctx.release(w)
    ### *Sigh* len() can't return an int because of builtin fallback support
    s = s + self.indent() + "%s = PyInt_FromLong(%s);\n" % (wr, wInt)
    s = s + s2
    s = s + self.builtinFooter(wr, wFunction, args) + self.ctx.donewith(wInt)
    return s, 'object', wr

  def builtin_str(self, args):
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    s = _builtin_header % (wFunction, wFunction, self.ctx.cmodule, "str")
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 1:
      self.ctx.neverused(wFunction)
      s2 = self.builtinFallback(wr, "str", args)
      s = s + s2
      return s, t, wr
    s2, t, wa = self.dispatch(args[0])
    s = s + s2
    s = s + "        %s = PyObject_Str(%s);\n" % (wr, wa)
    s = s + self.check(wr) + self.ctx.release(wa)
    s = s + self.builtinFooter(wr, wFunction, args)
    return s, 'object', wr

  def builtin_repr(self, args):
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    s = _builtin_header % (wFunction, wFunction, self.ctx.cmodule, "repr")
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 1:
      self.ctx.neverused(wFunction)
      s2 = self.builtinFallback(wr, "repr", args)
      s = s + s2
      return s, t, wr
    s2, t, wa = self.dispatch(args[0])
    s = s + s2
    wr = self.ctx.gettemp()
    s = s + "        %s = PyObject_Repr(%s);\n" % (wr, wa)
    s = s + self.check(wr) + self.ctx.release(wa)
    s = s + self.buitinFooter(wr, wFunction, args)
    return s, 'object', wr

  def builtin_cmp(self, args):
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    s = _builtin_header % (wFunction, wFunction, self.ctx.cmodule, "cmp")
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 1:
      self.ctx.neverused(wFunction)
      s2 = self.builtinFallback(wr, "cmp", args)
      s = s + s2
      return s, t, wr
    if len(args) != 2:
      raise error, 'Builtin "cmp()" requires 2 arguments'
    s2, t, w1 = self.dispatch(args[0])
    s3, t, w2 = self.dispatch(args[1])
    s = s + s2 + s3
    s = s + "        %s = PyObject_Compare(%s, %s);\n" % (wr, w1, w2)
    s = s + "        if (PyErr_Occurred())\n"
    s = s + "        {\n"
    s = s + "                goto %s;\n" % self.ctx.toperrorlabel()
    s = s + "        }\n"
    s = s + self.ctx.release(w1) + self.ctx.release(w2)
    s = s + self.builtinFooter(wr, wFunction, args)
    return s, 'object', wr

  def builtin_apply(self, args):
    wFunction = self.ctx.gettemp()
    wr = self.ctx.gettemp()
    s = _builtin_header % (wFunction, wFunction, self.ctx.cmodule, "apply")
    # If the builtin arg count doesn't match, do the normal thing
    if (len(args)) > 3 or len(args) < 2:
      self.ctx.neverused(wFunction)
      s2 = self.builtinFallback(wr, "apply", args)
      s = s + s2
      return s, t, wr
    s2, t, wFunction = self.dispatch(args[0])
    s3, t, wArg = self.dispatch(args[1])
    s = s + s2 + s3
    if len(args) == 3:
      s2, t, wKw = self.dispatch(args[2])
    else:
      s2, wKw = ('', '(PyObject *)NULL')
    s = s + s2
    s = s + "        %s = PyEval_CallObjectWithKeywords(%s, %s, %s);\n" % (wr, wFunction, wArg, wKw)
    s = s + self.check(wr) + self.ctx.release(wFunction) + self.ctx.release(wArg) + self.ctx.release(wKw)
    s = s + self.builtinFooter(wr, wFunction, args)
    return s, 'object', wr

_builtin_header = '''
if ( ( %s = %s_Globals->ob_type->tp_as_mapping->mp_subscript(%s_Globals, %s)) == NULL)
{
    PyErr_Clear();
'''


class Namespaces:
  "Represents a set of local/global namespaces."
  def __init__(self, ctx, name, usedict=None, prior=None, clsobj=None, isClass=0):
    self.ctx = ctx          # what ctx to operate within
    self.usedict = usedict
    self.clsobj = clsobj
    self.prior = prior
    self.name = name
    # True only for classes
    self.isClass = isClass
    self.locals = { }               # Py name to C name
    self.makeglobal = { }   # the keys should be global vars

  def getroot(self):
    "Return the root namespace"
    prior = self.prior
    while prior:
      prior = prior.prior
    if prior is None:
      return self
    return prior

  def isRoot(self):
    if self.prior is None:
      return 1
    return 0

  def getNamespaceDepth(self):
    i = 1
    prior = self.prior
    while prior:
      prior = prior.prior
      i = i + 1
    return i

  def getNestedName(self):
    """Return a name uniquely representing the nesting of namespaces
    The idea being to generate a different C function name for:
      class blah: def __init__(self): pass
      and
      class blah2: def __init__(self): pass
    """
    name = self.name
    prior = self.prior
    while prior:
      name = "%s_%s" % (prior.name, name)
      prior = prior.prior
    return name

  def canUseGlobalDefaultVar(self):
    """Return 1 if the caller can use global defaults for functions
    Return 0 if the caller must create a glue lambda."""

    # If we're in the global namespace, always allow static defaults
    if self.prior is None:
      return 1
    else:
      # If we're the 3rd namespace and the 2nd namespace is a class (the 1st namespace is always the module)
      # allow them to use global defaults
      if self.getNamespaceDepth() == 3 and self.prior.isClass:
        return 1
      # If we're the 2nd namespace, allow them to use global defaults
      elif self.getNamespaceDepth() == 2:
        return 1
    # Otherwise don't
    return 0
  
  def lookupFallback(self, w, name):
    """Lookup a name in globals or builtins
    
        Try and find 'name' in the global or builtin dictionaries.
    """
    sIndent = INDENT * (indentlevel + 1)
    wName = constantPool.getConstant('string', name)
    s = ''
    #wExceptionType = self.ctx.gettemp()
    #wExceptionValue = self.ctx.gettemp()
    #wExceptionTraceback = self.ctx.gettemp()

    ## Preserve exception state across the lookup if it succeeds
    #s = sIndent + 'PyErr_Fetch(&%s, &%s, &%s);\n' % (wExceptionType, wExceptionValue, wExceptionTraceback)
    s = s + sIndent + 'if ( ( %s = %s_Globals->ob_type->tp_as_mapping->mp_subscript(%s_Globals, %s)) == NULL)\n' % (w, self.ctx.cmodule, self.ctx.cmodule, wName)
    s = s + sIndent + '{\n'
    s = s + sIndent + INDENT + 'if ( ( %s = PyObject_GetItem(PyEval_GetBuiltins(), %s)) == NULL)\n' % (w, wName)
    s = s + sIndent + INDENT + '/* --- BAD LOCAL --- */\n'
    s = s + sIndent + INDENT + '{\n'
    # s = s + sIndent + INDENT * 2 + 'Py_XDECREF(%s); Py_XDECREF(%s); Py_XDECREF(%s);\n' % (wExceptionType, wExceptionValue, wExceptionTraceback)
    s = s + sIndent + INDENT * 2 + 'goto %s;\n' % self.ctx.toperrorlabel()
    s = s + sIndent + INDENT + '}\n'
    s = s + sIndent + '}\n'
    #s = s + sIndent + 'PyErr_Restore(%s, %s, %s);\n' % (wExceptionType, wExceptionValue, wExceptionTraceback)
    #s = s + self.ctx.donewith(wExceptionType) + self.ctx.donewith(wExceptionValue) + \
    #    self.ctx.donewith(wExceptionTraceback)
    s = s + sIndent + "if (PyErr_Occurred())\n"
    s = s + sIndent + "    PyErr_Clear();\n"
    return s


  def isPotentialSpecialBuiltin(self, name):
    "Determine if 'name' is a potential builtin that we care about"
    # If 'name' is a declared global or we're using a dictionary we're not a builtin
    if self.makeglobal.has_key(name) or self.usedict:
      return 0
    # If 'name' is a local, fall out.
    if self.locals.has_key(name):
      return 0
    # If 'name' is a C global, fall out.
    if self.ctx.globals.has_key(name):
      return 0
    root = self.getroot()
    # If 'name' doesn't exist in the module namespace, and 'name' is a builtin, we have a match
    if not root.makeglobal.has_key(name) and name in _special_builtins:
      return 1
    # If 'name' is a builtin, we have a match
    if name in _special_builtins:
      return 1
    return 0

  def isLocal(self, name):
    return self.locals.has_key(name)

  def isDeclaredGlobal(self, name):
    if self.isRoot():
      if self.ctx.globals.has_key(name):
        return 1
    return self.makeglobal.has_key(name)

  def isKnownGlobal(self, name):
    if self.isDeclaredGlobal(name):
      return 1
    root = self.getroot()
    return root.isDeclaredGlobal(name)

  def lookup(self, name):
    """Lookup a name for access.

    Three values are returned: a string to place before the value access,
    the type of the result, and where the result is located.
    """

    fDeclaredGlobal = 0
    # check for dictionary-based access. note that globals take precedence
    # over other dictionary vars.
    dict = self.usedict
    if self.makeglobal.has_key(name):
      dict = '%s_Globals' % self.ctx.cmodule
      fDeclaredGlobal = 1
    if dict:
      w = self.ctx.gettemp()
      ### Note: we rely on the mapping to raise KeyError
      ### technically, this would be a NameError in a program
      # If this is a declared global we need to check builtins as well
      # Since: global len; a = [2,3]; len(a) needs to call the builtin version
      if fDeclaredGlobal:
        s = self.lookupFallback(w, name)
      else:
        wName = constantPool.getConstant('string', name)
        s = '    if ( (%s = PyObject_GetItem(%s, %s)) == NULL )\n' \
            '          goto %s;\n' % (w, dict, wName, self.ctx.toperrorlabel())

      return s, 'object', w

    if self.isLocal(name):
      return '', 'object', self.locals[name]
    else:
      ### Check C globals
      if self.ctx.globals.has_key(name):
        return '', 'object', self.ctx.globals[name]

      # Find the root name space, and search for global variable
      root = self.getroot()
      if root.makeglobal.has_key(name):
        w = self.ctx.gettemp()
        # Note: we rely on the mapping to raise KeyError
        ### technically, this would be a NameError in a program
        s = self.lookupFallback(w, name)
        return s, 'object', w
      ### We should check builtins here.
      # If we couldn't find it it's either
      # 1) local function that should be called
      #    Note: local function calls are handled via n_call
      # 2) global variable we haven't seen yet
      # 3) builtin
      ### We may in the future not generate this code for cases 1, 2, and 3 above if a
      ### command line switch is set.
      w = self.ctx.gettemp()
      s = self.lookupFallback(w, name)
      return s, 'object', w

  def nameof(self, name):
    "Return the C name of Python name."

    # check for dictionary-based access. note that globals take precedence
    # over other dictionary vars. if there are no prior namespaces, then
    # we are in the global context, and the variable should go into the
    # global dict
    dict = self.usedict
    if self.makeglobal.has_key(name) or self.prior is None:
      dict = '%s_Globals' % self.ctx.cmodule
    if dict:
      ### for now, raise an exception. this could probably be a temp var and
      ### then the caller needs to assign it to the global and free the
      ### temp. we'll raise an exception to catch this case because we really
      ### don't want to accidentally hit here... it will result in pretty
      ### poor looking code (special checks and whatnot). we'll see if we
      ### can restructure the caller instead.
      raise error, 'nameof: called in a "usedict" namespace'

    w = self.locals[name] = 'l_%s' % name
    return w

  def assign(self, name, valtype, where, takeref=0):
    """Assign a value to the given name.

    The name to assign to should have been allocated beforehand.  The
    value is located by the "where" argument and has a type described
    by the "valtype" argument.

    The code to perform the assignment is returned.
    """

    sIndent = INDENT * (indentlevel + 1)
    
    ### ack... just cuz it is a global doesn't mean all assigns go there!
    if self.ctx.globals.has_key(name):
      var = self.ctx.globals[name]
    else:
      var = None

      # check for dictionary-based access. note that globals take precedence
      # over other dictionary vars. if there are no prior namespaces, then
      # we are in the global context, and the variable should go into the
      # global dict
      dict = self.usedict
      if self.makeglobal.has_key(name) or self.prior is None:
        dict = '%s_Globals' % self.ctx.cmodule
        # Since we don't have a prior scope, all variable destinations are globals
        # Mark it as such.
        if not self.makeglobal.has_key(name):
          self.makeglobal[name] = None
      if dict:
        ws = constantPool.getConstant('string', name)
        s = sIndent + 'if (PyDict_SetItem(%s, %s, %s) == -1)\n' % (dict, ws, where)
        s = s + sIndent + INDENT + 'goto %s;\n' % self.ctx.toperrorlabel()
        
        # if we are supposed to take the reference when assigning, then
        # we need to DECREF, because the SetItem didn't take it
        if takeref:
          s = s + sIndent + 'Py_DECREF(%s);\n' % where
        return s

    if not var:
      # must be a local variable
      var = self.locals[name] = 'l_%s' % name

    # if we aren't supposed to take the reference when assigning, then we
    # should create an extra reference.
    if takeref:
      s = ''
    else:
      s = sIndent + 'Py_INCREF(%s);\n' % where

    return s + \
               sIndent + 'Py_XDECREF(%s);\n' % var + \
               sIndent + '%s = %s;\n' % (var, where)


class FunctionContext:
  def __init__(self, cmodule, name, globals, prior=None):
    self.cmodule = cmodule
    self.name = name
    self.globals = globals  # the module's globals
    self.prior = prior

    self.freetemps = [ ]    # List of free temps
    self.freeints = [ ]             # List of free temps
    self.maxtemp = 0
    self.maxint = 0
    self.nextlabel = 1                      # Number of next label
    self.errorstack = [ ('error' , 'TRYEXCEPT') ] # Stack of error labels
    self.finallystack = [ None ] # Locations of finally blocks
    self.nestingLevel = 0

    prior_ns = None
    if prior:
      prior_ns = self.prior.ns
    self.ns = Namespaces(self, name, None, prior_ns)

  def __str__(self):
    return 'maxtemp: %s,  maxint: %s, freetemps: %s, freeints: %s' % \
               (self.maxtemp, self.maxint, self.freetemps, self.freeints)

  def incNestingLevel(self):
    self.nestingLevel = self.nestingLevel + 1

  def decNestingLevel(self):
    self.nestingLevel = self.nestingLevel - 1
    assert self.nestingLevel >= 0, "Tried to exit non-existant loop!"

  def getNestingLevel(self):
    return self.nestingLevel
    
  def geterrorlabel(self):
    self.nextlabel = self.nextlabel + 1
    return 'label' + str(self.nextlabel - 1)

  def pusherrorlabel(self, label, type):
    if type == 'TRYFINALLY':
      self.finallystack.append(label)
    self.errorstack.append(label,type)

  def poperrorlabel(self):
    l, type = self.errorstack[-1]
    if type == 'TRYFINALLY':
      del self.finallystack[-1]
    del self.errorstack[-1]
    return l, type

  def toperrorlabel(self):
    return self.errorstack[-1][0]

  def toptryfinallylabel(self):
    return self.finallystack[-1]

  def inFinallyBlock(self):
    return (len(self.finallystack) > 1)

  def gettemp(self):
    if len(self.freetemps) > 0:
      s = self.freetemps[-1]
      del self.freetemps[-1]
      return s

    s = 'temp_%s' % self.maxtemp
    self.maxtemp = self.maxtemp + 1
    return s

  def getint(self):
    if len(self.freeints) > 0:
      s = self.freeints[-1]
      del self.freeints[-1]
      return s

    s = 'long_%s' % self.maxint
    self.maxint = self.maxint + 1
    return s

  def release(self, varname):
    "Release the contents of a variable and enable the variable's reuse."
    if not varname:
      return ''
    s = INDENT * (indentlevel + 1) #/* Releasing %s\n%s\n */\n' % (varname, self)
    if varname[:5] == 'temp_':
      if varname not in self.freetemps:
        self.freetemps.append(varname)
        s = s + 'Py_DECREF(%s); %s = NULL;  ' % (varname, varname)
      else:
        s = s + '<<< Tried to free %s twice >>>' % varname
    elif varname[:5] == 'long_':
      if varname not in self.freetemps:
        self.freeints.append(varname)
      else:
        s = s + '<<< Tried to free %s twice>>>' % varname
    # Could be BAD_LOCAL_xxx, %(cmod)s_Globals, local variable, Py_None, or Py_Ellipsis, etc...
    # if s isn't set above
    return s + '/* release called on %s */\n' % varname

  def donewith(self, *varnames):
    "Note that we are done with a variable, so it can be reused."
    s = ''
    for varname in varnames:
      #s = s + '/* Done with %s \n%s\n*/\n' % (varname, self)
      if varname[:5] == 'temp_':
        if varname not in self.freetemps:
          self.freetemps.append(varname)
          s = s + INDENT * (indentlevel + 1) + '%s = NULL; /* Done with %s */\n' % (varname, varname)
        else:
          s = s + '<<< Tried to free %s twice >>>' % varname
      elif varname[:5] == 'long_':
        if varname not in self.freeints:
          self.freeints.append(varname)
          s = s + INDENT * (indentlevel + 1) + '/* Done with %s: freelist length = %d, %s */\n' % (varname, len(self.freeints), self.freeints)
        else:
          s = s + '<<< Tried to free %s twice >>>' % varname

    return s

  def neverused(self, *varnames):
    "Put an unused variable back into the pool."

    # just use this, but ignore the return value
    apply(self.donewith, varnames)
    return ''

  def decls(self):
    "Return declarations for all locals."
    s = ''
    sIndent = INDENT * (indentlevel + 1)
    for l in self.ns.locals.values():
      s = s + sIndent + 'PyObject * %s = NULL;\n' % l
    for i in range(self.maxtemp):
      s = s + sIndent + 'PyObject * temp_%s = NULL;\n' % i
    for i in range(self.maxint):
      s = s + sIndent + 'long long_%s;\n' % i
    return s + '\n'

  def errorhandler(self, hideLabel=0):
    "Return error handler for cleaning up locals."
    if hideLabel:
      s = ''
    else:
      s = 'error:\n'
    sIndent = INDENT * (indentlevel + 1)
    for l in self.ns.locals.values():
      s = s + sIndent + 'Py_XDECREF(%s);\n' % l
    for i in range(self.maxtemp):
      s = s + sIndent + 'Py_XDECREF(temp_%s);\n' % i
    return s

  def cleanup(self, keep=None):
    "Return code for cleaning up outstanding locals."
    s = ''
    sIndent = INDENT * (indentlevel + 1)

    for l in self.ns.locals.values():
      if l != keep:
        s = s + sIndent + 'Py_XDECREF(%s);\n' % l

    # Loop over all possible temps and free them
    for i in range(self.maxtemp):
      tempvar = 'temp_%d' % i
      # If it already hasn't been freed and its not something we care about, free it now
      if not tempvar in self.freetemps and tempvar != keep:
        s = s + sIndent + 'Py_XDECREF(%s); /* Cleaned up live temporary */\n' % tempvar
    # Loop over all possible ints
    for i in range(self.maxint):
      intvar = 'long_%d' % i
      if not intvar in self.freeints and intvar != keep:
        s = s + sIndent + "/* long_%d was live, don't need to cleanup */\n" % i

    return s



def _cstr(s):
  "Convert the string to a usable C source string."
  if not s:
    return ''
  return string.replace(repr(s)[1:-1], '"', '\\"')

_special_builtins = [
  'locals',
  'vars',
  'globals',
  'range',
  'xrange',
]

_optimized_builtins = {
  'len' : 'builtin_len'
}

# These aren't well tested yet.
##   'type' : 'builtin_type',
##   'str'  : 'builtin_str',
##   'repr' : 'builtin_repr',
##   'cmp'  : 'builtin_cmp',
##   'apply' : 'builtin_apply',
## }

# Append on the builtins that are optimized
_special_builtins[len(_special_builtins):] = _optimized_builtins.keys()

_node_names = {
  'module' : 'n_module',
  'stmt' : 'n_stmt',
  'function' : 'n_function',
  'lambda' : 'n_lambda',
  'classdef' : 'n_classdef',
  'pass' : 'n_pass',
  'break' : 'n_break',
  'continue' : 'n_continue',
  'for' : 'n_for',
  'while' : 'n_while',
  'if' : 'n_if',
  'exec' : 'n_exec',
  'assert' : 'n_assert',
  'from' : 'n_from',
  'import' : 'n_import',
  'raise' : 'n_raise',
  'tryfinally' : 'n_tryfinally',
  'tryexcept' : 'n_tryexcept',
  'return' : 'n_return',
  'const' : 'n_const',
  'print' : 'n_print',
  'printnl' : 'n_printnl',
  'discard' : 'n_discard',
  'assign' : 'n_assign',
  'ass_tuple' : 'n_ass_tuple',
  'ass_list' : 'n_ass_list',
  'ass_name' : 'n_ass_name',
  'ass_attr' : 'n_ass_attr',
  'tuple' : 'n_tuple',
  'list' : 'n_list',
  'dict' : 'n_dict',
  'or' : 'n_or',
  'and' : 'n_and',
  'not' : 'n_not',
  'compare' : 'n_compare',
  'bitor' : 'n_bitor',
  'bitxor' : 'n_bitxor',
  'bitand' : 'n_bitand',
  'name' : 'n_name',
  'globals' : 'n_globals',
  '<<' : 'n_lshift',
  '>>' : 'n_rshift',
  '+' : 'n_plus',
  '-' : 'n_minus',
  '*' : 'n_star',
  '/' : 'n_slash',
  '%' : 'n_percent',
  'unary+' : 'n_uplus',
  'unary-' : 'n_uminus',
  'invert' : 'n_invert',
  'power' : 'n_power',
  'backquote' : 'n_backquote',
  'getattr' : 'n_getattr',
  'call_func' : 'n_call',
  'keyword' : 'n_keyword',
  'subscript' : 'n_subscript',
  'ellipsis' : 'n_ellipsis',
  'sliceobj' : 'n_sliceobj',
  'slice' : 'n_slice',
}

_func_cop = {
  'PyNumber_Or'          : '||',
  'PyNumber_And'         : '&&',
  'PyNumber_Xor'         : '^',
  'PyNumber_Lshift'      : '<<',
  'PyNumber_Rshift'      : '>>',
  'PyNumber_Add'         : '+',
  'PyNumber_Subtract': '-',
  'PyNumber_Multiply': '*',
  'PyNumber_Divide'      : '/',
  'PyNumber_Remainder' : '%',
  'PyNumber_Positive' : '',
  'PyNumber_Negative' : '-',
  'PyNumber_Invert'       : '!',
}

_cmod_header = '''\
/*
** Generated automatically by genc.py at %(time)s
** From source: %(src)s
*/

#include <Python.h>
#include <rename2.h>
#include <config.h>

static char %(cmod)s_doc[] = "%(doc)s";
static PyObject * %(cmod)s_Globals = NULL;

#define FC_NORMAL 0
#define FC_BREAK 1
#define FC_RETURN 2
#define FC_CONTINUE 3

/* snagged from set_exc_info in ceval.c in 1.5.2 */
static void %(cmod)s_ExposePyException
(
  PyObject *type,
  PyObject *value,
  PyObject *tb,
  PyObject **f_exc_type,
  PyObject **f_exc_value,
  PyObject **f_exc_traceback
)
{
	PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_Get();
	if (*f_exc_type == NULL) {
		/* This frame didn't catch an exception before */
		/* Save previous exception of this thread in this frame */
		if (tstate->exc_type == NULL) {
			Py_INCREF(Py_None);
			tstate->exc_type = Py_None;
		}
		tmp_type = *f_exc_type;
		tmp_value = *f_exc_value;
		tmp_tb = *f_exc_traceback;
		Py_XINCREF(tstate->exc_type);
		Py_XINCREF(tstate->exc_value);
		Py_XINCREF(tstate->exc_traceback);
		*f_exc_type = tstate->exc_type;
		*f_exc_value = tstate->exc_value;
		*f_exc_traceback = tstate->exc_traceback;
		Py_XDECREF(tmp_type);
		Py_XDECREF(tmp_value);
		Py_XDECREF(tmp_tb);
	}
	/* Set new exception for this thread */
	tmp_type = tstate->exc_type;
	tmp_value = tstate->exc_value;
	tmp_tb = tstate->exc_traceback;
	Py_XINCREF(type);
	Py_XINCREF(value);
	Py_XINCREF(tb);
	tstate->exc_type = type;
	tstate->exc_value = value;
	tstate->exc_traceback = tb;
	Py_XDECREF(tmp_type);
	Py_XDECREF(tmp_value);
	Py_XDECREF(tmp_tb);
	/* For b/w compatibility */
	PySys_SetObject("exc_type", type);
	PySys_SetObject("exc_value", value);
	PySys_SetObject("exc_traceback", tb);
}

/* snagged from reset_exc_info in ceval.c in 1.5.2 */
static void %(cmod)s_ResetPyException
(
    PyObject *f_exc_type,
    PyObject *f_exc_value,
    PyObject *f_exc_traceback
)
{
	PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_Get();
	if (f_exc_type != NULL) {
		/* This frame caught an exception */
		tmp_type = tstate->exc_type;
		tmp_value = tstate->exc_value;
		tmp_tb = tstate->exc_traceback;
		Py_XINCREF(f_exc_type);
		Py_XINCREF(f_exc_value);
		Py_XINCREF(f_exc_traceback);
		tstate->exc_type = f_exc_type;
		tstate->exc_value = f_exc_value;
		tstate->exc_traceback = f_exc_traceback;
		Py_XDECREF(tmp_type);
		Py_XDECREF(tmp_value);
		Py_XDECREF(tmp_tb);
		/* For b/w compatibility */
		PySys_SetObject("exc_type", f_exc_type);
		PySys_SetObject("exc_value", f_exc_value);
		PySys_SetObject("exc_traceback", f_exc_traceback);
	}
	tmp_type = f_exc_type;
	tmp_value = f_exc_value;
	tmp_tb = f_exc_traceback;
	Py_XDECREF(tmp_type);
	Py_XDECREF(tmp_value);
	Py_XDECREF(tmp_tb);
}
'''

_cmod_trailer = '''

%(methoddefs)s

static PyObject * %(mod)s_run_main(void)
{
    int finally_code = FC_NORMAL;
    PyObject *result;
%(gdecls)s

%(constants)s
%(objconstants)s
/* End of constants */

%(defaults)s

/* End of defaults */

%(gcode)s

    Py_INCREF(Py_None);
    return Py_None;

%(gerr)s
    return NULL;
}


static struct PyMethodDef %(mod)s_methods[] = {
%(methods)s
  { NULL, NULL } /* sentinel */
};

#ifdef _MSC_VER
_declspec(dllexport)
#endif
void init%(mod)s()
{
        PyObject *m, *r;

        m = Py_InitModule4("%(mod)s", %(mod)s_methods,
                                           %(mod)s_doc, NULL, PYTHON_API_VERSION);
        if ( m == NULL )
                Py_FatalError("can't initialize module %(mod)s");
                
        %(mod)s_Globals = PyModule_GetDict(m);
        PyDict_SetItem(
            %(mod)s_Globals,
            PyString_InternFromString("__builtins__"),
            PyImport_ImportModule("__builtin__"));
        
%(initlambda)s
        if ( PyErr_Occurred() )
                Py_FatalError("can't initialize module %(mod)s");

        r = %(mod)s_run_main();
        Py_XDECREF(r);

}
'''
#" #Hack for Emacs

_pymod_header = '''
#
# Generated automatically by genc.py at %s
# From source: %s
#

%s

from %s import *
'''

_func_defn = '''
static PyObject * %(nestedname)s(PyObject *self, PyObject *args, PyObject *kw)
{
    int finally_code = FC_NORMAL;
    PyObject *result = NULL;
%(decls)s%(args)s
%(body)s
    Py_INCREF(Py_None);
    return Py_None;
%(err)s
    return NULL;
}
'''

_exec_func      = '''
static int
%(cmod)s_do_exec(PyObject *prog, PyObject *globals, PyObject *locals)
{
        char *s;
        int n;
        PyObject *v;
        int plain = 0;

        if (PyTuple_Check(prog) && globals == Py_None && locals == Py_None &&
                ((n = PyTuple_Size(prog)) == 2 || n == 3)) {
                /* Backward compatibility hack */
                globals = PyTuple_GetItem(prog, 1);
                if (n == 3)
                        locals = PyTuple_GetItem(prog, 2);
                prog = PyTuple_GetItem(prog, 0);
        }
        if (globals == Py_None) {
                globals = PyEval_GetGlobals();
                if (locals == Py_None) {
                        locals = PyEval_GetLocals();
                        plain = 1;
                }
        }
        else if (locals == Py_None)
                locals = globals;
        if (!PyString_Check(prog) &&
                !PyCode_Check(prog) &&
                !PyFile_Check(prog)) {
                PyErr_SetString(PyExc_TypeError,
                           "exec 1st arg must be string, code or file object");
                return -1;
        }
        if (!PyDict_Check(globals) || !PyDict_Check(locals)) {
                PyErr_SetString(PyExc_TypeError,
                        "exec 2nd/3rd args must be dict or None");
                return -1;
        }
        if (PyDict_GetItemString(globals, "__builtins__") == NULL)
                PyDict_SetItemString(globals, "__builtins__", f->f_builtins);
        if (PyCode_Check(prog)) {
                v = PyEval_EvalCode((PyCodeObject *) prog,
                                        globals, locals);
                if (v == NULL)
                        return -1;
                Py_DECREF(v);
                return 0;
        }
        if (PyFile_Check(prog)) {
                FILE *fp = PyFile_AsFile(prog);
                char *name = PyString_AsString(PyFile_Name(prog));
                if (PyRun_File(fp, name, Py_file_input,
                                   globals, locals) == NULL)
                        return -1;
                return 0;
        }
        s = PyString_AsString(prog);
        if ((int)strlen(s) != PyString_Size(prog)) {
                PyErr_SetString(PyExc_ValueError,
                                "embedded '\\0' in exec string");
                return -1;
        }
        v = PyRun_String(s, Py_file_input, globals, locals);
        if (v == NULL)
                return -1;
        Py_DECREF(v);
        if (plain)
                PyFrame_LocalsToFast(f, 0);
        return 0;
}


'''

_raise_func = '''
/* Snagged from Python 1.5.1 ceval.c */
/* Logic for the raise statement (too complicated for inlining).
   This *consumes* a reference count to each of its arguments. */
static void
%(cmod)s_do_raise(PyObject *type, PyObject *value, PyObject *tb)
{
        if (type == NULL) {
                /* Reraise */
                PyThreadState *tstate = PyThreadState_Get();
                type = tstate->exc_type == NULL ? Py_None : tstate->exc_type;
                value = tstate->exc_value;
                tb = tstate->exc_traceback;
                Py_XINCREF(type);
                Py_XINCREF(value);
                Py_XINCREF(tb);
        }
                
        /* We support the following forms of raise:
           raise <class>, <classinstance>
           raise <class>, <argument tuple>
           raise <class>, None
           raise <class>, <argument>
           raise <classinstance>, None
           raise <string>, <object>
           raise <string>, None

           An omitted second argument is the same as None.

           In addition, raise <tuple>, <anything> is the same as
           raising the tuple's first item (and it better have one!);
           this rule is applied recursively.

           Finally, an optional third argument can be supplied, which
           gives the traceback to be substituted (useful when
           re-raising an exception after examining it).  */

        /* First, check the traceback argument, replacing None with
           NULL. */
        if (tb == Py_None) {
                Py_DECREF(tb);
                tb = NULL;
        }
        else if (tb != NULL && !PyTraceBack_Check(tb)) {
                PyErr_SetString(PyExc_TypeError,
                           "raise 3rd arg must be traceback or None");
                goto raise_error;
        }

        /* Next, replace a missing value with None */
        if (value == NULL) {
                value = Py_None;
                Py_INCREF(value);
        }

        /* Next, repeatedly, replace a tuple exception with its first item */
        while (PyTuple_Check(type) && PyTuple_Size(type) > 0) {
                PyObject *tmp = type;
                type = PyTuple_GET_ITEM(type, 0);
                Py_INCREF(type);
                Py_DECREF(tmp);
        }

        if (PyString_Check(type))
                ;

        else if (PyClass_Check(type))
                PyErr_NormalizeException(&type, &value, &tb);

        else if (PyInstance_Check(type)) {
                /* Raising an instance.  The value should be a dummy. */
                if (value != Py_None) {
                        PyErr_SetString(PyExc_TypeError,
                          "instance exception may not have a separate value");
                        goto raise_error;
                }
                else {
                        /* Normalize to raise <class>, <instance> */
                        Py_DECREF(value);
                        value = type;
                        type = (PyObject*) ((PyInstanceObject*)type)->in_class;
                        Py_INCREF(type);
                }
        }
        else {
                /* Not something you can raise.  You get an exception
                   anyway, just not what you specified :-) */
                PyErr_SetString(PyExc_TypeError,
                        "exceptions must be strings, classes, or instances");
                goto raise_error;
        }
        PyErr_Restore(type, value, tb);
        return;
 raise_error:
        Py_XDECREF(value);
        Py_XDECREF(type);
        Py_XDECREF(tb);
        return;
}
'''
# ' #Hack for Emacs

_print_func = '''
#include <ctype.h>
static int %(cmod)s_print_helper(PyObject *ob)
{
        PyObject *f = PySys_GetObject("stdout");
        int err;

        if ( f == NULL )
        {
                PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
                return -1;
        }
        if ( PyFile_SoftSpace(f, 1) )
                PyFile_WriteString(" ", f);
        err = PyFile_WriteObject(ob, f, Py_PRINT_RAW);
        if ( err == 0 && PyString_Check(ob) )
        {
                char *s = PyString_AS_STRING(ob);
                int len = PyString_Size(ob);
                if ( len > 0 && isspace(Py_CHARMASK(s[len-1])) && s[len-1] != ' ' )
                        PyFile_SoftSpace(f, 0);
        }
        return err;
}
static int %(cmod)s_print_helper_nl(void)
{
        PyObject *f = PySys_GetObject("stdout");

        if ( f == NULL )
        {
                PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
                return -1;
        }
        PyFile_WriteString("\\n", f);
        PyFile_SoftSpace(f, 0);
        return 0;
}
'''

_slicer_func = '''
static int %(cmod)s_slicer_helper(PyObject *seq, PyObject *obLow, PyObject *obHi, long *resLow, long *resHi)
{
        PySequenceMethods *sq = seq->ob_type->tp_as_sequence;
        int isize;

        if ( sq == NULL )
        {
                PyErr_SetString(PyExc_TypeError, "illegal slice of a non-sequence");
                return -1;
        }

        isize = (*sq->sq_length)(seq);
        if ( isize < 0 )
                return -1;

        if ( obLow == NULL )
                *resLow = 0;
        else if ( !PyInt_Check(obLow) )
                return -1;
        else
        {
                *resLow = PyInt_AsLong(obLow);
                if ( *resLow < 0 )
                        *resLow += isize;
        }

        if ( obHi == NULL )
                *resHi = isize;
        else if ( !PyInt_Check(obHi) )
                return -1;
        else
        {
                *resHi = PyInt_AsLong(obHi);
                if ( *resHi < 0 )
                        *resHi += isize;
        }

        return 0;
}
'''

_compare_funcs = '''
static int
%(cmod)s_cmp_member(PyObject *v, PyObject *w)
{
        int i, cmp;
        PyObject *x;
        PySequenceMethods *sq;
        /* Special case for char in string */
        if (PyString_Check(w))
        {
                register char *s, *end;
                register char c;
                if (!PyString_Check(v) || PyString_Size(v) != 1) {
                        PyErr_SetString(PyExc_TypeError,
                                "string member test needs char left operand");
                        return -1;
                }
                c = PyString_AS_STRING((PyStringObject *)v)[0];
                s = PyString_AS_STRING((PyStringObject *)w);
                end = s + PyString_Size(w);
                while (s < end) {
                        if (c == *s++)
                                return 1;
                }
                return 0;
        }
        sq = w->ob_type->tp_as_sequence;
        if (sq == NULL) {
                PyErr_SetString(PyExc_TypeError,
                        "'in' or 'not in' needs sequence right argument");
                return -1;
        }
        for (i = 0; ; i++) {
                x = (*sq->sq_item)(w, i);
                if (x == NULL) {
                        if (PyErr_Occurred() == PyExc_IndexError) {
                                PyErr_Clear();
                                break;
                        }
                        return -1;
                }
                cmp = PyObject_Compare(v, x);
                Py_XDECREF(x);
                if (cmp == 0)
                        return 1;
        }
        return 0;
}
'''

_kwarg_func = '''
/*
** %(cmod)s_kwarg notes:
**       args is arg tuple after VARARGS have been sliced off
**       format is the parseformat for the function
**               with a REQUIRED '|' at the beginning
**       kwIn is the keyword Dict passed into the Function
**       kwOut is the output keyword Dict
**       kwOut may be NULL (func does not have a kwwhere)
**       numpassed is the length of the args tuple
**       startdef is the 0-based index of the first argument that has a
**                default expression
**                e.g.: def f(a,b,c,d=4) startdef = 3
**       argnames is an array of PyObject **'s that are the addresses of a PyObject that contain the argument name not including the
**                VARARGS or KEYWORD variables
**                e.g.: def f(a,b,c,d, *va, **kw) would need a argnames array of:
**                              { "a", "b", "c", "d" }
**                if an argument position is a tuple, then it should be NULL
**       The rest of the parameters are where to stick the data once found.
**
**       Implementation notes:
**       kwIn must not be modified (it is owned by the core interpreter)
**       alloc kwOut if needed, copy all non useable keyword
**                 parameters into kwOut
**       argnames up thru numpassed cannot be in kwIn
**       argnames after numpassed must be in kwIn or have a def expr
**              if you have a tuple arg at pos N
**                and numpassed < N
**                and tuple arg doesn't have a def expr
**              then we have an error
**       the number of names in argnames is implied by the format string.
**       args cannot be longer than argnames/implied-by-format
**       it is legal for numpassed to be LONGER than args/argnames/format
**
**       len(argnames) == implied-by-format
**       len(args) <= len(argnames)
**       len(args) <= numpassed
*/

static int %(cmod)s_kwarg(
        PyObject *args,
        char *format,
        PyObject *kwIn,
        PyObject **kwOut,
        int numpassed,
        int startdef,
        const PyObject ***argnames,
        ...)
{
        int curarg;
        int level = 0;
        char c, msgbuf[256];
        int cKeys = 0;
        va_list va;

        va_start(va, argnames);

        if (!PyArg_VaParse(args, format, va))
          return -1;
        /* Reset va after VaParse */  
        va_end(va);

        /* If kwIn is NULL, bail */
        if (kwIn == NULL)
          return 1;
          
        /* if kwIn doesn't have any keys, don't do any more work */
        if ((cKeys = PyMapping_Length(kwIn)) == -1)
            return -1;
        if (cKeys == 0)
            return 1;

        /* start the varargs up again */
        va_start(va, argnames);

        /* if kwOut is not NULL, allocate it and copy kwIn into it. */
        if ( kwOut )
        {
                *kwOut = %(cmod)s_copydict(kwIn);
                if ( *kwOut == NULL )
                  return -1;
        }

        curarg = 0;
        /*
           important variables below
           char c loops over the format string
           int curarg is the current index into the argument list.
        */
           
        for ( ; c = *format++; )
        {
          if ( c == '(' )
          {
                  level++;

                  /*
                  ** Any tuple-style arguments must be passed in as a parameter or
                  ** have an associated default argument.  Note that kwIn cannot
                  ** supply the value.
                  */
                  if ( numpassed <= curarg && curarg < startdef )
                  {
                          strcpy(msgbuf, "not enough arguments");
                          goto error;
                  }
          }
          else if ( c == ')' )
          {
                  if (level == 1)
                          ++curarg;
                  level--;
          }
          else if ( c == 'O' )
          {
                  PyObject **o = va_arg(va, PyObject **);

                  /* tuple args will have been supplied already, handle top-level */
                  if ( level == 0 )
                  {
                          int k;
                          PyObject *curargname = (PyObject *)*(argnames[curarg]);

                          /*
                          ** This checks for something that was passed in as an argument
                          ** as well as in the kwIn dictinary.
                          */
                          k = PyMapping_HasKey(kwIn, curargname);
                          if ( k && curarg < numpassed )
                          {
                                  sprintf(msgbuf, "keyword parameter %%s redefined", argnames[curarg]);
                                  goto error;
                          }

                          /*
                          ** this arg was passed and isn't in the in/out dictionary. we
                          ** have no more work for this argument
                          */
                          if ( curarg < numpassed )
                          {
                                  ++curarg;
                                  continue;
                          }

                          /*
                          ** The if condition is true if somebody forgot to pass in
                          ** values for arguments that don't have default expressions.
                          */
                          if ( !k && curarg < startdef )
                          {
                                   sprintf(msgbuf,
                                                   "Missing required argument: %%s", argnames[curarg]);
                                   goto error;
                          }

                          if ( k )
                          {
                                  /* Set the output variable (w/o its own ref) */
                                  *o = PyDict_GetItem(kwIn, curargname);

                                  /* remove the variable from kwOut since we used it */
                                  if ( kwOut )
                                          PyMapping_DelItem(*kwOut, curargname);
                          }

                          ++curarg;
                  }
          }
        }  

        va_end(va);
        return 1;

  error:
        PyErr_SetString(PyExc_TypeError, msgbuf);
        if ( kwOut != NULL && *kwOut )
                Py_DECREF(*kwOut);
        va_end(va);
        return 0;
}
'''

_copydict_func = '''
static PyObject * %(cmod)s_copydict(PyObject *dict)
{
        int pos = 0;
        PyObject * result = PyDict_New();
        PyObject * key;
        PyObject * value;

        if ( result )
                while ( PyDict_Next(dict, &pos, &key, &value) )
                        PyDict_SetItem(result, key, value);

        return result;
}
'''

# Code from:
# l = lambda a=x,b=y, *___va, **___kw: apply(c, (a,b) + ___va, ___kw)

##           3 LOAD_CONST          0 (apply)
##           6 LOAD_CONST          1 (c)
##           9 LOAD_FAST           0 (a)
##          12 LOAD_FAST           1 (b)
##          15 BUILD_TUPLE         2
##          18 LOAD_FAST           2 (___va)
##          21 BINARY_ADD
##          22 LOAD_FAST           3 (___kw)
##          25 CALL_FUNCTION       3
##          28 RETURN_VALUE

# cbOP = 3;
# Size of prologue + loads for argument + build_tuple
# cb = sizeof(prologue) + cbOp * (cArgs + 1)
# Handle variable args
# cb = cb + cbOP * 2 # Handle load for arg, and binary_add
# Handle keyword
# cb = cb + cbOp




_lambda_helpers = '''
#include <compile.h>
static const char g_%(cmod)s_lambda_prologue[] =
{
        100, 0, 0,              /* LOAD_CONST     0      ('apply') */
        100, 1, 0,              /* LOAD_CONST     1      (func)    */
};

static PyObject * g_%(cmod)s_lambda_varnames = NULL;
static PyObject * g_%(cmod)s_lambda_filename = NULL;
static PyObject * g_%(cmod)s_lambda_name = NULL;
static PyObject * g_%(cmod)s_lambda_apply = NULL;



static void %(cmod)s_lambda_init()
{
        g_%(cmod)s_lambda_filename = Py_BuildValue("s", "%(cmod)s");
        g_%(cmod)s_lambda_name = Py_BuildValue("s", "<lambda>");
        g_%(cmod)s_lambda_apply = PyDict_GetItemString(PyEval_GetBuiltins(), "apply");
}

static PyObject * %(cmod)s_newcode(PyMethodDef * pmd, int cArgs, int flags, const PyObject ***argnames)
{
        PyObject * function = NULL;
        PyObject * constsOb = NULL;
        PyObject * code = NULL;
        PyObject * codeob = NULL;
        PyObject * varnames = NULL;
        unsigned int cb;
        char * pCode = NULL;
        int i;
        char * IP = NULL;

        function = PyCFunction_New(pmd, NULL);
        if ( function == NULL )
                return NULL;
        constsOb = Py_BuildValue("OO", g_%(cmod)s_lambda_apply, function);
        Py_DECREF(function);
        if ( constsOb == NULL )
                return NULL;
// Size of instruction
#define cbOP 3
        cb = sizeof(g_%(cmod)s_lambda_prologue) +
             // Cost of loading arguments, and BUILD_TUPLE
             cbOP * (cArgs + 1) +
             // Cost of loading vararg param, and BINARY_ADD
             cbOP + 1 +
             // Cost of loading kw param
             cbOP +
             // Cost of the function call & return
             cbOP * 2;

        pCode = PyMem_NEW(char, cb);
        if (pCode == NULL)
        {
            goto Error;
        }

        // Fill in pCode with data.
        // First the prologue
        memcpy(pCode, g_%(cmod)s_lambda_prologue, sizeof(g_%(cmod)s_lambda_prologue));
        IP = pCode + sizeof(g_%(cmod)s_lambda_prologue);

// This magic was grabbed from compile.c:com_addint()
#define ADDARG(i) do { *(IP++) = (i) & 0xff; *(IP++) = (i) >> 8; } while (0)
        
        // Then the arguments.
        for(i = 0; i < cArgs; i++)
        {
            *(IP++) = 124;
            ADDARG(i);
        }

        // Build the tuple
        *(IP++) = 102;
        ADDARG(cArgs);

        // Only contcatenate the tuples if necessary.
        if (flags & CO_VARARGS)
        {
            // Load the vararg param
            *(IP++) = 124;
            ADDARG(cArgs);

            // Do the BINARY_ADD
            *(IP++) = 23;
        }

        // Only use the kw arg if necessary.
        if (flags & CO_VARKEYWORDS)
        {
           // Load the KW param
           *(IP++) = 124;
           ADDARG(cArgs + 1);
        }

        // Call the function
        *(IP++) = (char)131;
        if (flags & CO_VARKEYWORDS)
        {
           ADDARG(3);
        }
        else
        {
           ADDARG(2);
        }

        // Return
        *(IP++) = 83;

        // Phew, we're all done with that part.
        codeob = PyString_FromStringAndSize(pCode, cb);
        PyString_InternInPlace(&codeob);

        // Now fill in the varname tuple:
        varnames = PyTuple_New(cArgs);
        for(i = 0; i < cArgs; i++)
        {   Py_INCREF((PyObject *)*argnames[i]);
            PyTuple_SET_ITEM(varnames, i, (PyObject *)*argnames[i]);
        }

        code = (PyObject *)PyCode_New(cArgs, /* argcount */
                                      cArgs + 2, /* nlocals */
                                      5, /* stackszie */
                                      /* 0, 2, */
                                      CO_OPTIMIZED | CO_NEWLOCALS | flags, /* flags */
                                      codeob, /* code obj */
                                      constsOb, /* const obj */
                                      varnames, /* list of strings (names used) */
                                      varnames, /* tuple of strings (locacl variable names) */
                                      g_%(cmod)s_lambda_filename, /* filename */
                                      g_%(cmod)s_lambda_name,         /* string (name, for reference) */
                                      0, /* first source line # */
                                      PyString_FromString("") /* string (encoding addr<->lineno mapping) */
                                      );
        Py_DECREF(constsOb);
        Py_DECREF(codeob);
        Py_DECREF(varnames);
        PyMem_DEL(pCode);
        return code;
Error:
        Py_XDECREF(constsOb);
        Py_XDECREF(codeob);
        Py_XDECREF(varnames);
        PyMem_Free(pCode);
        return NULL;
}

'''

_methoddef_format = '''
PyMethodDef PyMethDef_%(name)s = { "<lambda %(name)s>", %(name)s, METH_VARARGS|METH_KEYWORDS, NULL };
'''

_subscript_helpers = '''
static int
%(cmod)s_assign_subscript(PyObject *w, PyObject *key, PyObject *v)
{
        PyTypeObject *tp = w->ob_type;
        PySequenceMethods *sq;
        PyMappingMethods *mp;
        int (*func1)();
        int (*func2)();
        if ((mp = tp->tp_as_mapping) != NULL &&
                (func1 = mp->mp_ass_subscript) != NULL)
        {
                return (*func1)(w, key, v);
        }
        else if ((sq = tp->tp_as_sequence) != NULL &&
                         (func2 = sq->sq_ass_item) != NULL)
        {
                if (!is_intobject(key))
                {
                        PyErr_SetString(PyExc_TypeError,
                                "sequence subscript must be integer (assign or del)");
                        return -1;
                }
                else
                {
                        int i = PyInt_AsLong(key);
                        if (i < 0)
                        {
                                int len = (*sq->sq_length)(w);
                                if (len < 0)
                                        return -1;
                                i += len;
                        }
                        return (*func2)(w, i, v);
                }
        }
        else
        {
                PyErr_SetString(PyExc_TypeError,
                        "can't assign to this subscripted object");
                return -1;
        }
}

'''

# ' #Hack for Emacs

_import_func = '''
/* Hacked version of PyImport_Import to not pass __import__()s fourth arg */

PyObject *
Py2C_Import(PyObject *module_name)
{
	static PyObject *builtins_str = NULL;
	static PyObject *import_str = NULL;
	static PyObject *standard_builtins = NULL;
	PyObject *globals = NULL;
	PyObject *import = NULL;
	PyObject *builtins = NULL;
	PyObject *r = NULL;

    if (builtins_str == NULL)
    {
        builtins_str = PyString_InternFromString("__builtins__");
    }

    if (import_str == NULL)
    {
        import_str = PyString_InternFromString("__import__");
    }
    
	/* Get the builtins from current globals */
	globals = PyEval_GetGlobals();
	if(globals != NULL) {
	        Py_INCREF(globals);
		builtins = PyObject_GetItem(globals, builtins_str);
		if (builtins == NULL)
			goto err;
	}
	else {
		/* No globals -- use standard builtins, and fake globals */
		PyErr_Clear();

		if (standard_builtins == NULL) {
			standard_builtins =
				PyImport_ImportModule("__builtin__");
			if (standard_builtins == NULL)
				return NULL;
		}

		builtins = standard_builtins;
		Py_INCREF(builtins);
		globals = Py_BuildValue("{OO}", builtins_str, builtins);
		if (globals == NULL)
			goto err;
	}

	/* Get the __import__ function from the builtins */
	if (PyDict_Check(builtins))
		import=PyObject_GetItem(builtins, import_str);
	else
		import=PyObject_GetAttr(builtins, import_str);
	if (import == NULL)
		goto err;

	/* Call the _import__ function with the proper argument list */
	r = PyObject_CallFunction(import, "OOO",
				  module_name, globals, globals);

  err:
	Py_XDECREF(globals);
	Py_XDECREF(builtins);
	Py_XDECREF(import);
 
	return r;
}

static int
%(cmod)s_import_from(PyObject *locals, PyObject *v, PyObject *name)
{
        PyObject *w, *x;
        if (!PyModule_Check(v)) {
                PyErr_SetString(PyExc_TypeError,
                                "import-from requires module object");
                return -1;
        }
        w = PyModule_GetDict(v);
        if (PyString_AsString(name)[0] == '*') {
                int pos, err;
                PyObject *name, *value;
                pos = 0;
                while (PyDict_Next(w, &pos, &name, &value)) {
                        if (!PyString_Check(name) ||
                                PyString_AsString(name)[0] == '_')
                                continue;
                        Py_INCREF(value);
                        err = PyDict_SetItem(locals, name, value);
                        Py_DECREF(value);
                        if (err != 0)
                                return -1;
                }
                return 0;
        }
        else {
                x = PyDict_GetItem(w, name);
                if (x == NULL) {
                        char buf[250];
                        sprintf(buf, "cannot import name %%.230s",
                                PyString_AsString(name));
                        PyErr_SetString(PyExc_ImportError, buf);
                        return -1;
                }
                else
                        return PyDict_SetItem(locals, name, x);
        }
}
'''




