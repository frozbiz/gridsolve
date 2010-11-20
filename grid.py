
class grid:
    # Class constants
    (HORIZ,VERT) = range(2)
    def __init__(self, filename=None, *parse_args, **kargs):
        self.links = {}
        self.extraction = []
        if (filename):
            self.parse(filename, *parse_args, **kargs)

    def parse(self, filename, special_char="*", min_word_len=2):
        vert_in_prog = {}
        horiz_dict = {}
        vert_dict = {}
        links = {}
        extraction = []
        with open(filename) as infile:
            # Scroll through the file to figure out how the layout looks
            for row,line in enumerate(infile):
                horiz_in_prog = ()
                for col,c in enumerate(line):
                    if (c.isspace()):
                        # Clean up any vertical start that ended here
                        if (col in vert_in_prog):
                            del vert_in_prog[col]
                        # Clean up any horizontal start that ended here
                        horiz_in_prog = ()
                        continue

                    if not horiz_in_prog:
                        horiz_in_prog = (row,col)

                    # The starting point of this vertical run (default to here)
                    vert_start = vert_in_prog.setdefault(col,row)
                    vert_pos = (vert_start,col)
                    # Add in the intersections and the indices thereof
                    vert_dict.setdefault(vert_pos,[]).append(horiz_in_prog)
                    horiz_dict.setdefault(horiz_in_prog,[]).append(vert_pos)
                    if (c == special_char):
                        extraction.append((row,col))
                # do some record keeping if the line ended before it got to all
                # the verticals in progress
                for key in vert_in_prog.keys():
                    if (key > col):
                        del vert_in_prog[key]

        # Record the extraction
        self.extraction = extraction

        # Now prune the entries that are too short.
        for (key,val) in vert_dict.items():
            if (len(val) < min_word_len):
                del vert_dict[key]

        for (key,val) in horiz_dict.items():
            if (len(val) < min_word_len):
                del horiz_dict[key]

        # Now prune references to items that were just pruned, and insert them
        # into the final dictonary
        for pos,val in horiz_dict.iteritems():
            link_table = []
            for ix in xrange(len(val)):
                if val[ix] not in vert_dict:
                    val[ix] = None
                    link_table.append(None)
                else:
                    link_table.append(((grid.VERT,val[ix]),pos[0]-val[ix][0]+1))
            key = (grid.HORIZ, pos)
            links[key] = link_table

        for pos,val in vert_dict.iteritems():
            link_table = []
            for ix in xrange(len(val)):
                if val[ix] not in horiz_dict:
                    val[ix] = None
                    link_table.append(None)
                else:
                    link_table.append(((grid.HORIZ,val[ix]),pos[1]-val[ix][1]+1))

            key = (grid.VERT, pos)
            links[key] = link_table

        self.links = links

        
        

FILE = "grid_simple.txt"

if __name__ == "__main__":
    g = grid(FILE)

    
