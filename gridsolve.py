# Crossword puzzle solver

WILDCARD = "*"

##links = {(2,1):  (None,((3,1),2)),      #2-1
##         (2,2):  (((4,1),3),((2,3),1)), #2-2
##         (2,3):  (((4,1),3),((2,3),1)), #2-3
##         (2,4):  (((4,1),3),((2,3),1)), #2-4
##         (2,5):  (((4,1),3),((2,3),1)), #2-5
##         (2,6):  (((4,1),3),((2,3),1)), #2-6
##         (2,7):  (((4,1),3),((2,3),1)), #2-7
##         (2,8):  (((4,1),3),((2,3),1)), #2-8
##         (2,9):  (((4,1),3),((2,3),1)), #2-9
##         (2,10): (((4,1),3),((2,3),1)), #2-10
##         (2,11): (((4,1),3),((2,3),1)), #2-11
##         (2,12): (((4,1),3),((2,3),1)), #2-12
##         (2,13): (((4,1),3),((2,3),1)), #2-13
##         (2,14): (((4,1),3),((2,3),1)), #2-14
##         (2,15): (((4,1),3),((2,3),1)), #2-15
##         (2,16): (((4,1),3),((2,3),1)), #2-16
##         (2,17): (((4,1),3),((2,3),1)), #2-17
##         (2,18): (((4,1),3),((2,3),1)), #2-18
##         (2,19): (((4,1),3),((2,3),1)), #2-19
##         (2,20): (((4,1),3),((2,3),1)), #2-20
##         (2,21): (((4,1),3),((2,3),1)), #2-21
##         (2,22): (((4,1),3),((2,3),1)), #2-22
##         (2,23): (((4,1),3),((2,3),1)), #2-23
##         (2,24): (((4,1),3),((2,3),1)), #2-24
##         (3,1) : (((4,1),3),((2,3),1),((2,3),2)), #3-1
##         }
##
links = {(2,1): (((2,3),1),((2,4),1)), #2-1
         (2,2): (((2,3),2),((2,4),2)), #2-2
         (2,3): (((2,1),1),((2,2),1)), #2-3
         (2,4): (((2,1),2),((2,2),2)), #2-4
         }

def count_dict(keys):
    d = {}
    for key in keys:
        d[key] = d.get(key,0) + 1
    return d

import grid
g = grid.grid("grid.txt")

links = g.links

candidates = ((("ALPHA", "ALPHA"),
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
               (WILDCARD,),
               ),
              )

import wordlist

candidates = wordlist.parse(wordlist.FILE, WILDCARD)

candidate_sets = [ count_dict(n) for n in candidates ]

answers = dict((key, [WILDCARD]*len(value)) for key,value in links.iteritems())

unsolved = set(links)

def partial_match(x,filt):
    if x == (WILDCARD,):
        return True
    
    if len(x) < len(filt):
        return False

    for cf, cx in zip(filt,x):
        if (cf != WILDCARD and cf != cx and cx != WILDCARD):
            return False

    return True

trans_dict = {
    "ALPHA" : "A",
    "BET" : "B",
    "BETA" : "B",
    "CHI" : "C",
    "PHI" : "F",
    "HE" : "H",
    "KAPPA" : "K",
    "MU" : "M",
    "NU" : "N",
    "NUN" : "N",
    "PE" : "P",
    "PI" : "P",
    "PSI" : "P",
    "QOF" : "Q",
    "RESH" : "R",
    "RHO" : "R",
    "SHIN" : "S",
    "SIGMA" : "S",
    "TAU" : "T",
    "TET" : "T",
    "XI" : "X",
    "YOD" : "Y",
    "ZAYIN" : "Z",
    }

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
    l = len(link_list[pos]) - 2
    consts = ans[pos]
    if consts:
        possibilities = (x for (x,y) in cands[l].iteritems() if y > 0 and partial_match(x, consts))
    else:
        possibilities = (x for (x,y) in cands[l].iteritems() if y > 0)

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
            for link, c in zip(link_list[pos],word):
##                print link,c
                # if this word has no corresponding link for this letter, continue
                if not link:
                    continue
                (p,z) = link
                # Adjust the numbers to be zero indexed
                z -= 1

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

#        if solve(

first_pos = set(unsolved).pop()

for solution in solve(first_pos, unsolved.difference((first_pos,)), answers, candidate_sets, links):
    print "Solved:"
    print solution
    
##for solution in solve(first_pos, unsolved.difference((first_pos,)), answers, transliterate(candidate_sets, trans_dict), links):
##    print "Solved:"
##    print solution
##

