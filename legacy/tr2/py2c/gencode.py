#!/usr/local/bin/python
# Copyright 1997-1998 Greg Stein and Bill Tutt
import parser
import token
import symbol
import sys
import string
import getopt

optlist, args = getopt.getopt(sys.argv[1:], 'tp')
if len(args) < 1 or len(args) > 3:
  print "USAGE: %s [-t] filename [ cfile pyfile ]" % sys.argv[0]
  print "   -t   print the raw parse tree, rebuilt as Python source"
  sys.exit(1)

print_tree = ('-p', '') in optlist
print_transformed = ('-t', '') in optlist

def gen_python(node, indent=0):
  x = node[0]
  if token.ISTERMINAL(x):
    print "%*s%s: %s" % (indent, '', token.tok_name[x],
                         string.join(map(repr, node[1:])))
  else:
    print "%*s%s:" % (indent, '', symbol.sym_name[x])
    for n in node[1:]:
      gen_python(n, indent+2)

if print_tree:
  ast = parser.suite(open(args[0]).read())
  tree = parser.ast2tuple(ast,1)
  gen_python(tree)
elif len(args) > 1:
  import genc
  genc.Generator(args[0], args[1], args[2])
else:
  import transformer
  import pprint
  t = transformer.Transformer()
  pprint.pprint(t.parsefile(args[0]).asList())
