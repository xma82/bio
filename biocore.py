####################################
# Utilities of broader application #
####################################

def namesToFile(fasta, keepStart='N'):
    """Creates a file of names from a given fasta.
    """
    titles = []

    f = open(fasta, "r")

    for line in f:
        if ">" in line:
            if (keepStart.upper() == 'N'):
                titles.append(line.lstrip('>'))
            elif (keepStart.upper() == 'Y'):
                titles.append(line)
            else:
                print("keepStart input unclear, accepts Y/N only")
                return
    f.close()

    n = open(r'names_out.txt', 'w')

    for element in titles:
        n.write(element)
    n.close()

def fastaToDict(fasta):
    """Given a fasta as its harddrive location, returns a dictionary
    where keys are the strain name and values are their associated
    sequences. Note that dictionaries are unordered.
    """
    strains = {}
    seqcatch = ""
    f = open(fasta, "r")
    
    for line in f: #take name from > to /n, seq from /n to >
        if ">" in line:
            tmp = line[1:-1]
            strains[tmp] = seqcatch
            seqcatch = ""
        else:
            seqcatch += line.rstrip()
        strains[tmp] = seqcatch
    f.close()
    return(strains)

def getStats(filename, returnLens='N'):
    """Given a fasta, return the top, bottom and mean lengths.
    Can also optionally return the full list of sequence lengths.
    """

    # NB: Replacing with a 'FASTA' class might be the best future solution

    if returnLens.upper() not in ['Y', 'N']:
        return ("Invalid value entered for returnFull, function only accepts Y or N.")

    contigLengths = [0]
    x = -1 # This can probably be replaced with something better suited

    f = open(filename, "r")

    # Get list of sequence lengths
    for line in f:
        if ">" in line:
            # Create new entry in contigLengths ()
            contigLengths.append(0)
            x += 1
        else:
            # Add length of line to value for that contig
            contigLengths[x] += len(line.rstrip('\n'))

    contigLengths = contigLengths[:-1] # Removes excess list entry
    totalMean = sum(contigLengths) / len(contigLengths)

    # Calculate N50 (The smallest contig length that at least half the nucleotides belong to)
    contigLengths.sort(reverse=True)
    print (contigLengths)
    tmpTotal = 0

    for index, value in enumerate(contigLengths):
        tmpTotal += int(contigLengths[index])
        if tmpTotal > (sum(contigLengths) / 2):
            N50 = contigLengths[index]
            break

    if returnLens.upper() == 'Y':
        print ("Contig lengths: " + str(contigLengths))

    print ("Mean: " + str(totalMean))
    print ("N50: " + str(N50))
    print ("Top: " + str(max(contigLengths)))
    print ("Bottom: " + str(min(contigLengths)))
    print ("Contigs: " + str(len(contigLengths)))
    # Could also add mode, median etc.

#########################
# Biologically Relevant #
#########################

def countNucs(seq):
    """Return the number of A, C, G & Ts within a sequence of DNA given
    as a string.
    """
    # Add DNA/RNA check
    A = C = G = T = 0
    for x in list(seq):
        if x == "a" or "A":
            A += 1
        elif x == "c" or "C":
            C += 1
        elif x == "g" or "G":
            G += 1
        elif x == "t" or "T":
            T += 1
    print(str(A) + ' ' + str(C) + ' ' + str(G) + ' '+ str(T))

def transcribe(seq):
    """Converts a sequence of bases, provided as a string, from RNA to
    DNA or DNA to RNA. An automatic check is included to determine if
    the given sequence is DNA or RNA.
    """
    seq.upper()
    newSeq = ""

    #DNA/RNA check
    if "U" in seq:
        switch = "toDNA"
        if "T" in seq:
            print("Invalid sequence, contains both DNA and RNA. " +\
                  "Function aborted.")
            return
    if "T" in seq:
        switch = "toRNA"
        if "U" in seq:
            print("Invalid sequence, contains both DNA and RNA. " +\
                  "Function aborted.")
            return
    
    #Sequence conversion
    if switch == "toDNA":
        for x in list(seq):
            if x == "U":
                newSeq += "T"
            else:
                newSeq += str(x)
    elif switch == "toRNA":
        for x in list(seq):
            if x == "T":
                newSeq += "U"
            else:
                newSeq += str(x)
    print(newSeq)

def getComplement(seq):
    """Returns the reverse complement of a given sequence,
    as a string
    """
    revSeq = seq[::-1]
    newSeq = ""
    for x in list(revSeq):
        if x == "A":
            newSeq += "T"
        elif x == "C":
            newSeq += "G"
        elif x == "G":
            newSeq += "C"
        elif x == "T":
            newSeq += "A"
    print(newSeq)

