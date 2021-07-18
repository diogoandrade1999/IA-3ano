from characters import *
from mapa import Map


class MyEnemy:
    def __init__(self, name: str, identifier, pos: tuple):
        self._id = identifier
        self.enemy = None
        if name == 'Balloom':
            self.enemy = Balloom(pos)
        elif name == 'Oneal':
            self.enemy = Oneal(pos)
        elif name == 'Doll':
            self.enemy = Doll(pos)
        elif name == 'Minvo':
            self.enemy = Minvo(pos)
        elif name == 'Kondoria':
            self.enemy = Kondoria(pos)
        elif name == 'Ovapi':
            self.enemy = Ovapi(pos)
        elif name == 'Pass':
            self.enemy = Pass(pos)

    @property
    def id(self):
        return self._id

    @property
    def name(self) -> str:
        return self.enemy._name

    @property
    def pos(self) -> tuple:
        return self.enemy._pos

    @pos.setter
    def pos(self, pos: tuple) -> None:
        if self.enemy.lastpos != self.pos or self.enemy.lastpos is None: self.enemy.lastpos = self.pos
        self.enemy._pos = pos

    def move(self, mapa: Map, bomberman: Bomberman, bombs: list, enemies: dict, moves: int=1) -> list:
        """
        Calculate the next positions
        :param mapa: mapa
        :param bomberman: bomberman
        :param bombs: bombs in the map
        :param enemies: others enemies in the map
        :param moves: how many moves I want
        :return: if collide and enemy
        """
        safety_pos = self.pos
        advance_pos = [self.pos]
        if self.pos != self.enemy.lastpos:
            self.enemy.lastdir = vector2dir(self.pos[0]-self.enemy.lastpos[0], self.pos[1]-self.enemy.lastpos[1])
        for x in range(moves):
            self.enemy.move(mapa, bomberman, bombs, list(enemies.values()))
            if self.pos != advance_pos[-1]: advance_pos.append(self.pos)
        self.pos = safety_pos
        return advance_pos

    def __str__(self) -> str:
        return 'Enemy: ' + str(self.enemy)
