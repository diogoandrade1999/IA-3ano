from enemy import MyEnemy
from game import Bomb, LEVEL_POWERUPS, LEVEL_ENEMIES
from mapa import Map
from characters import Bomberman, distance, DIR
from search import aStarSearch, breadth_first_search
from enum import IntEnum
from consts import Powerups
import logging


logging.basicConfig(level=logging.WARNING, format='%(message)s')


POWER_UP_DONT_NEED = [Powerups.Bombs, Powerups.Bombpass, Powerups.Wallpass]


def inverse_move(move: str) -> str:
    """
    Calculate the inverse movement
    :param move: actual movement
    :return: the next movement
    """
    key = ''
    if move == 'w':
        key = 's'
    elif move == 's':
        key = 'w'
    elif move == 'a':
        key = 'd'
    elif move == 'd':
        key = 'a'
    return key


def calc_move(pos1: tuple, pos2: tuple) -> str:
    """
    Calculate the next movement from intial position to final position
    :param pos1: initial position
    :param pos2: final position
    :return: the next movement
    """
    move = ''
    if pos1[0] < pos2[0]:
        move = 'd'
    elif pos1[0] > pos2[0]:
        move = 'a'
    elif pos1[1] < pos2[1]:
        move = 's'
    elif pos1[1] > pos2[1]:
        move = 'w'
    return move


class State(IntEnum):
    WAIT = 0
    BOMB = 1
    EXIT = 2
    WALL = 3
    POWER_UP = 4
    ENEMY = 5
    BUG = 6


