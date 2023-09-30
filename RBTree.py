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
		self._nil: Nil = Nil()
		self._root: Union[Node, Nil] = self._nil
		self._lenght: int = 0

	def search(self, data: Union[int, float, str]) -> Union[Node, None]:
		"""find element in the tree"""
		node = self._root
		while node != self._nil:
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
		new_node = Node(data=data, left=self._nil, right=self._nil) # create new node
		if self._root == self._nil: self._root = new_node # set a new root if there is nil
		else: # root is existing
			prev = self._root # the parent for the new node
			while True:
				if new_node.data > prev.data:
					if prev.right != self._nil:
						prev = prev.right # next node
					else:
						prev.right = new_node # set new node
						new_node.prev = prev # set parent for the new node
						break # leave the loop
				elif new_node.data < prev.data:
					if prev.left != self._nil:
						prev = prev.left # next node
					else:
						prev.left = new_node # set new node
						new_node.prev = prev # set parent for the new node
						break # leave the loop
				else: # if such a node already exists in the tree
					self._lenght -= 1 # decrease lenght
					return # exit the insert()
		self._fix(new_node) # fix the tree after new node inserting

	def _fix(self, node: Node) -> NoReturn:
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
						self._rotate_right(node) # need right rotate if node in left side
					node.prev.red = False # if node already in left side set black for parent
					node.prev.prev.red = True # red for parent's parent
					self._rotate_left(node.prev.prev) # left rotate parent's parent
			else: # uncle on the right side
				if node.prev.prev.right.red: # check uncle's color
					node.prev.prev.right.red = False # set black for uncle
					node.prev.red = False # set black for parent
					node.prev.prev.red = True # set red for (uncle, parent)'s parent
					node = node.prev.prev # next fixing iteration
				else: # uncle is not communist
					if node == node.prev.right: # сheck node's position
						node = node.prev
						self._rotate_left(node) #rotate parent to left side
					node.prev.red = False # set parent black
					node.prev.prev.red = True # set parent's parent red
					self._rotate_right(node.prev.prev) # right rotate for parent's parent
		self._root.red = False # paint the root black

	def _rotate_right(self, nodeX: Node):
		"""rotate the tree to the right relative to the incoming node.
		we pull the node to the right."""
		nodeY = nodeX.left # save Y is X left child
		nodeX.left = nodeY.right # set new child for X is Y right child

		if nodeX.left != self._nil: # if new X child is not Nil-set new parent for new X child
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

	def _rotate_left(self, nodeX: Node):
		"""rotate the tree to the left relative to the incoming node.
		we pull the node to the left."""
		# check left_rotate() comments for info what is happening
		nodeY = nodeX.right
		nodeX.right = nodeY.left

		if nodeX.right != self._nil:
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

	def delete(self, data: Union[int, float, str]):
		"""delete node from the tree. first try to get a node which has 0-2childs."""
		node = self.search(data)
		if node is None:
			return
		self._lenght -= 1
		color = node.red
		if node.left == self._nil:
			nodetmp = node.right
			self._swap_nodes(node, nodetmp)
		elif node.right == self._nil:
			nodetmp = node.left
			self._swap_nodes(node, nodetmp)
		else:
			successor = self._find_successor(node.right)
			color = successor.red
			nodetmp = successor.right
			if successor.prev == node:
				nodetmp.prev = successor
			else:
				self._swap_nodes(successor, successor.right)
				successor.right = node.right
				successor.right.prev = successor
			self._swap_nodes(node, successor)
			successor.left = node.left
			successor.left.prev = successor
			successor.red = node.red
		if color is False:
			self._fix_deletion(nodetmp)

	def _fix_deletion(self, node: Node):
		"""fix tree after node deletion"""
		while node != self._root and node.red is False:
			if node == node.prev.left: # check node position
				nodes = node.prev.right # brother/sister
				if nodes.red: # brother/sister is red
					nodes.red = False
					node.prev.red = True
					self._rotate_left(node.prev)
					nodes = node.prev.right
				if nodes.left.red is False and nodes.right.red is False:
					nodes.red = True
					node = node.prev
				else: # brother/sister is black
					if nodes.right.red is False: # brother's/sister's right child is black
						nodes.left.red = False
						nodes.red = True
						self._rotate_right(nodes)
						nodes = node.prev.right
					nodes.red = node.prev.red
					node.prev.red = False
					nodes.right.red = False
					self._rotate_left(node.prev)
					node = self._root
			else: # node in right position from parent
				nodes = node.prev.left # brother/sister
				if nodes.red: # brother/sister is red
					nodes.red = False
					node.prev.red = True
					self._rotate_right(node.prev)
					nodes = node.prev.left
				if nodes.right.red is False and nodes.left.red is False:
					nodes.red = True
					node = node.prev
				else:
					if nodes.left.red is False:
						nodes.right.red = False
						nodes.red = True
						self._rotate_left(nodes)
						nodes = node.prev.left
					nodes.red = node.prev.red
					node.prev.red = False
					nodes.left.red = False
					self._rotate_right(node.prev)
					node = self._root
		node.red = False

	def _find_successor(self, node: Node) -> Node:
		"""find node successor"""
		while node.left is not self._nil:
			node = node.left
		return node

	def _swap_nodes(self, old: Node, new: Node):
		"""replace nodes"""
		if not old.prev:
			self._root = new
		elif old == old.prev.left:
			old.prev.left = new
		else:
			old.prev.right = new
		new.prev = old.prev

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
	pass

if __name__ == "__main__":
	main()