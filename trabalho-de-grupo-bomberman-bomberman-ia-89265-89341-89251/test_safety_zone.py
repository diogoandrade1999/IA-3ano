from mapa import Map
from game import Bomb
from termcolor import colored


class Test:
    def __init__(self):
        self._map = Map(size=(51, 31), empty=True)
        self._map.walls = []
        self._bombs = None
    
    def create_bomb(self):
        x = int(input('x: '))
        y = int(input('y: '))
        r = int(input('r: '))
        self._bombs = [Bomb((x,y), self._map, r)]

    def safety_zone(self):
        """
        Calculate the safety zone
        :return: safety zone
        """
        bomb = self._bombs[-1]
        pos = bomb.pos
        for x in range(pos[0]-bomb.radius-1, pos[0]+bomb.radius+2):
            for y in range(pos[1]-bomb.radius-1, pos[1]+bomb.radius+2):
                p = (x,y)
                if 0 > x or x > self._map.size[0] or 0 > y or y > self._map.size[1]:
                    print(colored((x,y), 'blue'), end=' ')
                elif self._map.is_stone(p):
                    print(colored((x,y), 'white'), end=' ')
                elif p in self._map.walls:
                    print(colored((x,y), 'grey'), end=' ')
                elif bomb.in_range(p):
                    print(colored((x,y), 'red'), end=' ')
                else:
                    print(colored((x,y), 'green'), end=' ')
            print()

test = Test()
test.create_bomb()
test.safety_zone()
