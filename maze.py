from colours import *


class Maze():
    def __init__(self, filename=None, maze=None, wall='#', start='$', end='%', path='.'):
        '''load maze into object (or generate one if none given)'''

        self.wall, self.start, self.end, self.path = wall, start, end, path
        self.maze = self.read_maze(filename) if filename else maze if maze else self.gen_maze()
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

    def gen_maze(self):
        pass

    def solve(self):
        self.route = self.explore(self.find_char(self.start)[0])
        return self.route

    def reset(self):
        self.route = []

    def explore(self, pos, visited=[]):
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
    maze = Maze(filename='maze')
    print(maze)
    maze.solve()
    print(maze)
    maze.reset()
    print(maze)
