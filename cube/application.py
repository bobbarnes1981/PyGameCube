"""Application module"""

import logging
import time
import pygame

class Rubik():
    def __init__(self):
        self.sides = {
            'f': ['b','b','b','b','b','b','b','b','b'],
            'r': ['o','o','o','o','o','o','o','o','o'],
            'u': ['w','w','w','w','w','w','w','w','w'],
            'l': ['r','r','r','r','r','r','r','r','r'],
            'd': ['y','y','y','y','y','y','y','y','y'],
            'b': ['g','g','g','g','g','g','g','g','g']
        }
    def get_side(self, side):
        return self.sides[side]
    def move(self, move):
        print(move)
        self.move_cw(move)
    def move_cw(self, side):
        # nothing fancy
        updated_side = ['','','','','','','','','']
        updated_side[self.get_flat_coord(0,0)] = self.sides[side][self.get_flat_coord(0,2)]
        updated_side[self.get_flat_coord(1,0)] = self.sides[side][self.get_flat_coord(0,1)]
        updated_side[self.get_flat_coord(2,0)] = self.sides[side][self.get_flat_coord(0,0)]
        updated_side[self.get_flat_coord(0,1)] = self.sides[side][self.get_flat_coord(1,2)]
        updated_side[self.get_flat_coord(1,1)] = self.sides[side][self.get_flat_coord(1,1)]
        updated_side[self.get_flat_coord(2,1)] = self.sides[side][self.get_flat_coord(1,0)]
        updated_side[self.get_flat_coord(0,2)] = self.sides[side][self.get_flat_coord(2,2)]
        updated_side[self.get_flat_coord(1,2)] = self.sides[side][self.get_flat_coord(2,1)]
        updated_side[self.get_flat_coord(2,2)] = self.sides[side][self.get_flat_coord(2,0)]
        self.sides[side] = updated_side
        if side == 'f':
            self.move_cw_edge(['l','u','r','d'], ['r','b','l','t'])
        elif side == 'r':
            self.move_cw_edge(['f','u','b','d'], ['r','r','l','r'])
        elif side == 'u':
            self.move_cw_edge(['l','b','r','f'], ['t','t','t','t'])
        elif side == 'l':
            self.move_cw_edge(['b','u','f','d'], ['r','l','l','l'])
        elif side == 'd':
            self.move_cw_edge(['l','f','r','b'], ['b','b','b','b'])
        elif side == 'b':
            self.move_cw_edge(['r','u','l','d'], ['r','t','l','b'])
        else:
            pass
    def move_cw_edge(self, edges, coords):
        coordinates ={
            'r': (self.get_flat_coord(2,2),self.get_flat_coord(2,1),self.get_flat_coord(2,0)),
            'b': (self.get_flat_coord(0,2),self.get_flat_coord(1,2),self.get_flat_coord(2,2)),
            'l': (self.get_flat_coord(0,0),self.get_flat_coord(0,1),self.get_flat_coord(0,2)),
            't': (self.get_flat_coord(2,0),self.get_flat_coord(1,0),self.get_flat_coord(0,0)),
        }
        tmp = ['','','','','','','','','']

        tmp[coordinates[coords[0]][0]] = self.sides[edges[0]][coordinates[coords[0]][0]]
        tmp[coordinates[coords[0]][1]] = self.sides[edges[0]][coordinates[coords[0]][1]]
        tmp[coordinates[coords[0]][2]] = self.sides[edges[0]][coordinates[coords[0]][2]]

        self.sides[edges[0]][coordinates[coords[0]][0]] = self.sides[edges[3]][coordinates[coords[3]][0]]
        self.sides[edges[0]][coordinates[coords[0]][1]] = self.sides[edges[3]][coordinates[coords[3]][1]]
        self.sides[edges[0]][coordinates[coords[0]][2]] = self.sides[edges[3]][coordinates[coords[3]][2]]

        self.sides[edges[3]][coordinates[coords[3]][0]] = self.sides[edges[2]][coordinates[coords[2]][0]]
        self.sides[edges[3]][coordinates[coords[3]][1]] = self.sides[edges[2]][coordinates[coords[2]][1]]
        self.sides[edges[3]][coordinates[coords[3]][2]] = self.sides[edges[2]][coordinates[coords[2]][2]]

        self.sides[edges[2]][coordinates[coords[2]][0]] = self.sides[edges[1]][coordinates[coords[1]][0]]
        self.sides[edges[2]][coordinates[coords[2]][1]] = self.sides[edges[1]][coordinates[coords[1]][1]]
        self.sides[edges[2]][coordinates[coords[2]][2]] = self.sides[edges[1]][coordinates[coords[1]][2]]

        self.sides[edges[1]][coordinates[coords[1]][0]] = tmp[coordinates[coords[0]][0]]
        self.sides[edges[1]][coordinates[coords[1]][1]] = tmp[coordinates[coords[0]][1]]
        self.sides[edges[1]][coordinates[coords[1]][2]] = tmp[coordinates[coords[0]][2]]
        
    def get_flat_coord(self, x, y):
        return x + (y * 3)

