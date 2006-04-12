include Makefile.config.local

include Class.dep
include RMI.dep
include Main.dep
include Makefile.dist
include Makefile

# This is only available if Jikes is around and working, but it allows
# for the intelligent recompilation of various dependencies. (No it
# doesn't: Jikes doesn't output GNU compatible makefiles, or
# something...)

#  include Jikes.dep

world: class-targets rmi-targets main-targets
	@echo "World made."