def getHeteroProb(k, m, n):
        """Returns the probability of gaining a dominate positive
        offspring for a pairing within a population where dominant (k),
        heterozygous (m) and recessive (n) traits are known
        """

        # Probability of parent X being D, H or R
        D = k/(k+m+n)
        H = m/(k+m+n)
        R = n/(k+m+n)

        # Probability of parent Y being D, H or R
        DD = (k-1)/((k+m+n)-1)
        Dx = (k)/((k+m+n)-1)
        HH = (m-1)/((k+m+n)-1)
        Hx = (m)/((k+m+n)-1)
        RR = (n-1)/((k+m+n)-1)
        Rx = (n)/((k+m+n)-1)

        # Probabilities of dominant positive for pairings
        pDD = 1
        pDH = 1
        pDR = 1
        pHH = 0.75
        pHR = 0.5
        pRR = 0

        # Full calculation
        prob = (D*DD*pDD)+(D*Dx*pDH)+(D*Dx*pDR)+(H*HH*pHH)+(H*Hx*pDH)+(H*Hx*pHR)+(R*RR*pRR)+(R*Rx*pDR)+(R*Rx*pHR)
        print(prob)        

def getGC(fasta):
    """Given the location of a fasta, returns the GC value for each
    strain as a dictionary.
    """
    strains = fastaToDict(fasta) #convert fasta into dictionary
    strainsGC = {}
    for key in strains: #calculate GCs and assign to strains
        GC = 0
        for base in strains[key]:
            if base in ("G", "C"):
                GC += 1
        GCperc = (GC / len(strains[key])) * 100
        strainsGC[key] = GCperc
    return(strainsGC)
    
    
def getHighestGC(fasta):
    """Given a fasta file location, prints the strain with the highest
    GC content and its value.
    """
    strainsGC = getGC(fasta) #get GCs
    highestGC = 0
    highestGCstrain = ""
    for key in strainsGC: #find the highest GC, return the strain & value
        if strainsGC[key] > highestGC:
            highestGC = strainsGC[key]
            highestGCstrain = key
    print(str(highestGCstrain))
    print(str(strainsGC[highestGCstrain]))

def calcHamming(A, B):
    """Calculate the Hamming distance between two sequences (as strings)
    of equal length.
    """
    dH = 0
    if len(A) == len(B):
        for index, value in enumerate(A):
            if value != B[index]:
                dH += 1
    if len(A) != len(B):
        print("Error: Sequences must be the same length!")
        return
    print(dH)

def RNAtoPro(seq):
    """Given an RNA sequence, as a string, returns the protein
    sequence.
    """
    ##Convert RNA to Protein
    #Could include a "check type" function to check if DNA/RNA/Protein
    protein = ""
    end = False
    ticker = 0
    RNAcodons = {"UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
                 "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
                 "UAU": "Y", "UAC": "Y", "UAA": "-", "UAG": "-",
                 "UGU": "C", "UGC": "C", "UGA": "-", "UGG": "W",
                 "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
                 "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
                 "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
                 "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
                 "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
                 "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
                 "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
                 "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
                 "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
                 "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
                 "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
                 "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"}
    while end == False:
        fc = ticker
        codon = seq[fc:fc+3]
        protein += RNAcodons[codon]
        ticker += 3
        if fc+3 >= len(seq):
            end = True
    print(protein)

def findMotif(motif, seq):
    """Searches for a given motif within a sequence, returning the
    locations of each find as an integer.
    """
    locations =  []
    mod = 1
    for index, base in enumerate(seq):
        if base == motif[0]:
            while mod < len(motif) and (index + mod) < len(seq):
                if seq[index+mod] == motif[mod]:
                    print("Base match found, scanning for whole motif...")
                    mod += 1
                else:
                    mod = 1 #NB: reset mod on fail
                    break
            if mod >= len(motif):
                print("Whole motif found, adding location...")
                print(seq[index:index+mod])
                locations.append(index+1)
                mod = 1
    print("Full sequence scanned, returning locations...")
    print(locations)

def findConsensus(fasta):
        """Returns the consensus string and profile matrix for a given
        set of strains.
        Strains must be provided as a fasta. NB: Errors will occur when
        there is a base conflict.
        """
        base = ['A', 'C', 'G', 'T']
        baseDict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        count = 0
        consensus = ""

        #pull sequences into a dictionary {strain: sequence}
        sequences = fastaToDict(fasta)

        #check sequences are the same length, else abort
        #if check passes, assigns that length to seqLength
        seqLen = []
        for value in sequences.values():
                seqLen.append(len(value))
        if max(seqLen) != min(seqLen): #exit if sequences different lengths
                print("Error: Sequences must be of the same length!")
                print("Sequences current range from " + str(min(seqLen)) +\
                      " to " + str(max(seqLen)) + " bases long.")
                return
        else: #set sequence lengths
                seqLength = max(seqLen)
                
        #create empty matrix
        profile = [[0]*seqLength for i in range(4)]

        #populate matrix
        for value in sequences.values():
                for basePos, baseType in enumerate(value):
                       profile[baseDict[baseType]][basePos] += 1
                       #NB: base position = y, base type = x
        
        for i in range(seqLength):
                colHolder = []
                for value, x in enumerate(profile):
                        colHolder.append(profile[value][i])
                consensus += (base[colHolder.index(max(colHolder))])

        #print consensus string
        print(consensus)
                
        #print profile matrix
        for x in profile:
                row = ' '.join(map(str, x))
                print(base[count] + ": " + row)
                count += 1