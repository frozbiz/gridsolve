import csv
def parse_txt(filename, wildcard = "*"):
    words = {}
    max_len = 0
    with open(filename, "rb") as infile:
        for line in infile:
            word = line.strip()
            l = len(word)
            if (l > 0):
                words.setdefault(len(word),[]).append(word)
    
    candidates = []
    l = len(words)
    ix = 1
    while l:
        if (ix in words):
            candidates.append(tuple(words[ix]))
            l -= 1
        else:
            candidates.append(())
        ix += 1

    return candidates

def parse_csv(filename, wildcard = "*", confidence_factor = 1):
    infile = open(filename, "rb")
    csv_in = csv.reader(infile)

    words = {}
    section = -1
    max_section = -1
    for record in csv_in:
        if (not record[0]):
            section = -1
            
        if (section < 0):
            try:
                section = int(record[2])
                max_section = max(section, max_section)
                words.setdefault(section,[])
            except ValueError:
##                print record[0]
                pass
            continue
        try:
            confidence = int(record[1])
        except ValueError:
            confidence = 10

        if (record[0] == '?' or confidence < confidence_factor):
##            print record[0]
            word = (wildcard,)
        else:
            word = tuple(record[2:3+section])

        words[section].append(word)

    infile.close()

    candidates = []
    for ix in xrange(0,max_section + 1):
        candidates.append(tuple(words.get(ix,tuple())))

    return candidates

FILE = "164.csv"
FILE_TXT = "words_rivalries.txt"
TREASURE_TXT = "treasure_chest.txt"

if __name__ == "__main__":
    print parse_csv(FILE)
    print parse_txt(FILE_TXT)
    print parse_txt(TREASURE_TXT)
