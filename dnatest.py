#!/usr/bin/env python

DEBUG = True

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
        self.acc          = []
    def run(self):
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
            print "Current instruction =\t%s" % current_instruction

        self.ip = self.ip + 1

        if "MOV" in current_instruction:
            length = int(current_instruction[len("MOV") + 1:])
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


def main():
    tick = 1
    dna1 = ["MOV 1", "TUR 1", "MOV 1", "TUL 1"]
    dna2 = ["MOV 2", "TUR 1", "TUR 1", "MOV 1", "TUL 1"]
    ecoli = Organism((0,0), EAST, dna1)
    bcoli = Organism((10, 10), SOUTH, dna2)

    for i in xrange(20):
        print "\nTick\t\t    =\t%d" % tick
        tick = tick + 1
        # print "Ecoli:"
        # ecoli.run()
        print "Bcoli:"
        bcoli.run()

if __name__ == '__main__':
    main()
