
import copy_reg, types, new
from cPickle import *

def method_pickle(method):
	
	return method_unpickle, (method.im_func.__name__,
							 method.im_self,
							 method.im_class)

def method_unpickle(im_name,
					im_self,
					im_class):
	
	unbound=getattr(im_class,im_name)
	if im_self is None:
		return unbound
	bound=new.instancemethod(unbound.im_func,
							 im_self,
							 im_class)
	return bound

def module_pickle(module):
	return module_unpickle, (module.__name__,)

def module_unpickle(name):
	return __import__(name,None,None,1)

def function_pickle(function):
	
	function_name=function.__name__
	module_name=function.func_globals['__name__']
	return function_unpickle, (module_name,
							   function_name)

##def ellipsis_pickle(ellipsis):
##	return ellipsis_unpickle,('')

##def ellipsis_unpickle(str):
##	return Ellipsis

def function_unpickle(module_name,
					  function_name):

	module=__import__(module_name,
					  # none none because there is no context
					  # for this import, 1 because we want the
					  # subpackage (if this is one)
					  None,None,1)
	return getattr(module, function_name)


copy_reg.pickle(types.MethodType,
				method_pickle,
				method_unpickle)

copy_reg.pickle(types.ModuleType,
				module_pickle,
				module_unpickle)

##copy_reg.pickle(types.EllipsisType,
##				ellipsis_pickle,
##				ellipsis_unpickle)
