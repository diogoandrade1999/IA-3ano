from mapa import Map
from characters import DIR, distance
from game import Bomb
import collections


def neighbours(actual_pos: tuple, mapa: Map, wallpass: bool, invalid: list) -> list:
	"""
	Calculate the neighbours from one position
	:param actual_pos: actual position
	:param mapa: mapa
	:param wallpass: almost of cases use the power wallpass, but if the objetive is break walls, this power need be enable
	:param invalid: invalid positions
	:return:
	"""
	if invalid is None: invalid = []
	actlist = []
	for move in DIR:
		next_pos = mapa.calc_pos(actual_pos, move, wallpass)
		if next_pos != actual_pos and next_pos not in invalid:
			actlist += [next_pos]
	return actlist


def heuristic(pos1: tuple, pos2: tuple) -> float:
	"""
	Calculate the distance between two positions
	:param pos1: actual position
	:param pos2: final position
	:return:
	"""
	return distance(pos1, pos2)


def aStarSearch(start: tuple, end: tuple, mapa: Map, wallpass: bool, invalid: list=None) -> list:
	"""
	Calculate the path between two positions
	:param start: initial position
	:param end: final position
	:param mapa: mapa
	:param wallpass: almost of cases use the power wallpass, but if the objetive is break walls, this power need be enable
	:param invalid: invalid positions
	:return:
	"""
	G = {} #Actual movement cost to each position from the start position
	F = {} #Estimated movement cost of start to end going via this position
	#Initialize starting values
	G[start] = 0 
	F[start] = heuristic(start, end)
	closedVertices = set()
	openVertices = set([start])
	cameFrom = {}
	while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos
		#Check if we have reached the goal
		if current == end:
			#Retrace our route backward
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path[1:]
		#Mark the current vertex as closed
		openVertices.remove(current)
		closedVertices.add(current)
		#Update scores for vertices near the current position
		for neighbour in neighbours(current, mapa, wallpass, invalid):
			if neighbour in closedVertices: 
				continue #We have already processed this node exhaustively
			candidateG = G[current] + 1
			if neighbour not in openVertices:
				openVertices.add(neighbour) #Discovered a new vertex
			elif candidateG >= G[neighbour]:
				continue #This G score is worse than previously found
			#Adopt this G score
			cameFrom[neighbour] = current
			G[neighbour] = candidateG
			H = heuristic(neighbour, end)
			F[neighbour] = G[neighbour] + H
	return []


def breadth_first_search(start: tuple, mapa: Map, wallpass: bool, bomb: Bomb, invalid: list=None) -> list: 
	"""
	Calculate the path between two positions
	:param start: initial position
	:param mapa: mapa
	:param wallpass: almost of cases use the power wallpass, but if the objetive is break walls, this power need be enable
	:param bomb: bomb I want to run
	:param invalid: invalid positions
	:return:
	"""
	openVertices = collections.deque([start])
	closedVertices = set()
	closedVertices.add(start)
	while openVertices:
		current = openVertices.popleft()
		for neighbour in neighbours(current, mapa, wallpass, invalid): 
			if neighbour not in closedVertices: 
				closedVertices.add(neighbour)
				openVertices.append(neighbour)
				if not bomb.in_range(neighbour):
					path = aStarSearch(start, neighbour, mapa, wallpass, invalid)
					if path: return path
	return []
