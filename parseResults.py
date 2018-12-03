def parseResults(filename):
    """This function parses the given filename into words and levels are certainty from 
        the tensorflow output
            Input:
                filename: name of the file that tensorflow output to
            Output:
                word: top word recognized by tf
                certainty: top how certain tf was of the words in the same order
    """
    with open(filename) as f:
        lines = f.read()
    lines = lines.split()
    
    return lines[0], float(lines[1])    

