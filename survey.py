"""Problem A Homework 2 ECS145
Group Members:
    John Nguyen 998808398
    Eric Du 913327304
    Joanne Wang
    Jeffrey Tai 998935915
Todo:
    *Finish calcfreqs
    *Handle NA in the input
    *Generate all the combinations
    *
"""
import fnmatch

def calcfreqs(infile, nqs, maxrat):
    """ Calculates the frequency of each answer combination, the return value would be a dictionary
    Args:
        infile: input file with
        nqs: the number of questions in the survey
        maxrat: max number of choices
    Returns:
        dictionary with key as the answer combination and value as the frequency
    """
    freqs = {}
    input_data = reader(infile, maxrat)
    dirty_data = {}
    for val in input_data:
        if val in freqs:
            freqs[val] += 1
        elif 'NA' not in val:
            freqs[val] = 1
        elif 'NA' in val and val not in dirty_data:
            dirty_data[val] = (float(nqs) - float(val.count('NA'))) / float(nqs)
        elif 'NA' in val and val in dirty_data:
            dirty_data[val] += (float(nqs) - float(val.count('NA'))) / float(nqs)

    filtered = filter_data(dirty_data, freqs)
    for tup in filtered:
        if tup[0] in freqs:
            freqs[tup[0]] += tup[1]

    return freqs


def highfreqs(freqs, k):

    #ranked dictionary
    result = {}

    #SET of all frequencies
    valSet = []

    for i in freqs.values():
        if i not in valSet:
            valSet.append(i)

    #sorts in descending order
    valSet = sorted(valSet, key=float, reverse=True)

    #list of keys and its frequencies
    kth = [(key, value) for key, value in freqs.items()]
    
    if abs(k) < len(valSet):
        if k > 0:
            #filters only the top k
            kth = filter(lambda val: val[1] >= valSet[k-1], kth)
        else:
            #filters only the bottom k
            kth = filter(lambda val: val[1] <= valSet[len(valSet) - abs(k)], kth)

    #puts it in resulting dictionary
    for i in kth:
        result[i[0]] = i[1]

    return result


def filter_data(dirty_data, freqs):
    """ Pattern matches the NA with the keys in our freqs dictionary
        Args:
            dirty_data: all the entries with NA
            freqs: frequency dictionary
        Returns:
            a list of matches and its frequency
        """
    filtered = []
    dirty_keys = [(key.replace('NA', '*'), val) for key, val in dirty_data.items()]
    freq_keys = [key for key in freqs.keys()]
    for key in dirty_keys:
        matches = fnmatch.filter(freq_keys, key[0])
        for i,v in enumerate(matches):
            matches[i] = (v,key[1])
        filtered.extend(matches)
    return filtered


def reader(infile, maxrat):
    """ Reads in the input file and returns a list of data
        Args:
            infile: input file with
            nqs: the number of questions in the survey
            maxrat: max number of choices
        Returns:
            list of data that contains the answer to each question
        Raises:
                IOError: File not found. If the file doesurvsn't exist.
                ValueError: If a line in the file is found to have an error.
        """
    try:
        with open(infile, 'r') as infile:
            input_data = infile.read().splitlines()
    except IOError:
        raise Exception("File not found.")
    if len(input_data[0].split()) > maxrat:
        raise Exception("Invalid input")
    input_data = [','.join(data.split()) for data in input_data]
    return input_data

calcfreqs('test3.txt', 3, 5)
