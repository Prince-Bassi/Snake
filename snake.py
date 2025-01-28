import pygame
import config


class SnakeNode:
	def __init__(self, pos, nextPart=None, prevPart=None):
		self.pos = pos
		self.next = nextPart
		self.prev = prevPart

class Snake:
	def __init__(self):
		self.pos = (90, 90)
		self.dir = (0, 1)
		self.head = SnakeNode(self.pos)
		self.tail = None

		self.posSet = set()
		self.grow = True

	def move(self):
		newPos = (self.pos[0] + config.SPEED * self.dir[0], self.pos[1] + config.SPEED * self.dir[1])
		newNode = SnakeNode(newPos, self.head)
		self.posSet.add(self.head.pos)
		self.pos = newPos

		self.head.prev = newNode
		if not self.head.next:
			self.tail = self.head

		self.head = newNode

		if not self.grow:
			newTail = self.tail.prev
			newTail.next = None
			self.posSet.remove(self.tail.pos)

			self.tail = newTail
		else:
			self.grow = False