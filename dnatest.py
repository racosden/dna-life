#!/usr/bin/env python

import numpy as np
import random

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
        self.accumulator  = 0
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
            print "Accumulator         =\t%d" % self.accumulator
            print "Energy              =\t%d" % self.energy_level
            print "Current instruction =\t%s" % (current_instruction,)

        self.ip = self.ip + 1

        if "MOV" in current_instruction:
            length = current_instruction[1]
            x, y = self.facing
            while (length > 0):
                self.pos = (self.pos[0] + x, self.pos[1] + y)
                length = length - 1
                # deplete energy by 2 units for each movement
                self.energy_level -= 2

            # if (DEBUG):
            #     print "New Position = (%d, %d)" % self.pos

        if "TUR" in current_instruction:
            try:
                newfacing = DIRLIST[DIRLIST.index(self.facing) + 1]
            except IndexError:
                newfacing = DIRLIST[0]

            self.facing = newfacing

            # deplete energy by 1 unit for each turn
            self.energy_level -= 1

            if (DEBUG):
                print "In TUR!"

        if "TUL" in current_instruction:
            try:
                newfacing = DIRLIST[DIRLIST.index(self.facing) - 1]
            except IndexError:
                newfacing = DIRLIST[-1]

            self.facing = newfacing

            # deplete energy by 1 unit for each turn
            self.energy_level -= 1

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

            # deplete energy by length ** 2
            self.energy_level -= length ** 2

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

            # deplete energy by 1 unit
            self.energy_level -= 1

        if "JGZ" in current_instruction:
            # jump if sense is greater than 0

            destination = current_instruction[1]

            if self.sense > 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "JLZ" in current_instruction:
            # jump if sense is less than 0

            destination = current_instruction[1]

            if self.sense < 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "JEZ" in current_instruction:
            # jump if sense is equal to 0

            destination = current_instruction[1]

            if self.sense == 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "JMP" in current_instruction:
            # unconditional jump

            destination = current_instruction[1]

            # only jump if destination is in memory
            # how should this fail?
            # right now it fails silently by not doing anything
            # perhaps make it jump to ip 0 on failure

            if destination <= len(self.memory):
                self.ip = destination

            # deplete energy by 1 unit
            self.energy_level -= 1

        if "JEQ" in current_instruction:
            # jump if sense memory is equal to the accumulator

            destination = current_instruction[1]

            if self.sense == self.accumulator:
                if destination <= len(self.memory):
                    self.ip = destination

            # deplete energy by 1 unit
            self.energy_level -= 1

        if "STO" in current_instruction:
            # store x in the accumulator

            self.accumulator = current_instruction[1]

            self.energy_level -= 1

        if "CPY" in current_instruction:
            # copy the sense memory to the accumulator (x is ignored)

            self.accumulator = self.sense

            self.energy_level -= 1

        if "ADD" in current_instruction:
            # add x to the accumulator

            addend = current_instruction[1]
            self.accumulator += addend

            self.energy_level -= 1

        if "JAL" in current_instruction:
            # jump to instruction x if accumulator is < 0

            destingation = current_instruction[1]

            if self.accumulator < 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "JAG" in current_instruction:
            # jump to instruction x if accumulator is > 0

            destination = current_instruction[1]

            if self.accumulator > 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "JAE" in current_instruction:
            # jump to instruction x if accumulator is = 0

            destination = current_instruction[1]

            if self.accumulator == 0:
                if destination <= len(self.memory):
                    self.ip = destination

        if "RND" in current_instruction:
            # add random number from 0 to 1 to the accumulator

            addend = random.randint(0, 1)
            self.accumulator += addend

            self.energy_level -= 1

        if "CRD" in current_instruction:
            # set accumulator to 0 then add a random number from 0 to 1 to accumulator

            maxrange = current_instruction[1]

            addend = random.randint(0, maxrange)
            self.accumulator = addend

            self.energy_level -= 1

        if "NOP" in current_instruction:
            # do nothing

            self.energy_level -= 1

def main():
    tick = 1
    dna2 = [ ('CRD', 1),        # 0 pick a random direction
             ('JAE', 4),        # 1 if 0 in accumulator, turn left
             ('TUR', 0),        # 2 turn right
             ('JMP', 5),        # 3 jump to movement
             ('TUL', 0),        # 4 turn left
             ('MOV', 1),        # 5 move forward 1
             ('CRD', 1),        # 6 keep moving?
             ('JAE', 5),        # 7 yes, keep moving
             ('SEN', 1),        # 8 see if there's some food here
             ('JEZ', 16),       # 9 if sense is 0, no food here, otherwise:
             ('STO', 20),       # 10 store 20 in accumulator to check for food
             ('JEQ', 15),       # 11 food worth acc here, jump to X to eat it!
             ('ADD', -1),       # 12 acc -= 1
             ('JAE', 16),       # 13 acc = 0, no food here :(
             ('JMP', 11),       # 13 cycle through the food values
             ('EAT', 0),        # 15 there is food here, eat it
             ('NOP', 0)         # 16 All done
             ]

    ecoli = Organism((10, 10), SOUTH, dna2)

    arena = np.zeros((MAX_X, MAX_Y))
    arena[ecoli.pos] = 1

    arena[10, 11] = 10 # put food directly in front of bcoli

    quit = False

    while quit == False:
        print "Ecoli:"
        ecoli.run(arena)
        rw_string = "Next (tick = " + str(tick) + ") > "
        uinput = raw_input(rw_string)
        tick = tick + 1
        if len(uinput) > 0:
            if uinput.lower()[0] == 'q':
                quit = True

if __name__ == '__main__':
    main()
