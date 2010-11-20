import csv

def parse(filename, wildcard = "*"):
    infile = open(filename, "rb")
    csv_in = csv.reader(infile)

    words = {}
    section = -1
    max_section = 0
    for record in csv_in:
        if (not record[0]):
            section = -1
            
        if (section < 0):
            try:
                section = int(record[2])
                max_section = max(section, max_section)
                words.setdefault(section,[])
            except:
                pass
            continue

        if (record[0] == '?'):
            word = (wildcard,)
        else:
            word = tuple(record[2:3+section])

        words[section].append(word)

    infile.close()

    candidates = []
    for ix in xrange(1,max_section + 1):
        candidates.append(tuple(words.get(ix,tuple())))

    return candidates

FILE = "164.csv"

if __name__ == "__main__":
    print parse(FILE)
