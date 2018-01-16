# Crossword puzzle solver
from time import time
WILDCARD = "*"

def count_dict(keys):
    d = {}
    for key in keys:
        d[key] = d.get(key,0) + 1
    return d

def partial_match(x,filt):
    if x == (WILDCARD,):
        return True
    
    if len(x) < len(filt):
        return False

    for i in range(len(filt)):
        cf = filt[i]
        cx = x[i]
        if (cf != cx and cf != WILDCARD and cx != WILDCARD):
            return False

    return True

def transliterate(cands, dictMap):
    l = []
    for word_list in cands:
        d = {}
        for word, num_occ in word_list.iteritems():
            trans = []
            for c in word:
                c = dictMap.get(c,c)
                if len(c) > 1:
                    print "No mapping for:", c
                trans.append(c)
            d[tuple(trans)] = num_occ
        l.append(d)
    return l


def solve(pos, unsolved_set, ans, cands, link_list):
    l = len(link_list[pos]) - 1
    consts = ans[pos]
    possibilities = [x for (x,y) in cands[l].iteritems() if y > 0 and partial_match(x, consts)]

    global low_water_mark
    if (len(unsolved_set) == 0 or not possibilities):
        lwm = len(unsolved_set) + (0 if possibilities else 1)
        if (lwm < low_water_mark):
            low_water_mark = lwm
            if (lwm < 25):
                global g
                g.printSolution(ans)
#    print consts

    for word in possibilities:
##        print word
        # Make a deep copy of all the inputs so that we don't polute them with the interim results.
        temp_ans = dict((k,list(v)) for (k,v) in ans.iteritems())
##        print temp_ans
        temp_cands = [dict(cand) for cand in cands]
        # Mark this word as used
        temp_cands[l][word] -= 1
        next_positions = set()
        # If it's not all wildcards
        if (word != (WILDCARD,)):
            # Insert it in the answer list
            temp_ans[pos] = list(word)
            # And in all the places it links
            for ix in xrange(len(word)):
                link = link_list[pos][ix]
                # if this word has no corresponding link for this letter, continue
                if not link:
                    continue
                c = word[ix]
                (p,z) = link
                # Adjust the numbers to be zero indexed
                z -= 1

                # Add the intersections to the list of next prospective candidates
                if p in unsolved_set:
                    next_positions.add(p)

                cCurr = temp_ans[p][z]
                if cCurr != WILDCARD:
                    if (cCurr != c):
                        print "Whoops! Overwriting", cCurr, "with", c, "at", p, ":", z
                    else:
                        continue

                temp_ans[p][z] = c

        if (unsolved_set):
            if (next_positions):
                p = next_positions.pop()
            else:
                p = set(unsolved_set).pop()

            for sol in solve(p, unsolved_set.difference((p,)), temp_ans, temp_cands, link_list):
                yield sol
        else:
            yield temp_ans

SIMPLE_TEST, END_TO_END_TEST, RIVALRIES, PAYROLL, TREASURE_CHEST = range(5)

mode = TREASURE_CHEST
xlate = True
if (mode == SIMPLE_TEST):
    candidates = ((),
                  (("ALPHA", "ALPHA"),
                   ("CHI", "RHO"),
                   ("CHI", "N"),
                   ("QOF", "E"),
                   ("QOF", "N"),
                   ("D", "BET"),
                   ("E", "MU"),
                   ("HE", "L"),
                   ("HE", "SHIN"),
                   ("MU", "D"),
                   ("MU", "V"),
                   ("MU", "L"),
                   ("NU", "B"),
                   ("NU", "R"),
                   ("NU", "Z"),
                   ("PI", "RHO"),
                   ("RHO", "P"),
                   ("RHO", "Z"),
                   ("XI", "PHI"),
                   ("SHIN", "E"),
                   ("TAU", "L"),
                   ("TAU", "R"),
                   ("YOD", "L"),
                   ("Z", "RHO"),
                   ),
                  )

    links = {(2,1): (((2,3),1),((2,4),1)), #2-1
             (2,2): (((2,3),2),((2,4),2)), #2-2
             (2,3): (((2,1),1),((2,2),1)), #2-3
             (2,4): (((2,1),2),((2,2),2)), #2-4
             }
else:
    import wordlist
    import grid
    if mode == END_TO_END_TEST:
        g = grid.grid("grid_square.txt")
        candidates = wordlist.parse_csv(wordlist.FILE, WILDCARD)
#        xlate = False
    elif mode == PAYROLL:
        g = grid.grid("grid_nu.txt")
        candidates = wordlist.parse_csv(wordlist.FILE, WILDCARD)
    elif mode == RIVALRIES:
        g = grid.grid("grid_rivalries.txt")
        candidates = wordlist.parse_txt(wordlist.FILE_TXT, WILDCARD)
        xlate = False
    elif mode == TREASURE_CHEST:
        g = grid.grid("biggrid.txt")
        candidates = wordlist.parse_txt(wordlist.TREASURE_TXT, WILDCARD)
        xlate = False

    links = g.links

candidate_sets = [ count_dict(n) for n in candidates ]

answers = dict((key, [WILDCARD]*len(value)) for key,value in links.iteritems())

unsolved = set(links)

first_pos = set(unsolved).pop()

print "Total answers:", len(unsolved)

order = [7, 1, 8, 6, 9, 12, 2, 5, 11, 3, 10, 4]
low_water_mark = len(unsolved)
print "Trying raw"
t1 = time()
for solution in solve(first_pos, unsolved.difference((first_pos,)), answers, candidate_sets, links):
    print "Solved:"
    if (mode == SIMPLE_TEST):
        print solution
    else:
        g.printSolution(solution, order)
t2 = time()
print '%s took %0.3f ms' % ("Raw", (t2-t1)*1000.0)
print "Low water mark:", low_water_mark

if xlate:
    trans_dict = {
        "ALPHA" : "A",
        "BET" : "b",
        "BETA" : "B",
        "CHI" : "X",
        "PHI" : "f",
        "HE" : "i",
        "KAPPA" : "K",
        "MEM" : "O",
        "MU" : "M",
        "NU" : "N",
        "NUN" : "n",
        "PE" : "e",
        "PI" : "i",
        "PSI" : "p",
        "QOF" : "P",
        "RESH" : "r",
        "RHO" : "P",
        "SHIN" : "W",
        "SIGMA" : "s",
        "TAU" : "T",
        "TET" : "t",
        "XI" : "x",
        "YOD" : "y",
        "ZAYIN" : "T",
        }

    low_water_mark = len(unsolved)
    tlate = transliterate(candidate_sets, trans_dict)
    print "Trying translated"
    t1 = time()
    for solution in solve(first_pos, unsolved.difference((first_pos,)), answers, tlate, links):
        print "Solved:"
        if (mode == SIMPLE_TEST):
            print solution
        else:
            g.printSolution(solution, order)
    t2 = time()
    print '%s took %0.3f ms' % ("Translated", (t2-t1)*1000.0)

    print "Low water mark:", low_water_mark


