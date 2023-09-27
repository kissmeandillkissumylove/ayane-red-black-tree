"""
red-black tree implementation
https://github.com/kissmeandillkissumylove
"""

from __future__ import annotations
from typing import Union, Any, NoReturn
from random import randint

class Node:
	"""class for red-black tree nodes with values"""
	def __init__(self,
	             data: Union[int, float, str],
	             left: Union[Node, Nil]=None,
	             right: Union[Node, Nil]=None,
	             prev: Union[Node, Nil]=None,
	             red: bool=True):
		"""
		data: any value that we can compare
		left: left child (Node or Nill)
		right: right child (Node Nill)
		prev: node parrant
		red: color is red or black
		"""
		self.data = data
		self.left = left
		self.right = right
		self.prev = prev
		self.red = red

class Nil(Node):
	"""class for nodes without values (Nil)"""
	def __init__(self):
		"""
		call super() and put None for data and False for red color
		"""
		super().__init__(data=None, red=False)

class RBTree:
	"""red-black binary tree"""
	def __init__(self):
		"""
		root: tree root
		nil: Nil node initialization
		_lenght: len(RBtree)
		"""
		self.__nil: Nil = Nil()
		self._root: Union[Node, Nil] = self.__nil
		self._lenght: int = 0

	def search(self, data: Union[int, float, str]) -> Union[Node, None]:
		"""find element in the tree"""
		node = self._root
		while node != self.__nil:
			if data == node.data:
				return node # found node
			elif data > node.data:
				node = node.right
			elif data < node.data:
				node = node.left
		else:
			return # None if no node in the tree

	def insert(self, data: Union[int, float, str]) -> None:
		"""insert new node in the tree:
		data: any value that we can compare"""
		self._lenght += 1 # increase length
		new_node = Node(data=data, left=self.__nil, right=self.__nil) # create new node
		if self._root == self.__nil: self._root = new_node # set a new root if there is nil
		else: # root is existing
			prev = self._root # the parent for the new node
			while True:
				if new_node.data > prev.data:
					if prev.right != self.__nil:
						prev = prev.right # next node
					else:
						prev.right = new_node # set new node
						new_node.prev = prev # set parent for the new node
						break # leave the loop
				elif new_node.data < prev.data:
					if prev.left != self.__nil:
						prev = prev.left # next node
					else:
						prev.left = new_node # set new node
						new_node.prev = prev # set parent for the new node
						break # leave the loop
				else: # if such a node already exists in the tree
					self._lenght -= 1 # decrease lenght
					return # exit the insert()
		self.__fix(new_node) # fix the tree after new node inserting

	def __fix(self, node: Node) -> NoReturn:
		"""fix the tree after inserting"""
		while node != self._root and node.prev.red:
			# be sure to check which side the uncle is on and look at his color.
			# this is mandatory, because the uncle is the most important informing element
			# about everything (black height, our position)
			if node.prev == node.prev.prev.right: # uncle on the right side
				if node.prev.prev.left.red: # check uncle's color
					node.prev.prev.left.red = False # set black color for uncle
					node.prev.red = False # set red color for node's parent
					node.prev.prev.red = True # set red color for parent's parent
					node = node.prev.prev # set new node for next loop iteration
				else: # uncle is black
					if node == node.prev.left: # check node's position from parent
						node = node.prev
						self.__rotate_right(node) # need right rotate if node in left side
					node.prev.red = False # if node already in left side set black for parent
					node.prev.prev.red = True # red for parent's parent
					self.__rotate_left(node.prev.prev) # left rotate parent's parent
			else: # uncle on the right side
				if node.prev.prev.right.red: # check uncle's color
					node.prev.prev.right.red = False # set black for uncle
					node.prev.red = False # set black for parent
					node.prev.prev.red = True # set red for (uncle, parent)'s parent
					node = node.prev.prev # next fixing iteration
				else: # uncle is not communist
					if node == node.prev.right: # сheck node's position
						node = node.prev
						self.__rotate_left(node) #rotate parent to left side
					node.prev.red = False # set parent black
					node.prev.prev.red = True # set parent's parent red
					self.__rotate_right(node.prev.prev) # right rotate for parent's parent
		self._root.red = False # paint the root black

	def __rotate_right(self, nodeX: Node) -> NoReturn:
		"""rotate the tree to the right relative to the incoming node.
		we pull the node to the right."""
		nodeY = nodeX.left # save Y is X left child
		nodeX.left = nodeY.right # set new child for X is Y right child

		if nodeX.left != self.__nil: # if new X child is not Nil-set new parent for new X child
			nodeX.left.prev = nodeX

		nodeY.prev = nodeX.prev # set X's parent for Y
		if nodeY.prev == None: # if Y has no parent then Y was a root
			self._root = nodeY # set new root
		elif nodeX == nodeX.prev.right: # check X position from X's parent
			nodeY.prev.right = nodeY # tell parent about new child
		else:
			nodeY.prev.left = nodeY # tell parent about new child

		nodeY.right = nodeX # set Y' right child is X
		nodeX.prev = nodeY # set new parent for X is Y

	def __rotate_left(self, nodeX: Node) -> NoReturn:
		"""rotate the tree to the left relative to the incoming node.
		we pull the node to the left."""
		# check left_rotate() comments for info what is happening
		nodeY = nodeX.right
		nodeX.right = nodeY.left

		if nodeX.right != self.__nil:
			nodeX.right.prev = nodeX

		nodeY.prev = nodeX.prev
		if nodeY.prev == None:
			self._root = nodeY
		elif nodeX == nodeX.prev.right:
			nodeY.prev.right = nodeY
		else:
			nodeY.prev.left = nodeY

		nodeY.left = nodeX
		nodeX.prev = nodeY

	def delete(self, data: Union[int, float, str]) -> None:
		"""delete node from tree"""
		self._lenght -= 1  # decrease lenght
		node = self.search(data)
		if node != None:  # if node is exist
			if node.red:  # check is node red or black
				if node.left == node.right: # if both childs are Nils
					if node.prev.right == node:
						node.prev.right = self.__nil
						return
					else:
						node.prev.left = self.__nil
						return
				else:
					nodeL, nodeR = node.left, node.right
					while nodeL.right != self.__nil and nodeR.left != self.__nil:
						if nodeL.right != self.__nil:
							nodeL = nodeL.right
						if nodeR.left != self.__nil:
							nodeR = nodeR.left
					if nodeL.red:
						node.data = nodeL.data
						nodeL.prev.right = self.__nil
						return
					elif nodeR.red:
						node.data = nodeR.data
						nodeR.prev.left = self.__nil
						return
					else: #both nodes are black
						if nodeL.left != self.__nil:
							node.data = nodeL.data
							nodeL.data = nodeL.left.data
							nodeL.left = self.__nil
							return
						elif nodeR.right != self.__nil:
							node.data = nodeR.data
							nodeR.data = nodeR.right.data
							nodeR.right = self.__nil
							return
						else: # both black nodes have no childs
							node.data = nodeL.data
							if nodeL.prev.left != nodeL:
								if nodeL.prev.left.red:
									self.__rotate_right(nodeL.prev)
									nodeL.prev.prev.red = False
									nodeL.prev.left.red = True
									nodeL.prev.right = self.__nil
									self.__rotate_left(node)
									return
								else:
									nodeL.prev.left.red = True
									nodeL.prev.right = self.__nil
									self.__rotate_left(node)
									return
							else:
								nodeL.prev.red = False
								nodeL.prev.right.red = True
								nodeL.prev.left = self.__nil
								return
			else:  # node is black
				if node.left == node.right:
					raise ValueError
				elif node.left == self.__nil:
					raise ValueError
				elif node.right == self.__nil:
					raise ValueError
				elif node.left != self.__nil and node.right != self.__nil:
					raise ValueError
		else:
			self._lenght += 1

	def out(self, root: Node) -> NoReturn:
		"""display the tree in the terminal. this is not the best solution in terms of
		complexity, but it can output the tree visually. so, you don't have to use this
		method to output the tree. you can use another method with regular recursion.
		use this when the number of elements is no more than 100, otherwise it will be
		hard to see. the color of black elements is colored blue for clarity in terminals
		where the background is black."""
		nodes, height = [self._root], 90
		while nodes:
			for node in nodes:
				if node:
					if node == "S":
						print(" ", end=" ")
					else:
						print(" " * height, ((("\033[91m" + str(
									node.data) + "\033[0m") if node.red == True else (
										"\033[96m" + str(
									node.data) + "\033[0m")) if node.data is not None else (
									"")), end=" " * height)
			print("\n")
			for elt in range(0, len(nodes)):
				node = nodes.pop(0)
				if node:
					if node == "S":
						nodes.append("S")
						if len(nodes) == nodes.count(nodes[0]):
							nodes = []
							break
					else:
						nodes.append(node.left)
						nodes.append(node.right)
				else:
					nodes.append("S")
					nodes.append("S")
			height //= 2

	def out_simple(self, node: Node) -> NoReturn:
		"""another solution for fast tree output. the color of black elements is colored blue
		for clarity in terminals where the background is black."""
		if node:
			if node.red:
				print("\033[91m" + str(node.data) + "\033[0m", end=" ")
			else:
				if node.data != None:
					print("\033[96m" + str(node.data) + "\033[0m", end=" ")
			self.out_simple(node.left)
			self.out_simple(node.right)

	def get_lenght(self) -> int:
		"""returns red-black tree lenght"""
		return self._lenght

	def get_root(self) -> Node:
		"""returns red-black tree root"""
		return self._root

def main():
	"""main function"""
	tree = RBTree()
	add = [elt for elt in range(0, 15)]
	for elt in add:
		tree.insert(elt)
	tree.out(tree.get_root())
	tree.out_simple(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	print(tree.search(1), tree.search(4), tree.search(66))
	tree.delete(12)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(14)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(7)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(6)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(5)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(11)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(8)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())
	tree.delete(13)
	tree.out(tree.get_root())
	print("\nlenght =", tree.get_lenght())

if __name__ == "__main__":
	main()