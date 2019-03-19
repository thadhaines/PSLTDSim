import os

def exportDict(mirror):
    """Make and Export mirror dictionary to disk
    Returns path to saved dictionary
    """

    # Change current working directory to data destination.
    cwd = os.getcwd()
    if mirror.simParams['fileDirectory'] :
        os.chdir(cwd + mirror.simParams['fileDirectory'])

    dictName = mirror.simParams['fileName']
    D = ltd.data.makeMirrorDictionary(mirror)
    savedName = ltd.data.saveMirrorDictionary(D,dictName)
    savedPath = os.getcwd() + '\\' + savedName
    os.chdir(cwd)

    return savedPath
