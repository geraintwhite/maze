from colours import *
from random import shuffle, randrange
from math import sqrt


class Maze():
    def __init__(self, filename=None, maze=None, wall='#', start='$', end='%', path='.', width=20, height=20):
        '''load maze into object (or generate one if none given)'''

        self.wall, self.start, self.end, self.path = wall, start, end, path
        self.maze = self.read_maze(filename) if filename else maze if maze else self.gen_maze(width, height)
        self.route = []
        self.colours = {
            self.wall: colorStr(self.wall, bg=WHITE, style=CLEAR),
            self.start: colorStr(self.start, bg=BLUE, style=CLEAR),
            self.end: colorStr(self.end, bg=RED, style=CLEAR),
            self.path: colorStr(self.path, bg=YELLOW, style=CLEAR),
        }

    def read_maze(self, filename):
        with open(filename) as f:
            return f.read().splitlines()

    def gen_maze(self, width, height):
        '''generates a random maze'''

        maze = []
        visited = []
        distances = {}
        for y in range(2 * height + 1):
            row = list([self.wall, ' '][y % 2].join([self.wall] * (width + 1)))
            maze.append(row)

        def calc_dist(p1, p2):
            '''calculate distance between two points'''

            return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        def walk(x, y):
            '''traverses maze creating paths'''

            end = True
            visited.append((x, y))
            d = [(-2,0),(0,-2),(0,2),(2,0)]
            shuffle(d)
            for delta in d:
                new_x, new_y = tuple(map(sum, zip((x, y), delta)))
                if (-1 < new_y < len(maze) and -1 < new_x < len(maze[0])
                    and (new_x, new_y) not in visited):

                    maze[int((new_y + y)/2)][int((new_x + x)/2)] = ' '
                    walk(new_x, new_y)
                    end = False
            if end: distances[calc_dist(start, (x, y))] = (x, y)

        start = (2 * randrange(1, width+1)-1, 2 * randrange(1, height+1)-1)
        maze[start[1]][start[0]] = self.start
        walk(*start)

        end = distances[max(distances.keys())]
        maze[end[1]][end[0]] = self.end

        return maze

    def solve(self):
        self.route = self.explore(self.find_char(self.start)[0], [])
        return self.route

    def reset(self):
        self.route = []

    def explore(self, pos, visited):
        '''visit each of the free spots around pos in the maze'''

        visited.append(pos)
        if self.char(pos) is self.end:
            return []
        else:
            for delta in ((-1,0),(0,-1),(0,1),(1,0)):
                new_pos = tuple(map(sum, zip(pos, delta)))
                if new_pos not in visited and self.char(new_pos) is not self.wall:
                    route = self.explore(new_pos, visited)
                    if route is not None:
                        if self.char(new_pos) is not self.end: route.append(new_pos)
                        return route

    def char(self, pos):
        return self.maze[pos[1]][pos[0]]

    def find_char(self, char):
        '''return a list of positions of char in self.maze'''

        pos = []
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if col == char:
                    pos.append((x,y))
        return pos

        # return [(x, y) for y, row in enumerate(self.maze) for x, col in enumerate(row) if col == char]

    def __str__(self):
        '''outputs the maze with colours specified and the route if solved'''

        out = []
        for y, row in enumerate(self.maze):
            line = ''
            for x, col in enumerate(row):
                char = self.path if self.route and (x, y) in self.route else row[x]
                try: char = self.colours[char]
                except KeyError: pass
                line += char * 2
            out.append(line)
        return '\n'.join(out)


if __name__ == '__main__':
    # maze = Maze(filename='maze')
    # maze.solve()
    # print(maze)
    maze2 = Maze()
    maze2.solve()
    print(maze2)
