#!/usr/bin/env python

import numpy as np

DEBUG = True
BOUNDARIES = True

MAX_X = MAX_Y = 1000

EMPTY_SPACE = 0
FOOD_SPACE = range(1, 21)

NORTH = (0, -1)
EAST  = (1, 0)
SOUTH = (0, 1)
WEST  = (-1, 0)

DIRLIST = [NORTH, EAST, SOUTH, WEST]

class Organism(object):
    def __init__(self, position = (0, 0), facing = EAST, memory = ["NOP 1"]):
        "a single organism"
        self.pos          = position
        self.facing       = facing
        self.ip           = 0
        self.energy_level = 100
        self.age          = 0
        self.memory       = memory
        self.sense        = 0
        self.acc          = []
    def run(self, arena):
        current_instruction = ""

        try:
            current_instruction = self.memory[self.ip]
        except IndexError:
            self.ip = 0
            current_instruction = self.memory[self.ip]

        if (DEBUG):
            if self.facing == DIRLIST[0]:
                facing_text = "NORTH"
            if self.facing == DIRLIST[1]:
                facing_text = "EAST"
            if self.facing == DIRLIST[2]:
                facing_text = "SOUTH"
            if self.facing == DIRLIST[3]:
                facing_text = "WEST"

            print "Current ip          =\t%d" % self.ip
            print "Current position    =\t(%d, %d)" % self.pos
            print "Facing              =\t%s" % facing_text
            print "Sense memory        =\t%d" % self.sense
            print "Energy              =\t%d" % self.energy_level
            print "Current instruction =\t%s" % (current_instruction,)

        self.ip = self.ip + 1

        if "MOV" in current_instruction:
            print current_instruction
            length = current_instruction[1]
            print length
            x, y = self.facing
            while (length > 0):
                self.pos = (self.pos[0] + x, self.pos[1] + y)
                length = length - 1

            # if (DEBUG):
            #     print "New Position = (%d, %d)" % self.pos

        if "TUR" in current_instruction:
            try:
                newfacing = DIRLIST[DIRLIST.index(self.facing) + 1]
            except IndexError:
                newfacing = DIRLIST[0]

            self.facing = newfacing

        if "TUL" in current_instruction:
            try:
                newfacing = DIRLIST[DIRLIST.index(self.facing) - 1]
            except IndexError:
                newfacing = DIRLIST[-1]

            self.facing = newfacing

        if "SEN" in current_instruction:
            start_pos = self.pos
            end_pos = self.pos

            length = current_instruction[1]

            if length > 0:
                if self.facing == NORTH:
                    end_pos = (self.pos[0], self.pos[1] - length)
                    if BOUNDARIES:
                        if end_pos[1] < 0:
                            end_pos[1] = 0
                elif self.facing == SOUTH:
                    end_pos = (self.pos[0], self.pos[1] + length)
                    if BOUNDARIES:
                        if end_pos[1] > MAX_Y:
                            end_pos[1] = MAX_Y
                elif self.facing == EAST:
                    end_pos = (self.pos[0] + length, self.pos[1])
                    if BOUNDARIES:
                        if end_pos[0] > MAX_X:
                            end_pos[1] = MAX_X
                elif self.facing == WEST:
                    end_pos = (self.pos[0] - length, self.pos[1])
                    if BOUNDARIES:
                        if end_pos[0] < 0:
                            end_pos[0] = 0



            # start_pos now contains the current position of the organism
            # end_pos contains the end of the 'sense line'

            self.sense = arena[end_pos]

        if "EAT" in current_instruction:
            x, y = self.facing

            # get the value of the space in front of the organism

            target_pos = (self.pos[0] + x, self.pos[1] + y)
            target = arena[target_pos]

            if target in FOOD_SPACE:
                # food is in front of the organism, so eat it.
                self.energy_level += target
                # once food is eaten, it's gone
                arena[target_pos] = EMPTY_SPACE


def main():
    tick = 1
    # dna1 = [('MOV' 1), ('TUR' 1), ('MOV' 1), ('TUL' 1)]
    # dna2 = [('MOV', 2), ('TUR', 1), ('TUR', 1), ('MOV', 1), ('TUL', 1)]
    dna2 = [('SEN', 1), ('EAT', 1), ('EAT', 1)]
    #ecoli = Organism((0,0), EAST, dna1)
    bcoli = Organism((10, 10), SOUTH, dna2)

    arena = np.zeros((MAX_X, MAX_Y))
    arena[bcoli.pos] = 1

    arena[10, 11] = 10 # put food directly in front of bcoli

    for i in xrange( len( dna2 ) + 1 ):
        print "\nTick\t\t    =\t%d" % tick
        tick = tick + 1
        # print "Ecoli:"
        # ecoli.run()
        print "Bcoli:"
        bcoli.run(arena)
        raw_input("Next > ")

if __name__ == '__main__':
    main()