class App():
    """Application class"""
    def __init__(self, delay: float) -> None:
        self._delay = delay

        self._running = True
        self._display_surf = None
        self._width = 640
        self._height = 480
        self._size = (self._width, self._height)
        self._time = time.time()
        self._counter = 0
        self._complete = False
        self.font_s = None
        self.font_l = None

        self.rubik = Rubik()
    def on_init(self) -> None:
        """On init."""
        pygame.init()
        pygame.display.set_caption("Title")
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #self.font = pygame.font.SysFont('courier.ttf', 72)
        font_name = pygame.font.get_default_font()
        logging.info("System font: %s", font_name)
        self.font_s = pygame.font.SysFont(None, 22)
        self.font_l = pygame.font.SysFont(None, 33)
        return True
    def on_event(self, event: pygame.event.Event) -> None:
        """On event."""
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._running = False
            elif event.key == pygame.K_f:
                self.rubik.move('f')
            elif event.key == pygame.K_r:
                self.rubik.move('r')
            elif event.key == pygame.K_u:
                self.rubik.move('u')
            elif event.key == pygame.K_l:
                self.rubik.move('l')
            elif event.key == pygame.K_d:
                self.rubik.move('d')
            elif event.key == pygame.K_b:
                self.rubik.move('b')
        else:
            logging.debug(event)
    def on_loop(self, elapsed: float) -> None:
        """On loop."""
        self._counter+=elapsed
        if self._counter > self._delay:
            logging.info("tick")
            self._counter = 0
            if self._complete is False:
                pass
    def on_render(self) -> None:
        """On render."""
        self._display_surf.fill((0,0,0))
        self.render_side('f')
        self.render_side('r')
        self.render_side('u')
        self.render_side('l')
        self.render_side('d')
        self.render_side('b')
        pygame.display.update()
    def render_side(self, s):
        side = self.rubik.get_side(s)
        scale= 50
        gap = 2
        offsets = {
            'f': [1, 1],
            'r': [2, 1],
            'u': [1, 0],
            'l': [0, 1],
            'd': [1, 2],
            'b': [3, 1],
        }
        colours = {
            'b': (0,0,255),
            'o': (255,165,0),
            'w': (255,255,255),
            'r': (255,0,0),
            'y': (255,255,0),
            'g': (0,255,0)
        }
        offset = offsets[s]
        for y in range(0, 3):
            for x in range(0, 3):
                cell = side[x + (y * 3)]
                left = offset[0]*scale*3
                top = offset[1]*scale*3
                r = pygame.Rect(left+(x*scale),top+(y*scale), scale-gap, scale-gap)
                pygame.draw.rect(self._display_surf, colours[cell], r)
    def on_cleanup(self) -> None:
        """On cleanup."""
        pygame.quit()
    def on_execute(self) -> None:
        """On execute."""
        if self.on_init() is False:
            self._running = False
        while self._running:
            current = time.time()
            elapsed = current - self._time
            self._time = current
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(elapsed)
            self.on_render()
        self.on_cleanup()
