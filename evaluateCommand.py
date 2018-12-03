def evaluate(word, certainty, threshold, acceptedWords):
    """This function evaluates whether we should unlock our device or not
            Input:
                word: tf top word recognized
                certainty: how certain tf was of that word
                threshold: threshold for certainty
                acceptedWords: list of accepted words
            Output:
                true, false based on conditionals
    """
    #Check if the word is one of the acceptedWords
    if word in acceptedWords:
        #Check if the certainty is above the threshold
        if certainty > threshold:
            return True
        else: 
            return False
    return False
