from imagination.deployment import deploy

d = {}
execfile("config", {}, d)

print d
application = deploy(**d)
