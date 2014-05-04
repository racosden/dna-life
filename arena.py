#!/usr/bin/env python

import numpy as np

class Arena(object):
    def __init__(self, max_x = 10, max_y = 10):
        """ simulation arena
            arena.arena(max_x, max_y)
            do not alter max_x and max_y
        """
        self.max_x = max_x
        self.max_y = max_y
        self.arena = np.zeros( (self.max_x, self.max_y) )

    def update(self, changes = None):
        if changes:
            self.arena[changes[0]] = changes[1]

def main():
    MAX_X = 10
    MAX_Y = 10

    changeloc = (5, 5)
    changevalue = 10

    changes = (changeloc, changevalue)

    arena = Arena(MAX_X, MAX_Y)

    print "\nArena at %d, %d is %d.\n" % (changes[0][0], changes[0][1], arena.arena[changes[0]])

    arena.update(changes)

    print "\nArena at %d, %d is %d.\n" % (changes[0][0], changes[0][1], arena.arena[changes[0]])


if __name__ == '__main__':
    main()
