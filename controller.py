#!/usr/bin/env python

import organism
import arena

class Controller(object):
    def __init__(self, organism_list = None, arena = None):
        "controls the whole game"
        self.organism_list = organism_list
        self.arena = arena

    def tick(self):
        for organism in self.organism_list:
            result = organism.run()
            self.update_arena(result)

    def update_arena(self, changes):
        arena.update(changes)

def main():
    maxx = maxy = 10

    board = arena.Arena(maxx, maxy)

    board.update( ((3, 5), 20) )

    dna = [("MOV", 1),          # 0 Move one ahead
           ("TUR", 1),          # 1 Turn right
           ("SEN", 1),          # 2 Sense ahead
           ("JGZ", 6),          # 3 Found food!
           ("MOV", 1),          # 4 Move one ahead
           ("JMP", 0),          # 5 Repeat
           ("EAT", 1)           # 6 Eat the food found
           ]

    bacterium = organism.Organism((5, 5), organism.SOUTH, dna)

    orglist = [bacterium]

    retval = None

    quit = False
    tick = 0

    while not quit:
        for current_org in orglist:
            retval = current_org.run(board.arena)
            if retval:
                board.update( (retval[0], retval[1]) )
        prompt = "(tick: %d)> " % tick
        quit = raw_input(prompt)
        tick += 1


if __name__ == '__main__':
    main()