class Player:
    def __init__(self, mapa: Map):
        self._map = mapa
        self._map.level = 0
        self._bomberman = None
        self._state = State.WAIT
        self._bombs = None
        self._list_pos = None
        self._list_pos_old = None
        self._next_move = ''
        self._wall = None
        self._enemies = None
        self._enemy = (None, -1, -1)
        self._power_ups = None
        self._power_up = False
        self._exit = None
        self._step = 0
        self._time_out = 0
        self._safety = True
        self._debug = None

    def state(self, state: list) -> None:
        """
        Update all attributes
        :param state: state of the map
        :return:
        """
        # When we level up or start the game
        if self._map.level != state['level']:
            logging.info('------- LEVEL ' + str(state['level']) + ' -------')
            self._map.level = state['level']
            if state['level'] == 1:
                self._bomberman = Bomberman(tuple(state['bomberman']))
            self._bombs = []
            self._list_pos = []
            self._list_pos_old = [tuple(state['bomberman'])]
            self._next_move = ''
            self._wall = ()
            self._enemies = {}
            self._power_up = False
            if LEVEL_POWERUPS[self._map.level] in POWER_UP_DONT_NEED or \
            (LEVEL_POWERUPS[self._map.level] == Powerups.Wallpass and self._bomberman.wallpass) or \
            (LEVEL_POWERUPS[self._map.level] == Powerups.Detonator and Powerups.Detonator in self._bomberman.powers) or \
            (LEVEL_POWERUPS[self._map.level] == Powerups.Flamepass and self._bomberman.flamepass):
                self._power_up = True
            self._power_ups = []
            self._enemy = (None, -1, -1)
            self._exit = None
            self._state = State.WAIT
            for e in state['enemies']:
                self._enemies[str(e['id'])] = MyEnemy(e['name'], e['id'], tuple(e['pos']))
                logging.info('Alive => ' + str(self._enemies[e['id']]))

        # When we die
        if self._bomberman.lives != state['lives']:
            logging.info('LIVES: ' + str(state['lives']))
            logging.info(f'Debug! => {self._debug[0]} | {self._debug[1]} | {self._debug[2]} | {self._bomberman.pos}')
            self._bomberman.kill()
            self._list_pos = []
            self._list_pos_old = [tuple(state['bomberman'])]
            self._next_move = ''
            self._enemy = (None, -1, -1)
            self._wall = []
            self._state = State.WAIT

        # When pick the power up
        if len(self._power_ups) > len(state['powerups']):
            logging.info('PICK POWER UP => ' + str(self._power_ups[-1][1]))
            self._power_up = True
            self._power_ups.pop(-1)
            self._bomberman.powerup(LEVEL_POWERUPS[self._map.level])
        # When find one power up
        elif len(self._power_ups) < len(state['powerups']):
            logging.info('FIND POWER UP => ' + str(state['powerups'][-1][1]))
            self._power_ups.append([tuple(state['powerups'][0][0]), state['powerups'][0][1]])

        # Update bombs
        self._bombs = []
        for bomb in state['bombs']:
            self._bombs.append(Bomb(tuple(bomb[0]), self._map, bomb[2]))

        # Update walls
        self._map.walls = state['walls']
        if self._wall not in self._map.walls:
            self._wall = []

        # Find exit
        if self._exit is None and state['exit']:
            logging.info('FIND EXIT => ' + str(state['exit']))
            self._exit = tuple(state['exit'])

        # Update step
        self._step = state['step']

        # Update time out
        self._time_out = state['timeout']

        # Update bomber man position
        self._bomberman.pos = tuple(state['bomberman'])

        # When enemies die
        if len(state['enemies']) != len(self._enemies):
            self._enemy = (None, -1, -1)
            list_ids = []
            for enemy in state['enemies']:
                list_ids.append(enemy['id'])
            ids = list(set(self._enemies.keys()) - set(list_ids))
            for identifier in ids:
                logging.info('DEAD  => ' + str(self._enemies[identifier]))
                del self._enemies[identifier]
        # Update enemies positions
        for enemy in state['enemies']:
            self._enemies[enemy['id']].pos = tuple(enemy['pos'])

    def get_key(self) -> str:
        """
        Calculate the key to next move
        :return: Give the key ('wsad' or 'AB' or '')
        """
        old_state = self._state
        # If exist a bomb in map
        if self._bombs:
            self._state = State.BOMB
            # If there is no move list for the safe zone
            if not self._list_pos and not self._safety:
                self._list_pos = self.run_explosion()
                self._safety = True
            # Consume the list
            if self._list_pos:
                self._next_move = calc_move(self._bomberman.pos, self._list_pos.pop(0))
            # In safety place
            else: self._next_move = 'A'
        else:
            # Power up wallpass are deactivated
            wallpass = False # self._bomberman.wallpass
            enemy = None
            # If exist a power up exposed in map
            if self._power_ups and not self._power_up:
                self._state = State.POWER_UP
                pos = self._power_ups[-1][0]
            # If all enemies are dead
            elif not self._enemies:
                # Go to the exit
                if self._exit is not None and (self._power_up \
                    or self._step > self._time_out - 200 or self._map.level == len(LEVEL_ENEMIES)):
                    self._state = State.EXIT
                    pos = self._exit
                # Find the exit or power up
                else:
                    self._state = State.WALL
                    if not self._wall:
                        self._wall = sorted(self._map.walls, key=lambda pos:distance(self._bomberman.pos, pos))[0]
                    pos = self._wall
                    wallpass = True
            # If exist enemies a live
            else:
                # Avoids looping behind enemy
                if self._enemy[1] > 5 or self._enemy[2] > 150:
                    logging.info(f'Bug   => {str(self._enemy[0])} {self._enemy[1]} {self._enemy[2]}')
                    self._state = State.BUG
                    self._wall = sorted(self._map.walls, key=lambda pos:distance(self._enemy[0].pos, pos))[0]
                    pos = self._wall
                    wallpass = True
                else:
                    self._state = State.ENEMY
                    if self._enemy[0] is None:
                        enemy = sorted(list(self._enemies.values()), key=lambda enemy:distance(self._bomberman.pos, enemy.pos))[0]
                        self._enemy = (enemy, 0, 0)
                    self._enemy = (self._enemy[0], self._enemy[1], self._enemy[2]+1)
                    pos = self._enemy[0].pos
            # Go to the position
            if self._state != old_state: self._list_pos = []
            self.calc_next_move(pos, wallpass, self._enemy[0])
        if self._state != old_state: logging.debug('State => ' + old_state.name)
        # Save last position of bomberman
        if self._list_pos_old[-1] != self._bomberman.pos: self._list_pos_old.append(self._bomberman.pos)
        return self._next_move

    def calc_next_move(self, pos: tuple, wallpass: bool, enemy: MyEnemy) -> None:
        """
        Calculate the next move go to the objective
        :param pos: final position
        :param wallpass: almost of cases use the power wallpass, but if the objetive is break walls, this power need be enable
        :param enemy: enemy I want dead
        :return:
        """
        # If I don't have a path
        if not self._list_pos:
            invalid = None
            if self._state == State.BUG: invalid = [p for e in self._enemies.values() for p in e.move(self._map, self._bomberman, self._bombs, self._enemies, 2)]
            # Put exit to invalid positions if I don't have the power up
            if self._exit is not None and self._state in [3, 4] and not self._power_up:
                if invalid is not None: invalid += [self._exit]
                else: invalid = [self._exit]
            # Calc for Ballom enemy the next positions
            if enemy is not None and enemy.name == 'Balloom':
                moves = int(distance(self._bomberman.pos, pos)+10)
                advanced_pos = enemy.move(self._map, self._bomberman, self._bombs, self._enemies, moves)
                if self._bomberman.pos in advanced_pos: pos = enemy.pos
                else: pos = advanced_pos[-1]
            # Find the path
            self._list_pos = aStarSearch(self._bomberman.pos, pos, self._map, wallpass, invalid)
            if not self._list_pos:
                if self._state == State.WALL:
                    if len(self._map.walls) > 1:
                        pos = sorted(self._map.walls, key=lambda pos:distance(self._enemy[0].pos, pos))[1]
                self._list_pos = aStarSearch(self._bomberman.pos, pos, self._map, True, invalid)
                if not self._list_pos: logging.info('I have a problem!')
            # If I want kill enemies, I don't do all the path
            if enemy is not None and self._list_pos:
                if enemy.name == 'Balloom': size = int(len(self._list_pos)/2)
                else: size = int(2*len(self._list_pos)/3)
                if size == 0: size = 1
                self._list_pos = self._list_pos[:size]
        # Calc next move
        next_pos = self._bomberman.pos
        self._next_move = ''
        if self._list_pos:
            self._debug = (self._bomberman.pos, [x for x in self._list_pos], 3)
            next_pos = self._list_pos.pop(0)
            self._next_move = calc_move(self._bomberman.pos, next_pos)
        # If need break a wall to pass or kill enemies
        collide = self.collide_enemy(self._bomberman.pos, next_pos)
        if (self._next_move != '' and next_pos == self._bomberman.pos) or \
        next_pos in self._map.walls or collide:
            if collide: self._enemy = (self._enemy[0], self._enemy[1]+1, self._enemy[2])
            if self._state == State.BUG: self._enemy = (self._enemy[0], 0, 0)
            self._state = State.BOMB
            self._safety = False
            self._next_move = 'B'
            self._wall = ()
            self._list_pos = []

    def collide_enemy(self, pos: tuple, next_pos: tuple) -> bool:
        """
        Check for enemies from 2 positions away, 1 back and 2 for the sides
        :param pos: initial position
        :param next_pos: next position I want to go
        :return: if collide and enemy
        """
        possible_pos = [pos, next_pos]
        move = calc_move(pos, next_pos)
        for p in [pos, next_pos]:
            for m in DIR:
                calc_pos = self._map.calc_pos(p, m)
                if calc_pos != p: possible_pos.append(calc_pos)
        for enemy in self._enemies.values():
            if enemy.pos in possible_pos:
                return True
        return False

    def run_explosion(self) -> list:
        """
        Calculate the moves to make for bomber man run explosion
        :return: list of moves
        """
        list_pos = []
        invalid = [p for e in self._enemies.values() for p in e.move(self._map, self._bomberman, self._bombs, self._enemies, 2)]
        if self._exit is not None and len(self._enemies) <= 1: invalid += [self._exit]
        # Calc of the nearest safe position and the path to go there
        list_pos = breadth_first_search(self._bomberman.pos, self._map, self._bomberman.wallpass, self._bombs[-1], invalid)
        if list_pos: self._debug = (self._bombs[-1].pos, [x for x in list_pos], 1)
        # If don't find a path, he will reverse your steps
        if not list_pos:
            count = -2
            while True:
                if not self._list_pos_old or len(self._list_pos_old) < abs(count): break
                pos = self._list_pos_old[count]
                if not self._bombs[-1].in_range(pos):
                    list_pos = aStarSearch(self._bomberman.pos, pos, self._map, self._bomberman.wallpass)
                    if list_pos: break
                count -= 1
            if list_pos: logging.debug(f'Reverse Steps! => {self._bombs[-1].pos} | {list_pos}')
            else: logging.info('I killed myself!')
            self._debug = (self._bombs[-1].pos, [x for x in list_pos], 2)
        return list_pos
