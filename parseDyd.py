"""Parse dyd file information to python mirror
assumes each line is a separate dynamic element of the form:
genrou 12 "GRANDC-G3   " 20.00  "1 "  : #9 mva=9000.0000 6.0000 0.0250 0.0600 0.0400 5.0000 0.0000 1.2000 0.7000 0.3000 0.2300 0.2200 0.1700 0.0500 0.3000 0.0000 0.0000 0.0000 0.0000
"""

import PSLF_model_templates as pmod

def parseDyd(m_ref,dydLoc):
    """Function that parses dyd information to mirror
    Will parse particular dyd models to intermediate classes
    these classes will be referenced by the model to populate dynamic properties
    """

    file = open(dydLoc, 'r') # open file to read
    line = next(file) # get first line of file
    foundModels = 0

    while line:
        if line[0] == '#' or line[0] =='\n':
            # line is a comment, skip
            line = next(file, None)
            continue
        
        #print(line) # Debug
        parts = line.split()
    
        if parts[0] == "genrou":
            newPmod = pmod.genrou(line)
            m_ref.PSLFdynamics.append(newPmod)
            foundModels += 1
  
        line = next(file,  None) # get next line, if there is one

    file.close() # close file
    if m_ref.debug == 1:
        print("Parsed %d models from dyd:  %s" % (foundModels, dydLoc))