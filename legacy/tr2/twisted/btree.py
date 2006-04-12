#!/usr/bin/env python

class BNode:
	def __init__(self,tree):
		self.tree=tree
		self.nodes, self.keys, self.values = [], [], []

	def split(self,childno):
		"""
		split the given sub-node of this node
		
		preconditions: self.nodes must be at least childno long
		               self.nodes[childno] must be full
					   self must NOT be full
		"""
		order=self.tree.order
		left=self.nodes[childno]
		right=BNode(self.tree)

		self.nodes.insert(childno+1, right)
		self.keys.insert(childno, left.keys[order-1])
		self.values.insert(childno, left.keys[order-1])

		right.keys[:] = left.keys[order:]
		right.values[:] = left.values[order:]

		del left.keys[order-1:]
		del left.values[order-1:]
		
		if not left.leaf():
			right.nodes[:] = left.nodes[order:]
			del left.nodes[order:]

	def full(self):
		return len(self.keys) == (self.tree.order*2)-1
	
	def leaf(self):
		return not len(self.nodes)

	def find(self, key):

		i=0
		while (i < len(self.keys)) and (key > self.keys[i]):
			i=i+1

		return i
	
	def insert(self,key,value):
		"""
		insert the given key and value

		precondition: self is not full
		"""

		pos=self.find(key)

		if self.leaf():
			self.keys.insert(pos, key)
			self.values.insert(pos, value)
		else:
			node=self.nodes[pos]
			if node.full():
				self.split(pos)

				if key > self.keys[pos]:
					pos=pos+1

			self.nodes[pos].insert(key,value)

	def format(self,level):
		print " "*(level),self.keys
		for i in self.nodes:
			i.format(level+1)

	def walk(self, walker):
		if self.leaf():
			for key in self.keys:
				walker(key)
		else:
			for i in range(len(self.keys)):
				self.nodes[i].walk(walker)
				walker(self.keys[i])
			self.nodes[i+1].walk(walker)
			
class BTree:
	def __init__(self,order):
		self.order=order
		self.root=BNode(self)

	def insert(self,key,value):
		
		if self.root.full():
			s=BNode(self)
			s.nodes.append(self.root)
			s.split(0)
			self.root=s

		self.root.insert(key,value)
		
	def format(self):
		self.root.format(0)

from random import randint

def _test():
	b=BTree(10)
	x=range(10000)

	class TestWalker:
		def __init__(self):
			self.list=[]
		def __call__(self, arg):
			self.list.append(arg)
		def test(self):
			tst=self.list[:]
			tst.sort()
			return tst == self.list

	for i in x:
		b.insert(str(i),i)
	tw=TestWalker()
	# b.format()
	b.root.walk(tw)
	assert tw.test(), 'broken'

if __name__=='__main__':
	_test()
