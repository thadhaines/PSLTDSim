import os

def exportDict(mirror):
    """Export system dictionary to disk
    Returns path to saved dictionary
    """

    # Change current working directory to data destination.
    cwd = os.getcwd()
    if mirror.simParams['fileDirectory'] :
        os.chdir(cwd + mirror.simParams['fileDirectory'])

    dictName = mirror.simParams['fileName']
    D = ltd.data.makeModelDictionary(mirror)
    savedName = ltd.data.saveModelDictionary(D,dictName)
    savedPath = os.getcwd() + '\\' + savedName
    os.chdir(cwd)

    return savedPath
